from flask import Flask,render_template,url_for,request,jsonify
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from .config import configs
from flask_admin import Admin
from flask_sslify import SSLify
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
app=Flask(__name__)
app.config.from_object(configs['production'])
db=SQLAlchemy(app)
migrate = Migrate(app, db)
admin=Admin(app)

if app.config['SSL_REDIRECT']:
    sslify=SSLify(app)
if not app.debug and not app.testing:
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/progress.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Progress')

class Ideas(db.Model):
    __tablename__='ideas'
    id=db.Column(db.Integer,primary_key=True,index=True)
    title =db.Column(db.String(100),nullable=False,index=True)
    description=db.Column(db.Text(),nullable=False)
    date=db.Column(db.String(10),index=True,nullable=False)
    def __repr__(self):
        return f"idea:{self.idea},date:{self.date}"
    def to_json(self):
        json_ideas={
                'id':self.id,
                'title':self.title,
                'description':self.description,
                'date':self.date
                }
        return json_ideas
if app.debug:
    admin.add_view(ModelView(Ideas,db.session))

##routes
@app.route('/',methods=['GET','POST'])
def home():    
    return render_template('index.html')

@app.route('/add',methods=['GET'])
def add_ideas():    
    return render_template('add_idea.html')

@app.route('/idea/<int:id>',methods=['GET'])
def idea(id):
    print(id)   
    idea=Ideas.query.get(id) 
    return render_template('idea.html',idea=idea)

def get_time():
    date=datetime.now()
    yr,mnth,day=date.year,date.month,date.day
    date=f"{day}/{mnth}/{yr}"
    return date

@app.route('/ideas',methods=['GET','POST'])
def ideas():
    ideas=Ideas.query.all()
    resp=jsonify([idea.to_json() for idea in ideas])
    print('data:',resp)
    return resp,200

@app.route('/add/idea',methods=['POST'])
def add():
    data=request.json
    title=data.get('title')
    desc=data.get('description')
    date=get_time() 
    if title and desc: 
        idea=Ideas(title=title,description=desc,date=date)  
        db.session.add(idea)
        try:
            db.session.commit()
            return {'success':'added succesfully'},200
        except:
            db.session.rollback()
            return {'error':sys.exc_info()[0]},500
    return {'error':'missing data'},400
        

