import psycopg2 
from getpass import getpass
# from subprocess import Popen, PIPE, STDOUT
# import webbrowser
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    # Date,
    String,
    DECIMAL,
    TEXT,
    DateTime
)


ps_host = input('Enter the IP address or DNS name of your Postgres instance: ')
ps_user = input('Enter the username of your Postgres instance: ')
ps_password = input('Enter the password for user on your Postgres instance: ')
db_name = input(f'Enter the name of the database to be created on your Postgres instance: ')
ps_port = 5432

if input('Full deploymelnt? [y/n]') == 'y':

  # POSTGRES_USER : str = os.getenv("POSTGRES_USER")
  #   POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
  #   POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")

    # POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URL = f"postgresql://{ps_user}:{ps_password}@{ps_host}:{ps_port}/{db_name}"  
    app = Flask(__name__)
    app.secret_key = 'some secret salt'
    # app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:Liverpool@localhost:5432/farmer_markets'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# app.SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

conn = psycopg2.connect(user=ps_user,password=ps_password,host=ps_host,port='5432') 

conn.autocommit = True
cursor = conn.cursor() 


class Market(db.Model):
       
    __tablename__ = 'markets'
    
    id = Column(Integer, primary_key = True) 
    name = Column(TEXT) 
    lat = Column(DECIMAL(9,6))
    lon = Column(DECIMAL(9,6))
    wic = Column(TEXT) 
    street = Column(TEXT) 
    city = Column(TEXT) 
    country = Column(TEXT) 
    state = Column(TEXT) 
    zip_code = Column(String(10)) 
    reviews = db.relationship('Reviews', backref='market', lazy='dynamic')
    

class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True) 
    login = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique = True, nullable=False) 
    psw = Column(String(255), nullable = True) 
    date = Column(DateTime, default=datetime.utcnow)
    
   
class Reviews(db.Model):
    
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key = True) 
    market_id = Column(Integer, db.ForeignKey('markets.id') , nullable=False)
    user_name = Column(TEXT, nullable=False)
    text = Column(TEXT, nullable=False)
    rating = Column(Integer, nullable=False)
    timestamp =  Column(DateTime, default=datetime.utcnow)
    
    # with connect(
    #     host=host,
    #     user=user,
    #     password=password,
    # ) as connection:
    #     with connection.cursor() as cursor:
try:
    cursor.execute(f'CREATE DATABASE {db_name}')
except psycopg2.DatabaseError as err:
    if err.msg == f"Can't create database '{db_name}'; database exists":
        if input(f'Database {db_name} already exists. Do you want to drop it [y/n]? ') == 'y':
                        cursor.execute(f'DROP DATABASE {db_name}')
                        cursor.execute(f'CREATE DATABASE {db_name}')
          
with open('app_deployment.py', 'r') as inp, open('app.py', 'w') as outp:
        for line in inp:
            line = line.replace("ps_user", f"{ps_user}") \
                .replace("ps_password", f"{ps_password}") \
                .replace("ps_host", f"{ps_host}") \
                .replace("db_name", f"{db_name}")
            outp.write(line)


conn.commit() 
conn.close()
# with open('test.log','wb') as out, open('test-error.log','wb') as err:
#     p = Popen(['python', 'airports_deployed.py'], stdout=out, stderr=err)
               
app.app_context().push()
db.create_all()

conn = psycopg2.connect(database=db_name,user=ps_user,password=ps_password,host=ps_host,port='5432') 

conn.autocommit = True
cursor = conn.cursor() 

sql2 = '''COPY markets(id,name,lat,lon,WIC,street,city,country,State,zip_code) 
FROM 'D:\\markets\\markets\\markets.csv
DELIMITER ',' 
CSV HEADER;'''

  
cursor.execute(sql2) 
  
 
conn.commit() 
conn.close()
                
