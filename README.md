EasyAuc Notification

Implement email function and save the title and content of frequently used email type in MongoDB.


Email: docker run -di --name EasyAucEmail easyauc:email

docker exec -it EasyAucEmail /bin/bash
cd /src/email
python3 send_email.py

Watchlist: docker run -di --name EasyAucWatchlist -p 7000:7000 -p 27017:27017 easyauc:watchlist
docker exec -it EasyAucWatchlist /bin/bash
cd /src/watchlist
python3 watchlist.py

New Tab:
docker exec -it EasyAucWatchlist /bin/bash
cd /src/watchlist
python3 addNew.py
