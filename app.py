from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for session
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)  # identifies the user
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.before_request
def set_user():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # unique id per visitor


@app.route("/", methods=['GET','POST'])
def hello_world():
    user_id = session['user_id']
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc, user_id=user_id)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.filter_by(user_id=user_id).all()  # only this user's todos
    return render_template('index.html', allTodo=allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    user_id = session['user_id']
    todo = Todo.query.filter_by(sno=sno, user_id=user_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")


@app.route('/edit/<int:sno>', methods=['GET','POST'])
def edit(sno):
    user_id = session['user_id']
    todo = Todo.query.filter_by(sno=sno, user_id=user_id).first()
    if not todo:
        return redirect("/")

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')

    return render_template('edit.html', todo=todo)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)