from flask import Flask, render_template, request
from implementation import randorm_forest_test, random_forest_train, random_forest_predict
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random_forest import accuracy
from sklearn.metrics import accuracy_score
from time import time


import csv

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

import pandas as pd

from image_to_text import image_to_text
from text_to_csv import text_to_csv
from itertools import chain

# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert(lst, var_lst): #1d to 2d
	idx = 0
	for var_len in var_lst:
		yield lst[idx : idx + var_len]
		idx += var_len



@app.route('/')
def index():
	return render_template('home.html')


@app.route('/upload') 
def upload():
	disabled="disabled"
	return render_template('upload.html',disabled=disabled)



@app.route('/entries') 
def entries():
	return render_template('entries.html')



@app.route('/upload1', methods=['POST']) 
def upload_image():
	if request.method == 'POST':
		uploaded_img = request.files['image']
		#img_filename = secure_filename(uploaded_img.filename)
		img_filename="image.png"
		uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
		#session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
		success='file updated'
		
		return render_template('upload.html',success=success)


@app.route('/show') 
def show():
	image_to_text()
	text_to_csv()

	with open('static/files/image_extracted.csv', 'r') as read_obj:
		csv_reader = csv.reader(read_obj)
		two_d_list = list(csv_reader)
	data = list(chain.from_iterable(two_d_list))
	print(data)
	print(type(data)) #list
	str="hemanth"
	return render_template('display.html',data=data,str=str)


@app.route('/display', methods=['POST']) 
def display():
#image extraction

	data = []
	for i in range(1,31):
		data.append(float(request.form['value'+str(i)]))
	data_points = list()
	for i in range(30):
		data_points.append(data[i])
		
	print(data_points)
	print(type(data_points))   #list

	lst=data_points
	var_lst=[30]
	rows=list(convert(lst, var_lst))
	
	with open('static/files/image_edited.csv', 'w') as f:
		write = csv.writer(f)
		write.writerows(rows)

	data_np = np.asarray(data, dtype = float)
	data_np = data_np.reshape(1,-1)
	out, acc, t = random_forest_predict(clf, data_np)

	if(out==1):
		output = 'Malignant'
	else:
		output = 'Benign'

	acc_x = acc[0][0]
	acc_y = acc[0][1]
	if(acc_x>acc_y):
		acc1 = acc_x
	else:
		acc1=acc_y
	return render_template('result.html', output=output, accuracy=accuracy, time=t)



@app.route('/predict', methods=['POST']) 
def values():
#manually entering values

	data = []
	for i in range(1,31):
		data.append(float(request.form['value'+str(i)]))

	data_points = list()

	for i in range(30):
		data_points.append(data[i])
		
	print(data_points)
	print(type(data_points))   #list

	lst=data_points
	var_lst=[30]
	rows=list(convert(lst, var_lst))
	
	with open('static/files/manual_entries.csv', 'w') as f:
		write = csv.writer(f)
		write.writerows(rows)

	data_np = np.asarray(data, dtype = float)
	data_np = data_np.reshape(1,-1)
	out, acc, t = random_forest_predict(clf, data_np)

	if(out==1):
		output = 'Malignant'
	else:
		output = 'Benign'

	acc_x = acc[0][0]
	acc_y = acc[0][1]
	if(acc_x>acc_y):
		acc1 = acc_x
	else:
		acc1=acc_y
	return render_template('result.html', output=output, accuracy=accuracy, time=t)



if __name__=='__main__':
	global clf 
	clf = random_forest_train()
	randorm_forest_test(clf)
	#print("Done")
	app.run(debug=True)

