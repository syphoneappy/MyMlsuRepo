from flask import Flask, render_template , flash,request,session,abort,redirect,url_for,current_app,Markup
from flask_materialize import Material
from flask_login import logout_user,login_manager
from pymysql import *
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pandas.io.sql as sql
import yaml,xlwt,re,os,time,base64,io,secrets
import PIL.Image
app = Flask(__name__)
app.secret_key = 'This'
#-----------------------------database connection-----------

db = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] =  db['mysql_host']
app.config["MYSQL_USER"] =  db['mysql_user']
app.config["MYSQL_PASSWORD"] =  db['mysql_password']
app.config["MYSQL_DB"] =  db['mysql_db']
app.config["SERVER_NAME"] = 'localhost:8000'
UPLOAD_FOLDER = './static/images'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
MySQL = MySQL(app)

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'static/images',photo_name)
    photo.save(file_path)
    return photo_name
def assignment(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'/python practice/MyMlsuRepo/MLSU/Teacher/static/assign',photo_name)
    photo.save(file_path)
    return photo_name
def image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'/python practice/MyMlsuRepo/MLSU/Student/static/post',photo_name)
    photo.save(file_path)
    return photo_name
@app.route("/", methods=['GET','POST'])
def index():
        seconds = 3
        for i in range(seconds):
            times = print(str(seconds - i) + "seconds remain")
            time.sleep(1)
        return render_template('Loding.html')
@app.route('/test',methods=['GET','POST'])
def LogIn():
    msg = ''
    if request.method == 'POST' and 'Id' in request.form and 'password' in request.form:
        userDetails = request.form
        RollNo = userDetails['Id']
        password = userDetails['password']
        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM studentd Where (RollNo = %s OR Email = %s) AND Password=%s',(RollNo,RollNo,password))
        accounts = cursor.fetchone()
        if accounts:
            session['loggedin'] = True
            session['RollNo'] = accounts['RollNo']
            session['Name'] = accounts['Name']
            session['Email'] = accounts['Email']
            session['image'] = accounts['image']
            session['CourseId'] = accounts['CourseId']
            session['Bio'] = accounts['Bio']
            if session['image'] == '':
                return render_template('FormFill.html',Email = session['Email'])
            else:
                return redirect('/Homes')
        else:
            msg = 'Incorrect username or password!'
    conn = MySQL.connection.cursor()
    conn.execute("Select * from notification Order by Nid DESC")
    data = conn.fetchall()
    conn.close()
    return render_template('LogIn.html',msg = msg,data = data)
@app.route("/Homes",methods=['GET','POST'])
def Homes():
    cur = MySQL.connection.cursor()
    cur.execute("select * from courseid where Course = '%s' ORDER BY Id DESC"%(session['CourseId']))
    data = cur.fetchall()
    cur.close()
    conn = MySQL.connection.cursor()
    conn.execute("""select * from asprequest where user1 = %s AND pdf ='' """%(session['RollNo']))
    userLp = conn.fetchall()
    conn.close()
    return render_template("Home.html",Noti = data,userLp = userLp,Name = session['Name'],Email = session['Email'],RollNo = session['RollNo'],image = session['image'],CourseId=session['CourseId'])
#-----------------------Social start----------------
@app.route('/Social')
def Social():
    return render_template("profile.html",Name = session['Name'],image = session['image'],Bio = session['Bio'],RollNo = session['RollNo'],Email = session['Email'])
@app.route("/AccountType",methods=['GET','POST'])
def AccountType():
    if request.method == 'POST':
        AType = request.form['AType']
        conn = MySQL.connection.cursor()
        conn.execute("""UPDATE studentd SET Atype = '%s' Where Email = '%s'"""%(AType,session['Email']))
        MySQL.connection.commit()
        flash("Your Preference has been saved. Happy Boarding😊")
        return redirect("/Bio")
    return render_template("AccountType.html",Name = session['Name'],image = session['image'])
