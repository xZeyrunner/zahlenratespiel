from random import randrange
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zahlen.db'
db = SQLAlchemy(app)
randomZahl = randrange(0, 100)
richtig = True
tiefer = True
hoeher = True
versuche = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global gueltigeZahl
    if request.method == 'POST':
        new_number = request.form['number']
        if new_number != "":
            new_number = int(new_number)
            if new_number <= 100 and new_number >= 0:
                t = Task(content=new_number)
                db.session.add(t)
                db.session.commit()
        return redirect('/')
    else:
        my_tasks = Task.query.all()
        if(my_tasks):
            versuche = len(my_tasks)
            aktuelleZahl = my_tasks[-1].content
            if int(my_tasks[-1].content) == randomZahl:
                return render_template('index.html', tasks=my_tasks, richtig=richtig, aktuelleZahl=aktuelleZahl, versuche=versuche)
            elif int(my_tasks[-1].content) > randomZahl:
                return render_template('index.html', tasks=my_tasks, tiefer=tiefer, aktuelleZahl=aktuelleZahl, versuche=versuche)
            elif int(my_tasks[-1].content) < randomZahl:
                return render_template('index.html', tasks=my_tasks, hoeher=hoeher, aktuelleZahl=aktuelleZahl, versuche=versuche)
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