fimport os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    database_name ='local_db_name'
    default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    
class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    release_date = Column(db.DateTime)
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()

#################################################
# Database Setup
#################################################


# engine = create_engine('DATABASE_URL', echo = False) 

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Data_clu= Base.classes.clusterA
Data_elb= Base.classes.elbow
Data_lin=Base.classes.line
Data_linreg=Base.classes.linreg

# connection.close()
# session = Session(engine)


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
  
    
    return render_template("index.html")

@app.route("/unsup")
def unsup():
      
    return render_template("index1.html")
    
@app.route("/linear")
def linear():
     
    return render_template("index2.html")

# @app.route("/updatedata")
# def newdata():
   
#     data1, df_elbow = ml_script.cluster_info(data_base)
#     data3, data5 = ml_script.cluster_info(data_base)

#     engine = create_engine('DATABASE_URL', echo = False) 
#     connection = engine.connect()
    
#     data1.to_sql('clusterA',  if_exists='replace', index=True, con=connection, method='multi')
#     connection.execute('ALTER TABLE "clusterA" ADD PRIMARY KEY ("index");')

#     df_elbow.to_sql('elbow',  if_exists='replace', index=True, con=connection, method='multi')
#     connection.execute('ALTER TABLE "elbow" ADD PRIMARY KEY ("index");')
    
#     data3.to_sql('line', if_exists='replace', index=True, con=connection, method='multi')
#     connection.execute('ALTER TABLE "line" ADD PRIMARY KEY ("index");')
    
#     data5.to_sql('linreg', if_exists='replace', index=True, con=connection, method='multi')
#     connection.execute('ALTER TABLE "linreg" ADD PRIMARY KEY ("index");')
    
    
    
#     return home()

@app.route("/api/cluster")
def cluster():
      session = Session(engine)
      x = []
      y = []
      c2 =[]
      c3 =[]
      c4 =[]
      c6 =[]
      price = []
      livingArea = []

      results = session.query(Data_clu)
      for value in results:
          x.append(value.x)
          y.append(value.y)
          c2.append(value.c2)
          c3.append(value.c3)
          c4.append(value.c4)
          c6.append(value.c6)
          price.append(value.price)
          livingArea.append(value.livingArea)
    
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
      session.close()
      return jsonify(cluster_data)

@app.route("/api/elbow")
def inertia():
      session = Session(engine)
      results3 = session.query(Data_elb)
      k = []
      inertia = []
      
      for value in results3:
          k.append(value.k)
          inertia.append(value.inertia)
       
    
      elbow_data = {
      "k": k,
      "Inertia": inertia
                }
      session.close()
      return jsonify(elbow_data)




@app.route("/api/linear")
def linearapi():
      session = Session(engine)
      price = []
      livingarea = []
      yearbuilt = []
      familyincome = []
    #   bathrooms = []
    #   bedrooms = []

      results = session.query(Data_lin)
      for value in results:
          price.append(value.price)
          livingarea.append(value.livingArea)
          yearbuilt.append(value.yearBuilt)
          familyincome.append(value.family_income)
        #   familyincome.append(value.MarriedFamilyIncome)
      
    
      linear_data = {
      "price": price,
      "livingarea": livingarea,
      "yearbuilt": yearbuilt,
      "familyincome":familyincome,
              }
      session.close()
      return jsonify(linear_data)     


@app.route("/api/linreg")
def reg():
      session = Session(engine)
      livingarea = []
      bathrooms = []
      price = []
      pred_la_price = []
      pred_ba_price = []

      results = session.query(Data_linreg)
      for value in results:
          livingarea.append(value.livingArea)
          bathrooms.append(value.bathrooms)
          price.append(value.price)
          pred_la_price.append(value.pred_la_price)
          pred_ba_price.append(value.pred_bath_price)
      
      linreg_data = {
      "livingarea":livingarea,
      "bathrooms":bathrooms,
      "price":price,
      "pred_la_price":pred_la_price,
      "pred_ba_price":pred_ba_price,
              }
      session.close()
      return jsonify(linreg_data)     


if __name__ == "__main__":
    app.run(debug=True)
