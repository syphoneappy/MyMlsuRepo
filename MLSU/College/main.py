from flask import Flask,flash,render_template,request,session,abort,redirect,url_for,send_file,Markup,current_app
from flask_login import login_manager, login_required,logout_user
from pymysql import *
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pandas.io.sql as sql
import yaml,xlwt,re,os,secrets
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'This'
#-----------------------------database connection-----------
db = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] =  db['mysql_host']
app.config["MYSQL_USER"] =  db['mysql_user']
app.config["MYSQL_PASSWORD"] =  db['mysql_password']
app.config["MYSQL_DB"] =  db['mysql_db']

MySQL = MySQL(app)

def Global(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'/python practice/MyMlsuRepo/MLSU/Student/static/Global',photo_name)
    photo.save(file_path)
    return photo_name

def Local(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'/python practice/MyMlsuRepo/MLSU/Student/static/Local',photo_name)
    photo.save(file_path)
    return photo_name

def senddocs(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'/python practice/MyMlsuRepo/MLSU/Teacher/static/data',photo_name)
    photo.save(file_path)
    return photo_name


@app.route('/', methods=['GET','POST'])
def index():
    msg = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form:
        userDetails = request.form
        RegisterNumber = userDetails['userId']
        password = userDetails['password']
        comm = MySQL.connection.cursor()
        comm.execute("""select Password from collauth where RegistrationId = '%s' OR ProfName = '%s'"""%(RegisterNumber,RegisterNumber))
        hash = comm.fetchone()
        user = pbkdf2_sha256.verify(password, hash[0])
        print(user)
        if user == True:
            cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM collauth Where RegistrationId = %s OR ProfName = %s',(RegisterNumber,RegisterNumber))
            accounts = cursor.fetchone()
            if accounts:
                session['loggedin'] = True
                session['ClgId'] = accounts['ClgId']
                session['RegistrationId'] = accounts['RegistrationId']
                session['ProfName'] = accounts['ProfName']
                session['Password'] = accounts['Password']
                return redirect('/Homes')
            else:
                msg = 'Incorrect username or password!'
        else:
            msg = 'Incorrect username or password!'
    return render_template('LogIn.html',msg = msg)

@app.route("/Register",methods =['GET','POST'])
def Register():
    msg = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form and 'Prof.Name' in request.form:
        userDetails = request.form
        AnId = userDetails['userId']
        Psw = userDetails['Prof.Name']
        password = userDetails['password']
        hash = pbkdf2_sha256.hash(password)
        if len(password) < 8:
            msg = "Password Should have atlest 8 char"
        elif re.search('[0-9]',password) is None:
            msg = "Make sure you have Any One Numeric Value"
        elif re.search('[A-Z]',password) is None:
            msg = "Make Sure you have One Capital letter"
        elif re.match('[_@$]',password):
            msg = "Make sure you have One Special Character!"
        else:
            con = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            con.execute("insert into CollAuth( RegistrationId,ProfName,Password) value(%s, %s, %s)",(AnId,Psw,hash))
            cur = MySQL.connection.cursor()
            cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("select * from collegecourse;")
            cursor.execute('SELECT * FROM collauth Where (RegistrationId = %s OR ProfName = %s) AND Password =%s;',(AnId,Psw,hash))
            data = cur.fetchall()
            MySQL.connection.commit()
            msg = "Succesfully Created Your Account"
            accounts = cursor.fetchone()
            if accounts:
                session['loggedin'] = True
                session['ClgId'] = accounts['ClgId']
                session['RegistrationId'] = accounts['RegistrationId']
                session['ProfName'] = accounts['ProfName']
                return render_template("index.html",msg = msg, user = data,username = session["RegistrationId"],Name=session['ProfName'])
    return render_template("Register.html")
#----------------------------------------------------------------------------
@app.route('/LogOut')
def LogOut():
    session.pop('loggedin',None)
    session.pop('ClgId',None)
    session.pop('RegistrationId',None)
    session.clear()
    msg = "Logged Out Succesfully"
    return render_template('LogIN.html',LogOutMessage=msg)
