from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    DECIMAL,
    TEXT,
    DateTime
)
from datetime import datetime
# from app import db_sesssion, manager, Base
from app import db, manager
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
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    # def is_authenticated(self):
    #     return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True
    
    
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    # return db_sesssion.query(User).filter_by(id=user_id).one()

class Reviews(db.Model):
    
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key = True) 
    market_id = Column(Integer, db.ForeignKey('markets.id') , nullable=False)
    user_name = Column(TEXT, nullable=False)
    text = Column(TEXT, nullable=False)
    rating = Column(Integer, nullable=False)
    timestamp =  Column(DateTime, default=datetime.utcnow)
    