sudo docker run --name EasyAuc-User -e MYSQL_ROOT_PASSWORD=a1s2d3f4 -p 8000:8000 -p 8100:3306 -d easyauc:user3


Set admin:

    mysql -u root -p

    password: a1s2d3f4

    use USER;

    insert into Account (email, password) values ("admin@easyauc.com","123");



To run:

    /src:

    python main.py