@app.route('/Excel')
def Excel():
    con=connect(user="root",password="1234",host="localhost",database="mlsu")
    flaskapp = sql.read_sql('select * from collegecourse',con)
    print(flaskapp)
    flaskapp.to_excel('Excel.xls')
    return redirect("/Homes")
@app.route("/download")
def download():
    path = "./Excel.xls"
    return send_file(path,as_attachment=True)

@app.route("/Homes")
def Homes():
    cur = MySQL.connection.cursor()
    cur.execute("select * from collegecourse;")
    data = cur.fetchall()
    con = MySQL.connection.cursor()
    con.execute("select * from tprequest where TPName1 = '%s'"%(session['RegistrationId']))
    data1 = con.fetchall()
    conn = MySQL.connection.cursor()
    conn.execute("select * from trequest;")
    Drequest = conn.fetchall()
    curr = MySQL.connection.cursor()
    curr.execute("select SName from collegecourse")
    data2 = curr.fetchall()
    cur.close()
    if 'loggedin' in session:
        return render_template("index.html" ,user = data,user2 = data2, username=session['RegistrationId'],Name=session['ProfName'],data1 = data1,Drequest = Drequest)
    return render_template('Error.html')
@app.route('/empty')
def empty():
    con = MySQL.connection.cursor()
    con.execute("TRUNCATE TABLE notification")
    MySQL.connection.commit()
    return redirect('/Homes')
@app.route('/emptyLocal')
def emptyLocal():
    con = MySQL.connection.cursor()
    con.execute("TRUNCATE TABLE courseid")
    MySQL.connection.commit()
    return redirect('/Homes')
@app.route('/delete/<string:id_data>', methods = ['POST','GET'])
def delete(id_data):
        cur = MySQL.connection.cursor()
        cur.execute("DELETE FROM collegecourse WHERE Cid = %s",(id_data,))
        MySQL.connection.commit()
        msg = "Deleted"
        return redirect("/Homes")
@app.route('/update/<string:id_data>',methods = ['POST','GET'])
def update(id_data):
    cur = MySQL.connection.cursor()
    cur.execute("select * from collegecourse where Cid = %s",(id_data))
    data = cur.fetchall()
    cur.close()
    MySQL.connection.commit()
    return render_template('UpdateChech.html',user = data)
@app.route('/update',methods=['GET','POST'])
def updateActually():
        if request.method == 'POST':
            userDetails = request.form
            id = userDetails['id']
            newS = userDetails['newS']
            newC = userDetails['newC']
            newY = userDetails['newY']
            con = MySQL.connection.cursor()
            con.execute("Update collegecourse Set SName = %s,Cname = %s,Year = %s Where Cid = %s",(newS,newC,newY,id))
            MySQL.connection.commit()
            return redirect('/Homes')
        return 'close'
@app.route("/insertInScheme",methods=['GET','POST'])
def insertInScheme():
    if request.method == 'POST':
        userDetails = request.form
        SName = userDetails['SName']
        Course = userDetails['Course']
        Year = userDetails['Year']
        con = MySQL.connection.cursor()
        con.execute("INSERT INTO collegecourse (SName,Cname,Year) values('%s', '%s','%s')"%(SName,Course,Year))
        MySQL.connection.commit()
        msg = "Scheme has been Created!"
        con.close()
        return redirect('/Homes')
    return "Cannot Fetch"
@app.route('/accept/<string:id_data>', methods=['GET','POST'])
def accept(id_data):
        con = MySQL.connection.cursor()
        con.execute("""select * from tprequest where TPid = '%s'"""%(id_data))
        data = con.fetchall()
        return render_template("temp.html",data=data)
@app.route('/accept',methods=['GET','POST'])
def acceptFinal():
    if request.method == 'POST':
        No0 = request.form['No0']
        No1 = request.form['No1']
        No2 = request.form['No2']
        conn = MySQL.connection.cursor()
        conn.execute("""delete from tprequest where TPid = '%s'"""%(No0))
        con = MySQL.connection.cursor()
        con.execute("insert into trequest(user1,user2) values(%s,%s)",(No1,No2))
        con.connection.commit()
        return redirect('/Homes')
    return "close"
