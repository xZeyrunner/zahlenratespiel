from random import randrange
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zahlen.db'
db = SQLAlchemy(app)
randomZahl = randrange(1, 100)
richtig = True
tiefer = True
hoeher = True

@app.route('/', methods=['GET', 'POST'])
def index():
    print(randomZahl)
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
        if(my_tasks):
            print(my_tasks[-1].content)
            if int(my_tasks[-1].content) == randomZahl:
                return render_template('index.html', tasks=my_tasks, richtig=richtig)
            elif int(my_tasks[-1].content) > randomZahl:
                return render_template('index.html', tasks=my_tasks, tiefer=tiefer)
            elif int(my_tasks[-1].content) < randomZahl:
                return render_template('index.html', tasks=my_tasks, hoeher=hoeher)
        else:
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