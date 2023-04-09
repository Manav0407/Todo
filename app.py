from flask import Flask,request,redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)    
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db =SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"



@app.route('/',methods=['GET','POST'])
def first():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    # return "Hello world  my name is manav"
    allTodo=Todo.query.all()
    return render_template('imdex.html',allTodo=allTodo)

@app.route('/second')
def second():
    allTodo=Todo.query.all()
    # print(allTodo)
    # return "flask tutorial"

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    # allTodo=Todo.query.all()
    # print(allTodo)
    # return "flask tutorial"
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # print(allTodo)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", port=8080)