@app.route('/reject/<string:id_data>')
def reject(id_data):
    con = MySQL.connection.cursor()
    con.execute("DELETE FROM tprequest WHERE TPid = %s",(id_data))
    con.connection.commit()
    return redirect('/Homes')
@app.route('/Drequest/<string:id_data>')
def drequest(id_data):
    con = MySQL.connection.cursor()
    con.execute("""select * from trequest where id = '%s'"""%(id_data))
    data = con.fetchall()
    con.connection.commit()
    conn = MySQL.connection.cursor()
    conn.execute("select * from collegecourse;")
    data1 = conn.fetchall()
    return render_template("SendDocs.html",data=data,data1= data1)
@app.route("/senddocsadmin", methods=['GET','POST'])
def senddocsadmin():
    if request.method == 'POST':
        Email = request.form['Email']
        Course = request.form['Course']
        SubCode = request.form['Subcode']
        SemYear = request.form['SemYear']
        RollNo = request.form['RollNO']
        file = senddocs(request.files['file'])
        message = request.form['message']
        con = MySQL.connection.cursor()
        value = con.execute("""Select * from studentd where RollNo = %s"""%(RollNo))
        if value >= 1:
            conn = MySQL.connection.cursor()
            conn.execute("""insert into SendDocsAdmin(user,Email,Course,SubjectCode,SemYear,RollNo,pdf,guide) values('%s','%s','%s','%s','%s','%s','%s','%s')"""%(session['RegistrationId'],Email,Course,SubCode,SemYear,RollNo,file,message))
            MySQL.connection.commit()
            return redirect('/Homes')
        else:
            msg = "RollNo does Not exits!"
            return render_template("SendDocs.html",msg = msg)
    return render_template("Error.html")
@app.route("/deleteUser/<string:id>")
def deleteUser(id):
    con = MySQL.connection.cursor()
    con.execute("""DELETE FROM trequest where id = '%s'"""%(id))
    MySQL.connection.commit()
    return redirect('/Homes')
#-----------------------UpdateInScheme--------------------------------
@app.route("/ForgetPass", methods=['GET','POST'])
def ForgetPass():
    if request.method == 'POST':
        userDetails = request.form
        Id = userDetails['Id']
        NewPassword = userDetails['NewPassword']
        con = MySQL.connection.cursor()
        con.execute("UPDATE collauth SET Password = '%s' WHERE RegistrationId = '%s'"%(NewPassword,Id))
        MySQL.connection.commit()
        con.close()
        flash("Password Changed Succesfully")
        return redirect("/")
    return render_template("Forget.html")
@app.route("/Notifications", methods=["GET", "POST"])
def flash():
    cur = MySQL.connection.cursor()
    cur.execute("select * from collegecourse")
    MySQL.connection.commit()
    data = cur.fetchall()
    cur.close()
    return render_template("Notification.html",data=data)

@app.route("/Global",methods=['GET','POST'])
def Add():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        file = Global(request.files['file'])
        name = request.form['message']
        con = MySQL.connection.cursor()
        con.execute("""
        insert into notification(Title,time,Noti,pdf) values (%s,%s,%s,%s)
        """,(date,time,name,file))
        MySQL.connection.commit()
        return redirect("/Notifications")
    return 'Failed'
@app.route('/local',methods=['GET','POST'])
def Update():
    if request.method == 'POST':
        Course = request.form['Course1']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']
        file = Local(request.files['file'])
        con = MySQL.connection.cursor()
        con.execute("""INSERT INTO courseid(Course,date,time,details,pdf) VALUES(%s,%s,%s,%s,%s)""",(Course,date,time,message,file))
        MySQL.connection.commit()
        return redirect('/Notifications')
    return 'Failed'
#---------------------------exit-------------------------
if __name__ == "__main__":
            app.run(debug=True)
