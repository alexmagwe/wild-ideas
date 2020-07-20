from flask import Flask,render_template,url_for,request,jsonify
import os

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from .config import configs
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
app=Flask(__name__)
app.config.from_object(configs['production'])
db=SQLAlchemy(app)
admin=Admin(app)
from flask_sslify import SSLify
if app.config['SSL_REDIRECT']:
    sslify=SSLify(app)
socketio=SocketIO(sslify)
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

class Lessons(db.Model):
    id=db.Column(db.Integer,primary_key=True,index=True)
    lesson=db.Column(db.String(100),nullable=False)
    date=db.Column(db.String(10),index=True,nullable=False)
    def __repr__(self):
        return f"lesson:{self.lesson},date:{self.date}"
    def to_json(self):
        json_lessons={
                'lesson':self.lesson,
                'date':self.date
                }
        return json_lessons
if app.debug:
    admin.add_view(ModelView(Lessons,db.session))

@app.route('/',methods=['GET','POST'])
def home():    
    return render_template('index.html')

def get_time():
    date=datetime.now()
    yr,mnth,day=date.year,date.month,date.day
    date=f"{day}/{mnth}/{yr}"
    return date

    
@socketio.on('request')
def handle_custom_event(data,methods=['GET','POST']):
    if data.get('data')=='query_lessons':
        lessons=Lessons.query.all()
        msg={"lessons":[lesson.to_json() for lesson in lessons]}
        print('data:',msg)
        socketio.emit('receive',msg)
    elif data.get('lesson') is not None:
        pydate=(get_time())
        data['date']=pydate
        socketio.emit('receive',data)
        print('new lesson',data)
        success(data)
def success(data):
    lesson=Lessons(date=data.get('date'),lesson=data.get('lesson'))
    db.session.add(lesson)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    

