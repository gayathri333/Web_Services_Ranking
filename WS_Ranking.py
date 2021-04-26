from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import glob
import json
import openpyxl
from openpyxl import Workbook
from pathlib import Path
import numpy as np
import pickle
import joblib
import pandas as pd
import operator

ALLOWED_EXTENSIONS = {'xlsx'}
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + r'/uploads/'
folder_path = os.path.dirname(os.path.abspath(__file__)) + r'\uploads'
app=Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       file1 = request.files['file1']
       file2 = request.files['file2']
       file3 = request.files['file3']
       file4 = request.files['file4']

       if file.filename == '' or file1.filename == '' or file2.filename == '' or file3.filename == '' or file4.filename == '':
           print('No file selected')
           return redirect(request.url)

       if file and file1 and file2 and file3 and file4 and allowed_file(file.filename) and allowed_file(file1.filename) and allowed_file(file2.filename) and allowed_file(file3.filename) and allowed_file(file4.filename):
           filename = secure_filename(file.filename)
           filename1 = secure_filename(file1.filename)
           filename2 = secure_filename(file2.filename)
           filename3 = secure_filename(file3.filename)
           filename4 = secure_filename(file4.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
           file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
           file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
           file4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename4))
           
           print('----------Web Service 1----------: \n')
           percent1=ranking(file)
           print('----------Web Service 2----------: \n')
           percent2=ranking(file1)
           print('----------Web Service 3----------: \n')
           percent3=ranking(file2)
           print('----------Web Service 4----------: \n')
           percent4=ranking(file3)
           print('----------Web Service 5----------: \n')
           percent5=ranking(file4)
           data = {filename: percent1,filename1: percent2,filename2: percent3,filename3: percent4,filename4: percent5}
           final_ranks = dict(sorted(data.items(),key=operator.itemgetter(1),reverse=True))
           delete_files()
           return render_template('results.html',ranking=final_ranks)
           return redirect(url_for('index', filename=file.filename))
           
   return render_template('index.html')

def ranking(file):
    clf1 = joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'model/classifier1.pkl'))
    clf2 = joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'model/classifier2.pkl'))
    clf3 = joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'model/classifier3.pkl'))
    xlsx_file = file
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    df = pd.read_excel(file)
    X=df.iloc[1:101,0:2].values
    res1 = clf1.predict(X)
    res2 = clf2.predict(X)
    res3 = clf3.predict(X)
    count1=0
    count2=0
    count3=0
    for x in res1:
      if x == 1:
        count1+=1
    for x in res2:
      if x == 1:
        count2+=1
    for x in res3:
      if x == 1:
        count3+=1
    percent=(count1+count2+count3)/3
    print('Classifier 1: ',res1)
    print('Classifier 2: ',res2)
    print('Classifier 3: ',res3)
    print('TS percent of the web service = ',percent,'% \n')
    return percent

def delete_files():
    for filename in glob.glob(os.path.join(folder_path, '*.xlsx')):
        print(filename)
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(debug=True)
