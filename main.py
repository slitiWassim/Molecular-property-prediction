import os
import pandas as pd
from prediction import torchDrug
import subprocess
import time
import shlex
def activity(a:int):
      if(a==1):
            return "Inactive"
      else:
            return  "Active"
def toxcit(a:int):
      if(a==1):
            return "Toxic"
      else:
            return  "Not Toxic"
from werkzeug.utils import secure_filename
from flask import Flask, render_template, Response,  request, session, redirect, url_for, send_from_directory, flash
app=Flask(__name__,template_folder="./templates")
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route("/")
def index():
   return render_template("index.html")
   #return render_template("predict.html")
@app.route('/predict', methods=['GET', 'POST'])
def predict():
      if request.method == 'POST':
            f = request.form['smile']
            df = []
            df.append([f])
            test=pd.DataFrame(df,columns=["smiles"])
            test[["smiles"]].to_csv("test.csv", index=False)
            
            result=torchDrug(f)
            command = "/media/sliti-wassim/storage/anaconda3/envs/map4/bin/python Mp4.py --option1 -dir /path/to/dir"
            args = shlex.split(command)
            my_subprocess = subprocess.Popen(args)
            time.sleep(4.0)
            df1=pd.read_csv('result.csv')
            print(df1)
            sc1 = df1["1"][0]
            sc2 = df1["2"][0]
            sc3 = df1["3"][0]
            sc4 = df1["4"][0]
            sc5 = df1["5"][0]
            sc6 = df1["6"][0]
            print(sc1,sc2,sc3,sc4)
            ic5=activity(result[0])
            ec5=activity(result[1])
            ec9=activity(result[2])
            toxci=toxcit(result[3])
            #animal=ic5
            print(ic5,ec5,ec9,toxci)
            return render_template('predict.html',ec50=ec5,ic50=ic5,toxcity=toxci,ec90=ec9,sc1=sc1,sc2=sc2,sc3=sc3,sc4=sc4,sc5=sc5,sc6=sc6)
            #return render_template('predict.html',ic50 = ic5,ec50 = ec5,ec90 = ec9,toxcity = toxci)
            
      else:
            return render_template('predict.html')  
#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
 #     return render_template("uploaded.html", display_detection = filename, fname = filename)

app.run()
