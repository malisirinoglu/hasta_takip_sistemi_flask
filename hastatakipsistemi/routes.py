import os
from flask import render_template, flash, redirect, url_for, session, request
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from flask_ckeditor import upload_success, upload_fail
from flask.helpers import send_from_directory

from hastatakipsistemi import app,db
from hastatakipsistemi.models import PatientRequest,SessionConfig,Users,Patients,LoginForm
from hastatakipsistemi.functions import average_age_func,number_of_provience

server_url = "127.0.0.1:5000"
# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Önce sisteme giriş yapmanız gerekmektedir.", "danger")
            return redirect(url_for("login"))
    return decorated_function

# Ana Sayfa
@app.route("/")
@login_required
def index():
    result = db.engine.execute(
        'SELECT provienceId,COUNT(provienceId)FROM patients WHERE userId = {} GROUP BY provienceId;'.format(session['id']))
    provience = number_of_provience(result)

    return render_template("index.html", provience=provience)

# Giriş Sayfası
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('logged_in') == True:
        flash("Zaten Giriş Yaptınız.", "danger")
        return redirect(url_for("index"))
    else:
        form = LoginForm(request.form)
        if request.method == "POST":
            username = form.username.data
            password_entered = form.password.data
            user = Users.query.filter_by(userName=username).first()
            if user:
                real_password = user.userPassword
                if sha256_crypt.verify(password_entered, real_password):
                    flash(
                        "UYARI! Programı kapatmadan önce lütfen çıkış yapınız.", "danger")
                    flash("Başarıyla Giriş Yaptınız...", "success")
                    SessionConfig(
                        logged_in= True,
                        username = username,
                        Id = user.Id,
                        email=user.email,
                        name=user.name,
                        lastname=user.lastname,
                        numberofpatients=user.numberofpatients)
                    return redirect(url_for("index"))
                else:
                    flash("Kullanıcı Adını Kontrol Ediniz.", "danger")
                    return redirect(url_for("login"))

            else:
                flash("Parolanızı Kontrol Ediniz.", "danger")
                return redirect(url_for("login"))

        return render_template("login.html", form=form)

# Çıkış İşlemi
@app.route("/logout",)
def logout():
    session.clear()
    flash("Başarıyla Çıkış Yaptınız...", "success")
    return redirect(url_for("index"))


# Hastaları görüntüleme
@app.route("/patients/<string:id>")
@login_required
def patients(id):
    patients = Patients.query.filter_by(
        userId=session["id"], provienceId=id).all()
    return render_template("patients.html", patients=patients, id=id)

# Hasta Ekleme İl Bazında
@app.route("/patients/<string:id>/add-patient")
@login_required
def add_patient(id):
    today = datetime.today()
    return render_template("add-patient.html", patients=patients, id=id, today=today)

# Hasta Ekleme Kontrol Paneli
@app.route("/add-patient")
@login_required
def add_patient_dashboard():
    today = datetime.today()
    return render_template("add-patient.html", today=today)

# Hasta Ekleme Genel
@app.route("/add", methods=['POST'])
@login_required
def add():
    patientrequest = PatientRequest(
        track="track",
        name="name",
        lastname="lastname",
        phonenumber="phonenumber",
        email="email",
        birthday="birthday",
        gender="gender",
        diagnosis="content",
        diagnosisName="diagnosisName",
        provienceId="id",
        )
    userId = session["id"]
    
    newPatient = Patients(
        userId=userId,
        trackDate=patientrequest.track,
        name=patientrequest.name,
        lastname=patientrequest.lastname,
        phonenumber=patientrequest.phonenumber,
        email=patientrequest.email,
        birthday=patientrequest.birthday,
        age=patientrequest.age,
        gender=patientrequest.gender,
        provienceId=patientrequest.provienceId,
        diagnosisName=patientrequest.diagnosisName,
        diagnosis=patientrequest.diagnosis,
    )
    db.session.add(newPatient)
    db.session.commit()
    return redirect(url_for("patients", id=patientrequest.provienceId))



# Kontrol Paneli
@app.route("/dashboard")
@login_required
def dashboard():
    patients = Patients.query.filter_by(userId=session['id']).all()
    if patients != []:
        average_age = average_age_func(patients)
    else:
        average_age = 0

    return render_template("dashboard.html", patients=patients, average_age=average_age)

# Hasta Silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    patient = Patients.query.filter_by(userId=session['id'],Id=id).first()
    if patient != None:
        db.session.delete(patient)
        db.session.commit()
        flash("Hasta Başarıyla Silindi", "success")
    else:
        flash("Böyle bir hasta yok veya bu işleme yetkiniz yok", "danger")
    return redirect(url_for("dashboard"))

