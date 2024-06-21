from flask import  render_template, request, redirect, url_for, flash 
from werkzeug.security import  generate_password_hash, check_password_hash 
import zip_model_db as model  

from app import app, db 
from models import Market, User, Reviews

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)


@app.route('/', methods=['GET'])
def hello_user():
    return render_template('index.html')

 
@app.route("/markets/", defaults={'page': 1}, methods=["GET", "POST"])
@app.route('/markets/<int:page>', methods=["GET", "POST"])
def showMarkets(page = 1):
    
    per_page = 10  # Number of items per page

    markets = Market.query.order_by(Market.name).paginate(page =page, per_page=per_page)

   

    return render_template('markets.html', markets=markets)

# Эта функция позволит создать новую книгу и сохранить ее в базе данных.  
@app.route('/markets/new/', methods=['GET', 'POST'])  
def newMarket():  
    if request.method == 'POST':  
        newMarket = Market(name=request.form['name'], city=request.form['city'], street =request.form['street'], country =request.form['country'],
                         lat=request.form['lat'], lon=request.form['lon'], state =request.form['state'], zip_code =request.form['zip_code'] ) 
                           
        db.session.add(newMarket)  
        db.session.commit()  
        return redirect(url_for('showMarkets'))  
    else:  
        return render_template('newMarket.html')  
  
  
# Эта функция позволит нам обновить книги и сохранить их в базе данных.  
@app.route("/markets/<int:markets_id>/edit/", methods=['GET', 'POST'])  
def editMarket(markets_id):  
    # editedMarket = db.sesssion.query(Market).filter_by(id=markets_id).one
    editedMarket = Market.query.filter_by(id=markets_id).one()    
    if request.method == 'POST':  
        if request.form['name']:  
            editedMarket.name = request.form['name']  
            db.session.commit()  
            return redirect(url_for('showMarkets'))  
    else:  
        return render_template('editMarket.html', market= editedMarket)  
  
  
# Эта функция для удаления книг  
@app.route('/markets/<int:markets_id>/delete/', methods=['GET', 'POST'])  
def deleteMarket(markets_id):  
    # marketToDelete = db.sesssion.query(Market).filter_by(id=markets_id).one()  
    marketToDelete = Market.query.filter_by(id=markets_id).one()  
    if request.method == 'POST':  
        db.session.delete(marketToDelete)  
        db.session.commit()  
        return redirect(url_for('showMarkets', markets_id= markets_id)) 
    else:  
        return render_template('deleteMarket.html', market=marketToDelete)  
  
 
@app.route('/loc_by_zip', methods=['GET', 'POST'])
def location_by_zip():
    message = ''
    zip_code = ''
    if request.method == 'POST':
        zip_code = request.form['zip-input']
        message = model.location_by_zip(zip_code)
        # message = db.session.query(Market).filter_by(Market.zip_code.like("%zip_code"), zip_code).all()
        return render_template('loc_by_zip.html', zip_code=zip_code, message=message)
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('psw')
   

    if login and password:
        user = User.query.filter_by(login=login).first()
        # user = db.sesssion.query(User).filter_by(login=login).first()
        if user and check_password_hash(user.psw, password):
            login_user(user)

            next_page = request.args.get('next')
         
            return redirect(next_page or url_for('hello_user'))
            # return redirect(url_for('showMarkets'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('psw')
    password2 = request.form.get('psw2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, email=email, psw=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    print('hello_user')
    return redirect(url_for('hello_user'))


@app.after_request
def redirect_to_signin(response):
    
    if response.status_code == 401:
        print('login_page')
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response

@app.route('/market/<int:markets_id>/review', methods=['POST'])
@login_required
def create_review(markets_id):
    # if request.method == 'POST':
        review_text = request.form['review_text']
        rating = int(request.form['rating'])

        new_reviews = Reviews(market_id = markets_id, text = review_text,
                               rating = rating, user_name = current_user.login)
       
        db.session.add(new_reviews)
        db.session.commit()

        # return redirect(url_for('showMarkets', markets_id= markets_id)) 
        return redirect(f'/markets/{markets_id}/edit/')
    # return render_template('create_review.html',markets_id = markets_id)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form['location']
        markets = Market.query.filter(
            (Market.city.ilike(f'%{location}%')) |
            (Market.state.ilike(f'%{location}%')) |
            (Market.zip_code.ilike(f'%{location}%'))
        ).all()
        return render_template('search.html', markets=markets)
    return render_template('search.html') 

    
if __name__ == '__main__':  
    # app.debug = True  
    app.run(port=4996)