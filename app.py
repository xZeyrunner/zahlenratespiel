from pickle import NONE
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zahlen.db'
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_number = request.form['number']
        new_number = int(new_number)
        if(new_number != ""):
            t = Task(content=new_number)
            db.session.add(t)
            db.session.commit() 
        return redirect('/')
    else:
        my_tasks = Task.query.all()
        return render_template('index.html', tasks=my_tasks)

@app.route('/delete/<int:id>')  #
def delete(id):                 #
    t = Task.query.get(id)      #
    db.session.delete(t)        #
    db.session.commit()         #
    return redirect('/')        #
    
# models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer)
    
db.create_all()