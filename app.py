from flask import Flask
# from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from flask_migrate import Migrate, migrate
from flask_login import LoginManager
# from sqlalchemy.engine import result
# from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://ps_user:ps_password@ps_host:5432/db_name'
# app.SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config.from_object('config')

manager = LoginManager(app)
# Base = declarative_base()
# DATABASE_URL = "postgresql://postgres:Liverpool@localhost:5432/farmer_markets"
# engine = create_engine(DATABASE_URL)

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# db_sesssion = scoped_session(Session)

db = SQLAlchemy(app)
# db_sesssion = scoped_session(sessionmaker(bind=engine)) 




# def init_db():
#     # Здесь нужно импортировать все модули, где могут быть определены модели,
#     # которые необходимым образом могут зарегистрироваться в метаданных. 
#     # В противном случае их нужно будет импортировать до вызова init_db()
#     import  models
#     Base.metadata.create_all(bind=engine)



    

