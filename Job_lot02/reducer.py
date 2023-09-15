import json
import sys
import matplotlib.pyplot as plt

import pandas as pd
from pandas import DataFrame
from tabulate import tabulate


headers = {
    "cpcli",
    "villecli",
    "codcde",
    "timbrecde",
    "timbrecli",
    "points",
    "datcde"
}

def print_df(df_to_print):
    print(tabulate(df_to_print, headers='keys', tablefmt='psql'))
def get_top_100(df: DataFrame):
    ret = DataFrame()
    grouped = df.groupby(['codcde'])
    for group,df in grouped:
        sum_points = df['points'].sum()
        preparedLine = df.iloc[0]
        preparedLine['points'] = sum_points
        preparedLine['nbcolis'] = df.__len__()
        ret = ret.append(other=preparedLine,ignore_index=True)
    return ret.nlargest(100,['points'])

def get_five_percent(df:DataFrame):
    ret = DataFrame()
    for index,row in df.iterrows():
        if str(row['cpcli'])[:2] in ['28','53','61']:
            ret = ret.append(other=row,ignore_index=True)
    ret = ret.sample(ret.__len__()//20)
    plt.figure(figsize=(6, 6))
    plt.pie(ret['points'], labels=ret['villecli'], autopct='%1.1f%%', startangle=90)
    plt.title('titre')
    plt.savefig('graphique.pdf',format='pdf')
    return ret


def to_excel(df1:DataFrame, df2: DataFrame):
    with pd.ExcelWriter('output.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Partie_1')
        df2.to_excel(writer, sheet_name='Partie_2')

df = DataFrame(columns=headers)
# count=0
for line in sys.stdin:
    # count +=1
    json_line = json.loads(line)
    df = df.append(json_line,ignore_index=True)
    # if count>20000:
    #     break
    # print(count)


a = get_top_100(df)
b = get_five_percent(a)
to_excel(a,b)