@app.route("/PeopleOnCampus")
def people_on_campus():
    conn = MySQL.connection.cursor()
    conn.execute("""select * from studentd where RollNo != '%s'"""%(session['RollNo']))
    data = conn.fetchall()
    conn.close()
    return render_template("PeopleOnCampus.html",Name = session['Name'],image = session['image'],data = data)
@app.route('/Profile/<string:id>')
def Profile1(id):
    conn = MySQL.connection.cursor()
    conn.execute("""Select * from studentd where Sid = '%s' """%(id))
    data = conn.fetchall()
    conn.close()
    return render_template("PendingReq.html",Name = session['Name'],image = session['image'],data = data)
@app.route("/ProfileGet",methods=['GET','POST'])
def profile_get():
    if request.method == 'POST':
        Email = request.form['Email']
        cbb = MySQL.connection.cursor()
        req = cbb.execute("""select * from studentreq where user1 = '%s' and user2 = '%s'"""%(Email,session['RollNo']))
        Accreq = cbb.execute("""select * from studentacc where user1 = '%s' and user2 = '%s'"""%(Email,session['RollNo']))
        Accreq1 = cbb.execute("""select * from studentacc where user1 = '%s' and user2 = '%s'"""%(session['RollNo'],Email))
        if req >= 1:
            msg1 = Markup("""
                        <button type="submit" class="btn btn-block peach-gradient">Cancel Request!</button>
            """)
            conn = MySQL.connection.cursor()
            conn.execute("""select * from studentd where RollNo = '%s'"""%(Email))
            MySQL.connection.commit()
            data = conn.fetchall()
            return render_template("UserProfile.html", data = data,image = session['image'],msg1 = msg1)
        elif Accreq >=1 or Accreq1 >=1:
            msg1 = Markup("""
                        <button type="submit" class="btn btn-block btn-success">Un-Friend!</button>
            """)
            conn = MySQL.connection.cursor()
            conn.execute("""select * from studentd where RollNo = '%s'"""%(Email))
            MySQL.connection.commit()
            data = conn.fetchall()
            return render_template("UserProfile.html", data = data,image = session['image'],msg1 = msg1)
        else:
            conn = MySQL.connection.cursor()
            conn.execute("""select * from studentd where RollNo = '%s'"""%(Email))
            MySQL.connection.commit()
            data = conn.fetchall()
            com = MySQL.connection.cursor()
            com.execute("""select * from studentreq""")
            data1 = com.fetchall()
            msg = Markup("""
                    <button type="submit" class="btn btn-block aqua-gradient">Send Request</button>
            """)
            return render_template("UserProfile.html", data = data,image = session['image'],msg = msg,data1 = data1)
    return render_template("UserProfile.html")
