from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import request,session
from datetime import datetime
from wtforms import Form, StringField,PasswordField
from hastatakipsistemi import db

class Users(db.Model):
    __tablename__ = 'users'
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    userName = db.Column(db.String(120), unique=True, nullable=False)
    userPassword = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    numberofpatients = db.Column(db.Integer)

class Patients(db.Model):
    __tablename__ = 'patients'
    Id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    trackDate = db.Column(db.Date, default=datetime.today(), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=False)
    birthday = db.Column(db.Date, default=datetime.today(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    provienceId = db.Column(db.Integer, nullable=False)
    diagnosisName = db.Column(db.String(120), nullable=False)
    diagnosis = db.Column(db.String(9999), nullable=False)



class PatientRequest():
    def __init__(self,
     track, 
     name, 
     lastname, 
     phonenumber, 
     email, 
     birthday,
     gender, 
     diagnosis,
     diagnosisName,
     provienceId,
     ):
     self.track = self.request_form_get_date(track)
     self.name = self.request_form_get(name)
     self.lastname = self.request_form_get(lastname)
     self.phonenumber = self.request_form_get(phonenumber)
     self.email = self.request_form_get(email)
     self.birthday = self.request_form_get_date(birthday)
     self.age = datetime.today().year - self.birthday.year
     self.gender = self.request_form_get(gender)
     self.diagnosis = self.request_form_get(diagnosis)
     self.diagnosisName = self.request_form_get(diagnosisName)
     self.provienceId = self.request_form_get(provienceId)

    def request_form_get_date(self,tag):
        return datetime.strptime(request.form.get(tag), "%Y-%m-%d").date()

    def request_form_get(self,tag):
        return request.form.get(tag)


# Giriş Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

class SessionConfig():
    def __init__(self,logged_in,username,Id,email,name,lastname,numberofpatients):
        session["logged_in"] = logged_in
        session["username"] = username
        session["id"] = Id
        session["email"] = email
        session["name"] = name
        session["lastname"] = lastname
        session["numberofpatients"] = numberofpatients