# Hasta Detay Sayfası
@app.route("/patients/<string:id>/<string:patientid>", methods=["GET"])
@login_required
def detail(id, patientid):
    patient = Patients.query.filter_by(Id=patientid).first()
    return render_template("detail.html", patient=patient)

# Hasta Güncelleme Sayfası
@app.route("/edit/<string:id>", methods=["GET", "POST"])
@login_required
def update(id):
    patients = Patients.query.filter_by(userId=session['id'],Id=id).first()
    if request.method == "GET": 
        if patients != None:
            return render_template("update.html", 
            id=id, 
            trackDate=patients.trackDate, 
            name=patients.name, 
            lastname=patients.lastname, 
            phonenumber=patients.phonenumber, 
            email=patients.email, 
            birthday=patients.birthday, 
            age=patients.age, 
            gender=patients.gender, 
            provienceId=patients.provienceId, 
            diagnosisName=patients.diagnosisName, 
            diagnosis=patients.diagnosis)
        else:
            flash("Böyle bir hasta yok veya bu işleme yetkiniz yok", "danger")
            return redirect(url_for("index"))
    else:
        patientrequest = PatientRequest(
        track="track",
        name="name",
        lastname="lastname",
        phonenumber="phonenumber",
        email="email",
        birthday="birthday",
        gender="gender",
        diagnosis="content",
        diagnosisName="diagnosisName",
        provienceId="id",
        )
        patients.trackDate = patientrequest.track
        patients.name = patientrequest.name
        patients.lastname = patientrequest.lastname
        patients.phonenumber = patientrequest.phonenumber
        patients.email = patientrequest.email
        patients.birthday = patientrequest.birthday
        patients.age = patientrequest.age
        patients.diagnosis = patientrequest.diagnosis
        patients.diagnosisName = patientrequest.diagnosisName
        patients.provienceId = patientrequest.provienceId
        patients.gender = patientrequest.gender
        db.session.commit()
        flash("Hasta Başarıyla Güncellendi.", "success")
        return render_template("detail.html", patient=patients)

# Arama Özelliği
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":

        patients = Patients.query.filter_by(userId=session['id']).all()
        if patients != []:
            average_age = average_age_func(patients)
        else:
            average_age = 0
        keyword = request.form.get("keyword")
        select = request.form.get("select")
        result = db.engine.execute(
            "SELECT * from patients where userId = {} and {} like '".format(session["id"], select) + keyword + "%'")
        print("SELECT * from patients where userId = {} and {} like ".format(
            session["id"], select) + keyword + "%'")
        # ... :(
        liste = []
        for a in result:
            liste.append(a)
        if liste != []:
            result = db.engine.execute(
                "SELECT * from patients where userId = {} and {} like '%".format(session["id"], select) + keyword + "%'")
            return render_template("search-dashboard.html", result=result, patients=patients, average_age=average_age, keyword=keyword, select=select)
        else:
            flash("Aranan Kriterlere Göre Hasta Bulunamadı", "danger")
            return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("index"))


#Localde Sunucu Kapatma
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    flash("UYARI!", "danger")
    return render_template("shutdown.html")

#İsme Göre Profil Sayfası Gösterme
@app.route('/<string:profile>', methods=['GET'])
def profile(profile):
    if profile == session["username"]:
        user = Users.query.filter_by(userName=profile).first()
        return render_template('profile.html', user=user)
    else:
        flash("Böyle bir kullanıcı yok veya buna yetkiniz yok", "danger")
        return redirect(url_for("index"))
    return redirect(url_for("index"))


# Dosya Upload
@app.route('/files/<string:username>/<path:filename>')
@login_required
def uploaded_files(username,filename):
    path = "static/file/{}".format(username)
    return send_from_directory(path, filename)

#Dosya Upload
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Lütfen sadece resim yükleyiniz.(jpg, gif, png, jpeg)')
    try:
        f.save(os.path.join("hastatakipsistemi/static/file/{}".format(session["username"]), f.filename))
    except:
        os.mkdir("hastatakipsistemi/static/file/{}".format(session["username"]))
        f.save(os.path.join("hastatakipsistemi/static/file/{}".format(session["username"]), f.filename))
    
    url_for('uploaded_files', username = session["username"], filename=f.filename)
    # return upload_success call
    return upload_success('http://{}/files/{}/{}'.format(server_url,session["username"],f.filename))