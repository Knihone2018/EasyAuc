sudo docker run --name EasyAuc-User -e MYSQL_ROOT_PASSWORD=a1s2d3f4 -p 8000:8000 -p 8100:3306 -d easyauc:user4


Set admin:

    /src:

    python create_admin.py



To run:

    /src:

    python main.py