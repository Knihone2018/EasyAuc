import requests

port = 5672

def test0():
	p0 = requests.post(url="http://127.0.0.1:{}/droptable/boughtitems".format(port))
	print(p0.content)


def test1():
	d = {"userId":"123","itemId":"456","addQuantity":1,"isBid":False}
	p = requests.post(url="http://127.0.0.1:{}/additemtocartfrombuynow".format(port), json = d)
	print(p.content)

def test2():
	p1 = requests.get(url="http://127.0.0.1:{}/cart.html?id=2".format(port))
	print(p1.content)


def test3():
	e = {"userId":"123","itemId":"456"}
	p2 = requests.get(url="http://127.0.0.1:{}/getoneitemincart".format(port), json = e)
	print(p2.content)

def test4():
	e = {"email":"susanxu@126.com"}
	p3 = requests.post(url="http://127.0.0.1:{}/addaccount".format(port), json = e)
	print(p3.content)

def test5():
	p4 = requests.post(url="http://127.0.0.1:{}/setemail".format(port), json = {"userId":1, "email":"1234444@gmail.com"})
	print(p4.content)

def test6():
	p4 = requests.get(url="http://127.0.0.1:{}/getuseremail".format(port), json={"userId":1})
	print(p4.content)


def test7():
	p4 = requests.get(url="http://127.0.0.1:{}/checkdeleteaccount".format(port), json={"userId":1})
	print(p4.content)


def test7():
	p4 = requests.get(url="http://127.0.0.1:{}/checkblockaccount".format(port), json={"userId":1})
	print(p4.content)


def test8():
	p5 = requests.post(url="http://127.0.0.1:{}/additemstoboughtlist".format(port), json={"userId":1, "value":[(12, 1), (14, 2)]})
	print(p5.content)

	p6 = requests.get(url="http://127.0.0.1:{}//history.html?id=1".format(port))
	print(p6.content)


def test9():
	p7 = requests.get(url="http://127.0.0.1:{}/getitemisbid".format(port), json={"userId":"123","itemId":"456"})
	print(p7.content)

#test0()
test8()


    