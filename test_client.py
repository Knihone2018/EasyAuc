import requests

port = 5672

def test0():
	p0 = requests.post(url="http://127.0.0.1:{}/droptable/boughtitems".format(port))
	print(p0.content)


def test1():
	d = {"userId":"123","itemId":"456","addQuantity":1,"isBid":False}
	p = requests.post(url="http://127.0.0.1:{}/additemtocartfrombuynow".format(port), json = d)
	print(p.content)

#def test2():
#	p1 = requests.get(url="http://127.0.0.1:{}/cart".format(port), json={"userId":1})
#	print(p1.content)


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

	p6 = requests.get(url="http://127.0.0.1:{}//history".format(port), json={"userId":1})
	print(p6.content)


def test9():
	p7 = requests.get(url="http://127.0.0.1:{}/getitemisbid".format(port), json={"userId":"123","itemId":"456"})
	print(p7.content)


def test10():
	p = requests.post(url="http://127.0.0.1:{}/setpassword".format(port), json={"userId":"2","password":"111"})
	print(p.content)
	p8 = requests.post(url="http://127.0.0.1:{}/checkpassword".format(port), json={"email":"susanxu@126.com","password":"111"})
	print(p8.content)


def test11():
	p = requests.post(url="http://127.0.0.1:{}/additemtocartfrombuynow".format(port), json={"userId":2,"itemId":111,"addQuantity":2})
	print(p.content)
	p8 = requests.post(url="http://127.0.0.1:{}/checkoutcart".format(port), json={"userId":2})
	print(p8.content)


def test12():
	p = requests.get(url="http://127.0.0.1:{}/myaccount".format(port), json={"userId":2})
	print(p.content)


def test13():
	p = requests.post(url="http://127.0.0.1:{}/deleteaccount".format(port), json={"userId":2})
	print(p.content)

	p1 = requests.get(url="http://127.0.0.1:{}/checkdeleteaccount".format(port), json={"userId":2})
	print(p1.content)

	p2 = requests.post(url="http://127.0.0.1:{}/addaccount".format(port), json={"email":'susanxu@126.com'})
	print(p2.content)


	p3 = requests.get(url="http://127.0.0.1:{}/checkdeleteaccount".format(port), json={"userId":2})
	print(p3.content)


def test14():
	p = requests.post(url="http://127.0.0.1:{}/deleteitemfromcart".format(port), json={"userId":1, "itemId":2, "deleteQuantity":20})
	print(p.content)

	p2 = requests.post(url="http://127.0.0.1:{}/additemtocartfrombuynow".format(port), json={"userId":1,"itemId":3,"addQuantity":5})
	print(p2.content)

	p3 = requests.post(url="http://127.0.0.1:{}/deleteitemfromcart".format(port), json={"userId":1,"itemId":3,"deleteQuantity":2})
	print(p3.content)


def test15():
	p = requests.post(url="http://127.0.0.1:{}/addsellerrate".format(port), json={"sellerId":1, "rate":5})
	print(p.content)


#test0()
#test8()
#test10()
#test11()
#test13()
#test14()
test15()

