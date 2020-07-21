
wget -c https://github.com/actiontech/dble/releases/download/2.20.04.0%2Ftag/actiontech-dble-2.20.04.0.tar.gz
tar -xvf tag.tar.gz

docker run --name backend-mysql1 -e MYSQL_ROOT_PASSWORD=123456 -p 33061:3306 -d mysql:8.0 --server-id=1 
docker run --name backend-mysql2 -e MYSQL_ROOT_PASSWORD=123456 -p 33062:3306 -d mysql:8.0 --server-id=2 

docker ps 

