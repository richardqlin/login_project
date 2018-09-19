from flask import Flask
from flask import render_template,request,redirect,session,flash
import errorhandler
from flask_bootstrap import Bootstrap 
from flask_moment import Moment 
from datetime import datetime


from flask_pymongo import PyMongo 


#
app=Flask(__name__)

#app= Flask('UserAccount')

#app.config['MONGO_URI']='mongodb://localhost:27017/UserAccount'
app.config['MONGO_URI']='mongodb://richardqlin:linqiwei1@ds261302.mlab.com:61302/richardqlin'


mongo=PyMongo(app)

Bootstrap(app)

moment=Moment(app)
app.config['SECRET_KEY']='SomescreteText'

collection=mongo.db.AccountInformation



@app.route('/registration', methods=['POST','GET'])
def registration():
	
	return render_template('registration.html',current_time=datetime.utcnow())

@app.route('/registeruser', methods=['POST'])
def registeruser():
	global users
	first_name=request.form['first_name']
	last_name=request.form['last_name']
	email=request.form['email']
	password = request.form['password']
	users={}
	users={'first_name':first_name,'last_name':last_name,'email':email,'password':password}
	collection = mongo.db.AccountInformation
	#usersDetails={'firstName':'John','LastName':'Smith','email':'john.Smith@email.com','password':'123'}
	#print users
	collection.insert(users)
	flash('User already registered')
	return redirect('login')
	#return 'Name: {first_name} {last_name} and Email {email}'.format(first_name=first_name,last_name=last_name,email=email)

@app.route('/login',methods=['GET','POST'])
def login():
	return render_template('login.html',current_time=datetime.utcnow())

@app.route('/loginuser',methods=['GET', 'POST'])

def loginuser():
	#global users
	email=request.form['email']
	password=request.form['password']
	collection = mongo.db.AccountInformation
	user = collection.find_one({'email': email})
	
	user['_id'] =str(user['_id'])

	if email !=user['email']:
		return redirect('/invalid')
		#return '<h1> this email id is not registered with us</h1>'

	elif user['password']==password:
		session['user']=user
		print user
		return redirect('/home')
		#return '<h1> this email id and password combination is correct</h1>'
	else:
		flash('incorrect password, try it again!')
		return redirect('/login')
		#return '<h1> this email id and password combination is incorrect</h1>'

@app.route('/invalid')
def invalid():
	return render_template('invalid.html',current_time=datetime.utcnow())

@app.route('/home')
def home():
	if 'user' not in session:
		return redirect('/login')
	user = session['user']
	first_name=user['first_name']

	'''
	collection = mongo.db.AccountInformation
	user = collection.find_one({'email': email})
	print('user=',user['email'])
	first_name=user['email']
	'''
	return render_template('home.html',current_time=datetime.utcnow(),first_name=first_name)

@app.route('/')
def index():
	flash('hello user')
	return render_template('index.html',current_time=datetime.utcnow())

@app.route('/logout',methods=['GET','POST'])
def logout():
	del session['user']
	return redirect('/login')


@app.route('/listall')
def all():
	collection = mongo.db.AccountInformation
	user = [x for x in collection.find({})]
	return render_template('listall.html',user=user) 

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error404.html',error=e),404
@app.errorhandler(400)
def page_not_found(e):
	return render_template('error400.html',error=e),400

@app.errorhandler(500)
def page_not_found(e):
	return render_template('error500.html',error=e),500

if __name__ == '__main__':
	app.run(debug=True)