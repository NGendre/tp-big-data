docker cp mapper.py hadoop-master:/root/
docker cp reducer.py hadoop-master:/root/
docker cp ../classes hadoop-master:/root/
docker cp data.csv hadoop-master:/root/
docker cp job.sh hadoop-master:/root/
docker cp requirements.txt hadoop-master:/root/
docker exec hadoop-slave1 /bin/bash -c './service_slv.sh'
docker exec hadoop-slave2 /bin/bash -c './service_slv.sh'
docker exec hadoop-master /bin/bash -c './job.sh'