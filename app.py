from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route("/" , methods = ['GET','POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo = allTodo)

@app.route('/products')
def products():
    return "<h1>This is the products page</h1>"

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

@app.route('/edit/<int:sno>',methods = ['GET','POST'])
def edit(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    allTodo = Todo.query.all()
    if request.method == 'POST':
        todo.title = request.form['title']  
        todo.desc = request.form['desc']

        db.session.commit()   
        return redirect('/')

    return render_template('edit.html', todo=todo, allTodo = allTodo)


@app.route('/show')
def show():
    return "this is show page"

if __name__ == "__main__":
    app.run(debug=True)