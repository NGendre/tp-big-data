#!/usr/bin/python
"""reducer.py"""
import json
import sys
import pandas as pd
from pandas import DataFrame, set_option
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

set_option("display.max_columns", None)
set_option('display.expand_frame_repr', False)

df = None
count = 0
for line in sys.stdin:
    count += 1
    try:
        data = json.loads(line)
    except:
        continue
    if df is None:
        df = DataFrame([data])
    else:
        df.loc[len(df)] = data
    #print(count, "/ 5000")


def extract_departement(code_postal):
    if code_postal.isdigit() and len(code_postal) >= 2:
        return code_postal[:2]  # Les deux premiers caractères représentent généralement le département
    return None


'''def print_df(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))'''


df['datcde'] = pd.to_datetime(df['datcde'])
df['annee'] = df['datcde'].dt.year
df['departement'] = df['cpcli'].apply(extract_departement)

df_meyenne = df[(df['departement'] == '53') & (df['qte'] > 5)]  # & (df['annee'] >= 2010)
resultat = df_meyenne.groupby(['villecli', 'libobj', 'annee']).size().reset_index(name='nombre_de_commandes')

# print_df(resultat)
pivot_result = resultat.pivot_table(index=['annee', 'villecli'], columns='libobj', values='nombre_de_commandes', fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
pivot_result.plot(kind='bar', stacked=True, ax=ax)
plt.title('Nombre de Commandes par Ville (Mayenne, 53) par Objet (Quantité > 5) par Année depuis 2010')
plt.xlabel('Année et Ville')
plt.ylabel('Nombre de Commandes')
plt.legend(title='Objet')
# plt.show()
pdf_pages = PdfPages('lot1_1.pdf')
pdf_pages.savefig(fig)
pdf_pages.close()

df_2008 = df[df['annee'] >= 2004]
df_2008 = df_2008.copy()
df_2008.loc[:, "fidelité"] = df_2008['qte'] * df_2008['points']
df_2008.loc[:, "city_dept"] = df_2008['villecli'] + df_2008['departement']
grouped_data = df_2008.groupby(['codcli', 'city_dept', 'villecli', 'departement'])['fidelité'].agg(
    [('somme_fidelité', 'sum')]).reset_index()
# grouped_data['écrat_type_fidelité'] = grouped_data['écrat_type_fidelité'].fillna(0)
# print_df(grouped_data.tail(50))

top_10_clients = grouped_data.nlargest(10, 'somme_fidelité')
# print_df(top_10_clients)

commandes_top10_client = df_2008[df_2008['codcli'].isin(top_10_clients['codcli'])]
# print_df(commandes_top10_client)

aggreate_colis = commandes_top10_client.groupby(['codcli', 'city_dept', 'villecli', 'departement'])['Colis'].agg(
    [('somme_colis', 'sum'), ('moyenne_colis', 'mean'), ('écart_type_colis', 'std')]).reset_index()

#print_df(aggreate_colis)

fig = plt.figure(figsize=(8, 4))
plt.bar(aggreate_colis['villecli'], aggreate_colis['somme_colis'], label='Somme')
plt.bar(aggreate_colis['villecli'], aggreate_colis['moyenne_colis'], label='Moyenne')
plt.bar(aggreate_colis['villecli'], aggreate_colis['écart_type_colis'], label='Écart Type')
plt.xlabel('Ville')
plt.ylabel('Valeurs')
plt.title('Somme, Moyenne et Écart Type par Ville')
plt.legend()
plt.xticks(rotation=90)
pdf_pages = PdfPages('lot2_2_merged.pdf')
pdf_pages.savefig(fig)
pdf_pages.close()

for index, row in aggreate_colis.iterrows():
    fig = plt.figure(figsize=(8, 4))
    plt.bar(row['villecli'], row['somme_colis'], label='Somme')
    plt.bar(row['villecli'], row['moyenne_colis'], label='Moyenne', )
    plt.bar(row['villecli'], row['écart_type_colis'], label='Écart Type')
    plt.xlabel('Ville')
    plt.ylabel('Valeurs')
    plt.title('Somme, Moyenne et Écart Type pour {} ({})'.format(row['villecli'], row['departement']))
    plt.legend()
    pdf_pages = PdfPages('lot1_2_{}.pdf'.format(row['city_dept']))
    pdf_pages.savefig(fig)
    pdf_pages.close()

"""ville_group = top_10_clients.groupby(['city_dept', 'villecli', 'departement'])['somme_fidelité'].agg(
    [('somme_fidelité_ville', 'sum'), ('moyenne_fidelité_ville', 'mean'), ('écrat_type_fidelité_ville', 'std'),
     ('nb_client', 'size')]).reset_index()

# print_df(ville_group)

villes_uniques = grouped_data['city_dept'].unique()
resultats_villes = []
for ville in villes_uniques:
    ville_data = grouped_data[grouped_data['city_dept'] == ville]
    top_10_clients_ville = ville_data.nlargest(10, 'somme_fidelité')
    resultats_villes.append(top_10_clients_ville)

top_10_par_ville = pd.concat(resultats_villes, ignore_index=True)
agg_ville_top10 = top_10_par_ville.groupby(['city_dept', 'villecli', 'departement'])['somme_fidelité'].agg(
    [('somme_fidelité_ville', 'sum'), ('moyenne_fidelité_ville', 'mean'), ('écrat_type_fidelité_ville', 'std'),
     ('count', 'size')]).reset_index()
agg_ville_top10['écrat_type_fidelité_ville'] = agg_ville_top10['écrat_type_fidelité_ville'].fillna(0)"""
"""print("resultats_villes 2")
print_df(agg_ville_top10.sort_values(by="city_dept", ascending=True).tail(50))
"""

"""ville = "YERVILLE76"
toto = grouped_data[grouped_data['city_dept'] == ville]
print("toto")
print_df(toto)
ville_test_top10 = top_10_par_ville[top_10_par_ville['city_dept'] == ville]
print("ville_test_top10")
print_df(ville_test_top10)
vile_test = agg_ville_top10[agg_ville_top10['city_dept'] == ville]
print("vile_test")
print_df(vile_test)"""

selected_departments = ["53", "72", "49"]
df_departements = df[df['departement'].isin(selected_departments)]

grouped_data_df = df_departements.groupby(['annee', 'libobj', 'departement'])['codcde'].agg([("count", 'size')]).reset_index()

for departement in selected_departments:
    department_data = grouped_data_df[grouped_data_df['departement'] == departement]
    fig = plt.figure(figsize=(12, 6))

    unique_objects = department_data['libobj'].unique()
    for obj in unique_objects:
        obj_data = department_data[department_data["libobj"] == obj]
        plt.plot(obj_data['annee'], obj_data['count'], label=obj)

    plt.xlabel('Année')
    plt.ylabel('Nombre de Commandes')
    plt.title('Courbe de Croissance par Objet pour le Département {}'.format(departement))
    plt.xticks(rotation=90)
    plt.legend()

    pdf_pages = PdfPages('lot1_3_{}.pdf'.format(departement))
    pdf_pages.savefig(fig)
    pdf_pages.close()


