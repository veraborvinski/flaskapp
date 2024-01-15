from db import *
from datetime import *
import time
import sys
import mysql.connector

import json
import requests
# First we set our credentials

from flask_bootstrap import Bootstrap5
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.debug = True

@app.route('/Video/<video>')
def video_page(video):
     print (video)
     url = 'http://34.142.25.93/myflix/videos?filter={"video.uuid":"'+video+'"}'
     headers = {}
     payload = json.dumps({ })
     print (request.endpoint)
     response = requests.get(url)
     print (url)
     if response.status_code != 200:
          print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
          return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
     jResp = response.json()
     print (type(jResp))
     print (jResp)
     videofile = None
     pic = None
     ip = None
     for index in jResp:
        for key in index:
           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                    print (key2,index[key][key2])
                    if (key2=="Name"):
                         video=index[key][key2]
                    if (key2=="file"):
                         videofile=index[key][key2]
                    if (key2=="pic"):
                         pic=index[key][key2]
     if 'username' in session:
          cnx = mysql.connector.connect(user='remoteAccess', password='1234abcz',host='35.189.78.49', port=3306)
          cursr = cnx.cursor(buffered=True)
          insert_title(cnx,cursr,video,session['username'])
     return render_template('video.html', name=video,file=videofile,pic=pic)

@app.route('/')
def cat_page():
     username = request.args.get('username')
     if username is not None:
          session['username'] = username
          cnx = mysql.connector.connect(user='remoteAccess', password='1234abcz',host='35.189.78.49', port=3306)
          cursor = cnx.cursor()
          create_database(cnx,cursor,username)
          url = "http://34.142.25.93/myflix/videos"
          headers = {}
          payload = json.dumps({ })
          html="<h2>Your Videos</h2>"
          ServerIP=request.host.split(':')[0]
          
          response = requests.get(url)
          print (response)
          print (response.status_code)
          if response.status_code != 200:
               print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
               return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
          jResp = response.json()

          html=html+'<h3>Keep watching</h3>' 
          cnx = mysql.connector.connect(user='remoteAccess', password='1234abcz',host='35.189.78.49', port=3306)
          cursor = cnx.cursor(buffered=True)
          watchlist = get_watchlist(cnx,cursor,username)
          titlecount=0
          html=html+'<h3>'+category_index["category"]+'</h3>'    
          html=html+'<table style="width:100%" bgcolor="#d3d3d3">' 
          html=html+'<tr>' 
          for title in watchlist:
               for index in jResp:
                    print ("----------------")
                    for key in index:
                         if (key !="_id"):
                              name=None
                              uuid=None
                              thumb=None
                              for key2 in index[key]:
                                   print (key2,index[key][key2])
                                   if (key2=="Name"):
                                        name=index[key][key2]
                                   if (key2=="thumb"):
                                        thumb=index[key][key2]
                                   if (key2=="uuid"):
                                        uuid=index[key][key2]
                              if name is not None and uuid is not None and thumb is not None:
                                   if (index[key]["Name"]==title):
                                        if titlecount<5:
                                             html=html+'<th style="width:25%">'
                                        else:
                                             html=html+'<td style="width:25%">'
                                        html=html+'<a href="http://'+ServerIP+'/Video/'+uuid+'">'
                                        html=html+'<img width="300" height="200" src="http://34.147.236.169/pics/'+thumb+'">'
                                        html=html+"</a>"  
                                        html=html+'<h4>'+name+'</h4>'
                                        if titlecount<5:
                                             html=html+'</th>' 
                                        else:
                                             html=html+'</td>'
                                        titlecount = titlecount+1
          for i in range(titlecount,4):
               html=html+'<th style="width:25%"></th>'
          html=html+'</tr>' 
          html=html+'</table>' 
          
          html=html+'<h3>Recommended</h3>' 
          
          categories = requests.get("http://34.142.25.93/myflix/categories").json()
          for category_index in categories:
               for category in category_index:
                    if (category=="category"):
                         html=html+'<h3>'+category_index["category"]+'</h3>'    
                         html=html+'<table style="width:100%" bgcolor="#d3d3d3">' 
                         html=html+'<tr>' 
                         count = 0
                         for index in jResp:
                              print ("----------------")
                              for key in index:
                                   if (key !="_id"):
                                        print (index[key])
                                        for key2 in index[key]:
                                             print (key2,index[key][key2])
                                             if (key2=="Name"):
                                                  name=index[key][key2]
                                             if (key2=="thumb"):
                                                  thumb=index[key][key2]
                                             if (key2=="uuid"):
                                                  uuid=index[key][key2]
                                             if (key2=="category"):
                                                  if (index[key][key2]==category_index["category"]):
                                                       html=html+'<th style="width:25%">'
                                                       html=html+'<a href="http://'+ServerIP+'/Video/'+uuid+'">'
                                                       html=html+'<img width="300" height="200" src="http://34.147.236.169/pics/'+thumb+'">'
                                                       html=html+"</a>"  
                                                       html=html+'<h4>'+name+'</h4>'
                                                       html=html+'</th>' 
                                                       count = count+1
                         for i in range(count,4):
                              html=html+'<th style="width:25%"></th>'
                         html=html+'</tr>' 
                         html=html+'</table>' 
          return html
     else:
          return redirect("http://35.246.112.189:8080")

if __name__ == '__main__':
     app.secret_key = 'super secret key'
     app.run(host='0.0.0.0',port="8080")
