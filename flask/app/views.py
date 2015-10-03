# Create views for the html page
from app import app
import json
import time, datetime
from datetime import datetime
from flask import jsonify, render_template, request
from cassandra.cluster import Cluster
#import happybase
#import ast

@app.route('/')
@app.route('/index')
def index():
   return "Hiii! Wo ai nii"

@app.route('/maps')
def maps():
   return render_template('index.html')

@app.route('/maps_free')
def maps_free():
   return render_template('index2.html')

@app.route('/batch_chart/')
def batch():
   return render_template('batch.html')

@app.route('/steps/')
def steps():
   return render_template('steps.html')

@app.route('/slidedeck')
def slidedeck():
   return render_template('slidedeck.html')

@app.route("/real/")
def real_busy():
   cluster = Cluster(['54.175.157.12'])
   session = cluster.connect()
   session.set_keyspace("keyspace_realtime")
   rows = session.execute("SELECT * FROM mytable")
   response_list=[]
   for val in rows:
      response_list.append(val)
   json_response = [{"name": x.name, "latitude": x.latitude, "longitude": x.longitude, "steps": x.steps, "status": x.status} for x in response_list]
   return jsonify(result=json_response)

@app.route("/real2/")
def only_free():
   cluster = Cluster(['54.175.157.12'])
   session = cluster.connect()
   session.set_keyspace("keyspace_realtime")
   rows = session.execute("SELECT * FROM mytable")
   response_list=[]
   for val in rows:
      if val.status == 'True':
         response_list.append(val)
   json_response = [{"name": x.name, "latitude": x.latitude, "longitude": x.longitude, "steps": x.steps} for x in response_list]
   return jsonify(result=json_response)



@app.route("/batch/")
def batch_raw():
   cluster = Cluster(['54.175.157.12'])
   session = cluster.connect()
   session.set_keyspace("keyspace_batch")
   rows = session.execute("SELECT * FROM mytable_rdd")
   
   tmp_dict={}
   for val in rows:
      date_str = str(val.hour)
      date_time = datetime(year=int(date_str[0:4]), month=int(date_str[4:6]), day= int(date_str[6:8]), hour=int(date_str[8:10]))
      epoch = int(date_time.strftime("%s")) * 1000
      tmp_dict[epoch]= val.number_of_users
   keys = tmp_dict.keys()    
   keys.sort()

   json_response = []
   for key in keys:
      json_response.append([key, tmp_dict[key]])
   return render_template("batch.html", json_response=json_response )


# @app.route("/history_zipcode_daily", methods=['POST'])
# def history_zipcode_daily_post():
#     zipcode = request.form["zipcode"]
#     stmt = "SELECT house_zipcode, date, count FROM trending_zipcode_by_day WHERE house_zipcode = %s ALLOW FILTERING"
#     response = session.execute(stmt, parameters=[zipcode])
    
#     tmp_dict = {}
#     for val in response:
#         date_string = str(val.date)
#         date_time = datetime(year=int(date_string[0:4]), month=int(date_string[4:6]), day=int(date_string[6:8]))
#         epoch = int(date_time.strftime("%s")) * 1000
#         tmp_dict[epoch] = val.count
#     keys = tmp_dict.keys()
#     keys.sort()
    
#     jsonresponse = []
#     for key in keys:
#         jsonresponse.append([key, tmp_dict[key]])
#     return render_template("history_zipcode_daily.html", zipcode=zipcode, jsonresponse=jsonresponse)

