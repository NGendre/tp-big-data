pip install -r requirements.txt
cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
sudo -u hdfs hadoop dfsadmin -safemode leave
hdfs dfs -mkdir -p input
hdfs dfs -put data.csv input
hdfs dfs -rm -r outputjob01
hadoop jar hadoop-streaming-2.7.2.jar -file mapper.py -mapper 'python3 mapper.py' -file reducer.py -reducer 'python3 reducer.py' -input input/data.csv -output outputjob01
