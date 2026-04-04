from flask import Flask,render_template,jsonify,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import os
ist=pytz.timezone("Asia/Kolkata")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    marks=db.Column(db.Integer,nullable=False)
    date_created=db.Column(db.DateTime,default=lambda: datetime.now(ist))

    def __repr__(self)->str:
        return f"{self.id} - {self.name}"
app.secret_key="secret123"
@app.route('/')
def template():
    return render_template("index.html")
@app.route("/BACK")
def temp():
    return render_template("index.html")
@app.route("/ADD",methods=["GET","POST"])
def add_student():
    if request.method=="POST":
        print(request.method)
        name=request.form["name"]
        age=request.form["age"]
        marks=request.form["marks"]
        entry=Students(name=name,age=age,marks=marks)
        db.session.add(entry)
        db.session.commit()
        print(entry)
        flash("Record added successfully")
    return render_template("add.html")
@app.route("/READ")
def read1():
    k=Students.query.all()
    print(k)
    return render_template("read.html",student=k)
@app.route("/UPDATE")
def read2():
    k=Students.query.all()
    return render_template("update.html",student=k)
@app.route("/UPDATE/<int:ID>",methods=["POST","GET"])
def update(ID):
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        marks=request.form["marks"]
        k=Students.query.filter_by(id=ID).first()
        k.name=name
        k.age=age
        k.marks=marks
        db.session.commit()
        return redirect("/UPDATE")
    k=Students.query.filter_by(id=ID).first()
    return render_template("updaterecord.html",student=k)
@app.route("/DELETE")
def read3():
    k=Students.query.all()
    return render_template("delete.html",student=k)
@app.route("/DELETE/<int:ID>")
def delete(ID):
    entry=Students.query.filter_by(id=ID).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect("/DELETE")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)

