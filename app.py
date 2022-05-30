from flask import Flask, render_template, jsonify, redirect
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# from config import p_key
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
import ml_script

#################################################
# Running Machine Learning Script - Returning Tables
#################################################

data_base = ml_script.data_info()
data1, df_elbow = ml_script.cluster_info(data_base)
data3, data5 = ml_script.line_info(data_base)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# default_database_path= f'postgresql://postgres:{p_key}@localhost:5432/housing3'
# database_path = os.getenv('DATABASE_URL', default_database_path)

# database_path = os.environ['DATABASE_URL']
# app.config["SQLALCHEMY_DATABASE_URI"] = database_path
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app) 

# db.create_all()
# # Remove tracking modifications
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# Pet = create_classes(db)



#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///housing.db', echo=False)

#################################################
# INITIAL RUN ONLY - create database tables
#################################################

# connection = engine.connect()
# data1.to_sql('clusterA',  if_exists='replace', index=False, con=connection)
# df_elbow.to_sql('elbow',  if_exists='replace', index=False, con=connection)
# data3.to_sql('line', if_exists='replace', index=False, con=connection)
# data5.to_sql('linreg', if_exists='replace', index=False, con=connection)
# connection.close()


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
  
    
 return render_template("index.html")

@app.route("/load")
def load():
  connection = engine.connect()
  data1.to_sql('clusterA',  if_exists='replace', index=False, con=connection)
  df_elbow.to_sql('elbow',  if_exists='replace', index=False, con=connection)
  data3.to_sql('line', if_exists='replace', index=False, con=connection)
  data5.to_sql('linreg', if_exists='replace', index=False, con=connection)
  connection.close()
  return redirect("/", code=302)

@app.route("/unsup")
def unsup():
      
  return render_template("index1.html")
    
@app.route("/linear")
def linear():
     
  return render_template("index2.html")


@app.route("/api/cluster")
def cluster():
  connection = engine.connect()
  data1_df = pd.read_sql_table("clusterA", con = connection)
  x = [result for result in data1_df["x"]]
  y = [result for result in data1_df["y"]]
  c2 = [result for result in data1_df["c2"]]
  c3 = [result for result in data1_df["c3"]]
  c4 = [result for result in data1_df["c4"]]
  c6 = [result for result in data1_df["c6"]]
  price= [result for result in data1_df["price"]]
  livingArea = [result for result in data1_df["livingArea"]]    
  connection.close()    
    
  cluster_data = {
      "cluster2":{
        "x": x,
        "y": y,
        "c": c2,
        "price":price,
        "living_area":livingArea,
        "clusters":c2,
      },
      "cluster3":{
        "x": x,
        "y": y,
        "c": c3,
        "price":price,
        "living_area":livingArea,
        "clusters":c3,
      },
      "cluster4":{
        "x": x,
        "y": y,
        "c": c4,
        "price":price,
        "living_area":livingArea,
        "clusters":c4,
      },
      "cluster6":{
        "x": x,
        "y": y,
        "c": c6,
        "price":price,
        "living_area":livingArea,
        "clusters":c6,
      }
          }
  # session.close()
  return jsonify(cluster_data)

@app.route("/api/elbow")
def inertia():

  connection = engine.connect()
  data_elbow = pd.read_sql_table("elbow", con = connection)
  k = [result for result in data_elbow["k"]]
  inertia = [result for result in data_elbow["inertia"]]
  connection.close()    

  elbow_data = {"k": k,"Inertia": inertia}

  return jsonify(elbow_data)


@app.route("/api/linear")
def linearapi():
  connection = engine.connect()
  data3_df = pd.read_sql_table("line", con = connection)
  price = [result for result in data3_df["price"]]
  livingarea = [result for result in data3_df["livingArea"]]
  yearbuilt = [result for result in data3_df["yearBuilt"]]
  familyincome = [result for result in data3_df["family_income"]]
  connection.close() 

  linear_data = {
  "price": price,
  "livingarea": livingarea,
  "yearbuilt": yearbuilt,
  "familyincome":familyincome,
          }
  
  return jsonify(linear_data)     


@app.route("/api/linreg")
def reg():
  connection = engine.connect()
  data5_df = pd.read_sql_table("linreg", con = connection)
  price = [result for result in data5_df["price"]]
  livingarea = [result for result in data5_df["livingArea"]]
  bathrooms = [result for result in data5_df["bathrooms"]]
  pred_la_price = [result for result in data5_df["pred_la_price"]]
  pred_ba_price = [result for result in data5_df["pred_bath_price"]]
  connection.close() 

  linreg_data = {
  "livingarea":livingarea,
  "bathrooms":bathrooms,
  "price":price,
  "pred_la_price":pred_la_price,
  "pred_ba_price":pred_ba_price,
          }

  return jsonify(linreg_data)     


if __name__ == "__main__":
    app.run(debug=True)