@app.route("/uploader",methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        comment = request.form['comment']
        file = image(request.files['file'])
        Posttype = request.form['posttype']
        con = MySQL.connection.cursor()
        con.execute("""insert into post (RollNo,comment,image,accounttype) values('%s','%s','%s','%s')"""%(session['RollNo'],comment,file,Posttype))
        MySQL.connection.commit()
        return redirect("/dashboard")
    return render_template("Uploader.html",Name = session['Name'],image = session['image'])
@app.route('/reviews',methods=['GET','POST'])
def reviews():
    conn = MySQL.connection.cursor()
    conn.execute(""" select studentreq.id,studentd.Sid, studentd.RollNo,studentd.Name,studentreq.user1,studentd.image,studentreq.user2 FROM studentd INNER JOIN studentreq where user1 = '%s' and RollNo = user2; """%(session['RollNo']))
    user = conn.execute(""" select studentreq.id,studentd.Sid, studentd.RollNo,studentd.Name,studentreq.user1,studentd.image,studentreq.user2 FROM studentd INNER JOIN studentreq where user1 = '%s' and RollNo = user2; """%(session['RollNo']))
    if user == 0:
        flash("NO REQUEST TO DISPLAY!")
    data = conn.fetchall()
    return render_template("Review.html",Name = session['Name'],image = session['image'],data = data)
@app.route("/Activity")
def activity():
    return render_template("Activity.html",Name = session['Name'],image = session['image'])
@app.route('/StudentReq',methods=['GET','POST'])
def StudentReq():
    if request.method == 'POST':
        user1 = request.form['user1']
        conn = MySQL.connection.cursor()
        conn.execute("""INSERT INTO studentreq(user1,user2) values(%s,%s)"""%(user1,session['RollNo']))
        MySQL.connection.commit()
        flash("Request Send!")
    return redirect('/PeopleOnCampus')
@app.route('/deleteReq/<string:id_data>')
def deleteReq(id_data):
    connection = MySQL.connection.cursor()
    connection.execute("""Delete From studentreq where id = '%s'"""%(id_data))
    MySQL.connection.commit()
    flash("Request Delete")
    return redirect('/reviews')
@app.route('/Accepted',methods=['GET','POST'])
def Accepted():
    if request.method == 'POST':
        id = request.form['id']
        accept1 = request.form['user1']
        accept2 = request.form['user2']
        con = MySQL.connection.cursor()
        con.execute("""insert into studentacc (user1,user2) values(%s,%s)"""%(accept1,accept2))
        Conn = MySQL.connection.cursor()
        Conn.execute("""DELETE FROM studentreq WHERE id = %s"""%(id))
        MySQL.connection.commit()
        flash("Request Accepted!")
        return redirect("/reviews")
    return "close"
@app.route("/Bio",methods=['GET','POST'])
def Bio():
    if request.method == 'POST':
        bio = request.form['bio']
        conn = MySQL.connection.cursor()
        conn.execute("""UPDATE studentd SET Bio = '%s' where Email ='%s'"""%(bio,session['Email']))
        MySQL.connection.commit()
        flash("Bio Is Updated! Happy Boarding😊")
    return render_template("settings.html",Name=session['Name'],image = session['image'])
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html",Name = session['Name'],image = session['image'],Bio = session['Bio'])
#-----------------------Social End----------------------
@app.route('/submitassignment',methods=['GET','POST'])
def submitassignment():
    if request.method == 'POST':
        pdf = assignment(request.files['pdf'])
        Course = request.form['Course']
        Sem = request.form['sem']
        con = MySQL.connection.cursor()
        con.execute("""UPDATE asprequest SET pdf = '%s' where user1 = '%s' AND SubCode = '%s' AND Sem ='%s'"""%(pdf,session['RollNo'],Course,Sem))
        MySQL.connection.commit()
        flash("Assignement Send!")
        return redirect('/Homes')
    return "close"
@app.route('/LogOut',methods=['GET','POST'])
def LogOut():
        session.pop('loggedin',None)
        session.pop('Sid',None)
        session.pop('RollNo',None)
        session.pop('Email',None)
        session.pop('password',None)
        session.pop('image',None)
        session.pop('Name',None)
        session.clear()
        return redirect('/test')
@app.route('/PrintReg')
def PrintReg():
        cur = MySQL.connection.cursor()
        cur.execute("select * from collegecourse;")
        data = cur.fetchall()
        cur.close()
        conn = MySQL.connection.cursor()
        conn.execute("Select * from notification")
        db = conn.fetchall()
        conn.close()
        return render_template('Register.html',user=data,data = db)

@app.route('/Register',methods =['GET','POST'])
def Register():
    if request.method == 'POST' and 'Id' in request.form and 'CourseId' in request.form and 'email' in request.form and 'password' in request.form:
        userDetails = request.form
        RegisterNumber = userDetails['Id']
        CourseId = userDetails['CourseId']
        Email = userDetails['email']
        password = userDetails['password']
        comm = MySQL.connection.cursor()
        user = comm.execute("""SELECT * FROM studentd where RollNo = '%s' AND Email = '%s'"""%(RegisterNumber,Email))
        if len(password) < 8:
            flash("Password Should have atlest 8 char")
            return redirect("/PrintReg")
        elif re.search('[0-9]',password) is None:
            flash("Make sure you have Any One Numeric Value")
            return redirect("/PrintReg")
        elif re.search('[A-Z]',password) is None:
            flash("Make Sure you have One Capital letter")
            return redirect("/PrintReg")
        elif re.match('[_@$]',password):
            flash("Make Sure you have one Special characters(_,@,$)")
            return redirect("/PrintReg")
        elif user >=1:
            flash("RollNo Or Email Already Registered")
            return redirect("/PrintReg")
        else:
            con = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            con.execute("INSERT INTO studentd(RollNo,CourseId,Email,Password) values(%s,%s,%s,%s) ",(RegisterNumber,CourseId,Email,password))
            con.close()
            cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM studentd WHERE RollNo = %s AND  Password = %s;",(RegisterNumber,password))
            cur = MySQL.connection.cursor()
            cur.execute("select * from collegecourse")
            data = cur.fetchall()
            cur.close()
            MySQL.connection.commit()
            msg = "Your Account Is Successfully Created"
            accounts = cursor.fetchone()
            if accounts:
                session['loggedin'] = True
                session['RollNo'] = accounts['RollNo']
                session['CourseId'] = accounts['CourseId']
                session['Email'] = accounts['Email']
                session['image'] = accounts['image']
                session['Name'] = accounts['Name']
                return render_template("FormFill.html",msg = msg,Email = session['Email'],RollNo = session['RollNo'])
    return  "Invalid Url page"

@app.route("/RegFormFill",methods=['GET','POST'])
def reg_fill():
    if request.method == 'POST':
        Name = request.form['Name']
        RollNo = request.form['Roll']
        file = save_images(request.files['file'])
        con = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        con.execute("UPDATE studentd SET Name = %s WHERE RollNo = %s",(Name,RollNo))
        curr = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        curr.execute("UPDATE studentd SET image = %s WHERE RollNo = %s",(file,RollNo))
        cur = MySQL.connection.cursor()
        cur.execute("SELECT image FROM studentd;")
        data = cur.fetchall()
        MySQL.connection.commit()
        cur.close()
        return redirect('/Homes')
    return render_template("FormFill.html")
@app.route("/Redirect",methods=['GET','POST'])
def Redirect():
    cur = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from studentd")
    MySQL.connection.commit()
    accounts = cur.fetchone()
    if accounts:
        session['loggedin'] = True
        session['RollNo'] = accounts['RollNo']
        session['CourseId'] = accounts['CourseId']
        session['Email'] = accounts['Email']
        session['image'] = accounts['image']
        session['Name'] = accounts['Name']
        return redirect('/Homes')
    return render_template("Home.html",Name = session['Name'],Email = session['Email'],RollNo = session['RollNo'],image = session['image'],CourseId=session['CourseId'])
@app.route('/updateafter',methods=['GET','POST'])
def updateafter():
    if request.method == 'POST':
        Name = request.form['Name']
        file = save_images(request.files['file'])
        Email = request.form['Email']
        conn = MySQL.connection.cursor()
        conn.execute("UPDATE studentd SET Name = %s, image = %s WHERE Email = %s",(Name,file,Email))
        cur = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM studentd")
        MySQL.connection.commit()
        accounts = cur.fetchone()
        if accounts:
            session['loggedin'] = True
            session['RollNo'] = accounts['RollNo']
            session['CourseId'] = accounts['CourseId']
            session['Email'] = accounts['Email']
            session['image'] = accounts['image']
            session['Name'] = accounts['Name']
            flash("Updated Successfully")
            return redirect("/Redirect")
    return render_template("AfterUpdate.html",Name = session['Name'],Email = session['Email'],RollNo = session['RollNo'],image = session['image'],CourseId=session['CourseId'])

if __name__ == "__main__":
            app.run(host='127.0.0.1', port=8000,debug=True)
