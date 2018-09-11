from flask import Flask
from flask import render_template,request
app= Flask(__name__)

@app.route('/', methods=['POST','GET'])

def registration():

	return render_template('registration.html')

@app.route('/registeruser', methods=['POST'])
def registeruser():
	first_name=request.form['first_name']
	last_name=request.form['last_name']
	email=request.form['email']
	password = request.form['password']

	return 'Name: {first_name} {last_name} and Email {email}'.format(first_name=first_name,last_name=last_name,email=email)


if __name__ == '__main__':
	app.run(debug=True)