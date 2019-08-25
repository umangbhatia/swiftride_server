from flask import Flask, render_template,request

from predict import *
from crowd_prediction import *


app = Flask(__name__)

list_bt = set()

passengers = {}

list_notify = set()

response1 = 0

buddy_network = {}


iter_num = 0

@app.route("/")
def index():
    return "Index!"

@app.route('/uploadfile',methods=['GET','POST'])
def uploadfile():
	global response1;
	if request.method == 'POST':
		f = request.files['upload']
		filePath = "./images/test.jpg"
		f.save(filePath)

		response1 = predict_num(filePath)

		
		return "faces= {0}".format(response1)

@app.route('/scan_data',methods=['GET','POST'])
def scan_data():
	global iter_num, list_bt, list_location, passengers

	prev_num = iter_num
	if request.method == 'POST':
		content = request.get_json(force=True)
		
		num = content["iter"]
		mac = content["mac"]
		self = content["self"]
		lat = float(content["lat"])
		lon = float(content["lon"])


		print(num)
		print(mac)
		print(lat)
		print(lon)
		
		print(self)
		
		

		
		if(num != prev_num):
			iter_num = num
			list_bt = set()
		
		list_bt.add(mac)

		list_bt.add(self)
			

		passengers[self]=(lat,lon)




		
		
	print(passengers)
	
	dic = {
		"bt" : len(list_bt),
		"location" : len(passengers),
		"head": response1			
	}



	return dic


@app.route('/predict_crowd',methods=['GET','POST'])
def predict_crowd():
	if request.method == 'POST':

		content = request.get_json(force=True)

		date = content["date"]
		time = content["time"]

		print(date)
				
		print(time)


		pred = multilinear_regression(date, time)

		print(pred)
		
		
		dic = {
		
		"density" : pred[1]
			
	}


	return dic



@app.route("/incoming_sos", methods=['GET','POST'])
def incoming_sos():
	global list_notify, passengers

	if request.method == 'POST':

		content = request.get_json(force=True)

		mac = content["mac"]
		lat = float(content["lat"])
		lon = float(content["lon"])

		for key in passengers:
			if(key!=mac):
				x,y = passengers[key]

				if((lat-x)*(lat-x)+(lon-y)*(lon-y) < 10):
					list_notify.add(key)

	print(list_notify)
	return "abc"

@app.route("/outgoing_sos", methods=['GET','POST'])
def outgoing_sos():
	global list_notify

	if request.method == 'POST':

		content = request.get_json(force=True)

		mac = content["mac"]
		print(mac)

		for key in list_notify:
			print(key)
			if(key==mac):
				return {"notify": True}

	return {"notify": False}

@app.route("/find_buddy", methods=['GET','POST'])
def find_buddy():
	global buddy_network

	if request.method == 'POST':

		content = request.get_json(force=True)

		mac = content["mac"]
		name = content["name"]
		desc = content["desc"]
		topics = content["topics"]

		buddy_network[mac] = (name,desc,topics)
		print(buddy_network)
		if(len(buddy_network)>1):
			for key in buddy_network:
				if(key!=mac):
					name, desc, topics = buddy_network[key]

					return{"name": name, "desc":desc,"topics":topics}

	return{"name": "name", "desc":"desc","topics":"topics"}


@app.route("/members")
def members():
    return "Members"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)