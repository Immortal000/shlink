from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tmp/base.db'
app.config['SECRET_KEY']='dont guess this, this is a secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class URLS(db.Model): 
	id = db.Column(db.Integer,primary_key=True)
	url = db.Column(db.String(1024))
	short = db.Column(db.String(512))

@app.route('/')
def view():
	return render_template('index.html')
	
@app.route('/<url_id>')
def url_id(url_id):
	check_url = URLS.query.filter_by(short=url_id).first()
	if check_url: 
		return redirect(check_url.url)
	else:
		return "wrong page or page not registered"

@app.route('/',methods=['POST'])
def shorten(): 
	original_url = request.form['original_url']
	custom_url = request.form['custom_url']
	new_url = 'http://127.0.0.1:5000/'+custom_url
	n_url=URLS(url=original_url,short=custom_url)
	db.session.add(n_url)
	db.session.commit()
	return render_template('show.html',original_url=original_url,custom_url=custom_url,new_url=new_url)

if __name__ == '__main__':
	app.run(debug=True)



