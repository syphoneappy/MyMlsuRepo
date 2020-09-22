from flask import Flask,render_template,flash,request,session,abort,redirect,url_for,send_file,Markup,current_app
from flask_login import login_manager, login_required,logout_user
from pymysql import *
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pandas.io.sql as sql
import yaml,xlwt,re,os,secrets

app = Flask(__name__)
app.secret_key = 'This'
#-----------------------------database connection-----------
db = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] =  db['mysql_host']
app.config["MYSQL_USER"] =  db['mysql_user']
app.config["MYSQL_PASSWORD"] =  db['mysql_password']
app.config["MYSQL_DB"] =  db['mysql_db']


MySQL = MySQL(app)

def photo(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name =hash_photo + file_extension
    file_path =os.path.join(current_app.root_path,'/python practice/MyMlsuRepo/MLSU/College/static/Tumb',photo_name)
    photo.save(file_path)
    return photo_name

@app.route('/', methods=['GET','POST'])
def index():
    msg = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form:
        userDetails = request.form
        RegisterNumber = userDetails['userId']
        password = userDetails['password']
        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacherd Where Email = %s AND Password=%s',(RegisterNumber,password))
        accounts = cursor.fetchone()
        if accounts:
            session['loggedin'] = True
            session['id'] = accounts['id']
            session['FirstName'] = accounts['FirstName']
            session['LastName'] = accounts['LastName']
            session['Email'] = accounts['Email']
            session['Password'] = accounts['Password']
            return redirect('/Homes')
        else:
            msg = 'Incorrect username or password!'
    return render_template('LogIn.html',msg = msg)

@app.route('/Register',methods=['GET','POST'])
def func_Reg():
    msg = ''
    if request.method == 'POST' and 'FirstName' in request.form and 'LastName' in request.form and 'Email' in request.form and 'password' in request.form:
        userDetails = request.form
        Psw = userDetails['FirstName']
        LastName = userDetails['LastName']
        AnId = userDetails['Email']
        password = userDetails['password']
        if len(password) < 8:
            flash("Password Should have atlest 8 char")
        elif re.search('[0-9]',password) is None:
            flash("Make sure you have Any One Numeric Value")
        elif re.search('[A-Z]',password) is None:
            flash("Make Sure you have One Capital letter")
        elif re.match('[_@$]',password):
            flash("Make Sure you have one Special characters(_,@,$)")
        else:
            Cursor = MySQL.connection.cursor()
            Cursor.execute("Select * from collauth")
            data = Cursor.fetchall()
            con = MySQL.connection.cursor()
            con.execute("insert into teacherd(Email,FirstName,LastName,Password) value(%s, %s, %s, %s)",(AnId,Psw,LastName,password))
            MySQL.connection.commit()
            msg = "Succesfully Created Your Account. Login To Continue"
            return render_template("Login.html",msg = msg)
    return render_template('Register.html')

@app.route('/LogOut')
def LogOut():
    session.pop('loggedin',None)
    session.pop('FirstName',None)
    session.pop('LastName',None)
    session.pop('Email',None)
    session.clear()
    msg = "Logged Out Succesfully"
    return render_template('LogIN.html',LogOutMessage=msg)
@app.route('/SendMarks',methods=['GET','POST'])
def SendMarks():
    if request.method == 'POST':
        id = request.form['id']
        Marks = request.form['Marks']
        TMarks = request.form['TMarks']
        file = photo(request.files['file'])
        if TMarks >= Marks:
            con = MySQL.connection.cursor()
            con.execute("""Update senddocsadmin Set Marks = '%s',TMarks = '%s',image = '%s' where id = '%s'"""%(Marks,TMarks,file,id))
            MySQL.connection.commit()
        else:
            flash("Marks Are greater than the total marks!")
            return redirect('/DataRecive')
    return redirect("/DataRecive")
@app.route('/sendmarksassign',methods=['GET','POST'])
def sendmarksassign():
    if request.method == 'POST':
        id = request.form['id']
        Marks = request.form['Marks']
        TMarks = request.form['TMarks']
        image = photo(request.files['file'])
        if TMarks >= Marks:
            conn = MySQL.connection.cursor()
            con = conn.execute("""update asprequest set Marks = '%s',TotalMarks = '%s' ,image = '%s' where id = '%s'"""%(Marks,TMarks,image,id))
            MySQL.connection.commit()
        else:
            flash("Marks Are greater than the total marks!")
            return redirect("/DataRecive")
    return redirect("/DataRecive")
@app.route("/Homes")
def Homes():
    Cursor = MySQL.connection.cursor()
    user1 = Cursor.execute("Select * from tprequest where TPName2 = '%s'"%(session['Email']))
    user2 = Cursor.execute("Select * from trequest where user2 = '%s'"%(session['Email']))
    if user1 == 0 and user2 == 0:
        msg = Markup("<strong style='color:red'>No Request Send!</strong>")
    elif user2 >= 1:
        msg = Markup("<strong style='color:green'>Request Accepted</strong>")
    else:
        msg = Markup("<strong style='color:orange'>Request Pending!</strong>")
    Con = MySQL.connection.cursor()
    Con.execute("SELECT * FROM CollAuth;")
    MySQL.connection.commit()
    data = Con.fetchall()
    return render_template("Home.html",data = data, username=session['Email'],FName=session['FirstName'],LName = session['LastName'],msg = msg)
@app.route('/DataRecive')
def dataRecive():
    conn = MySQL.connection.cursor()
    value = conn.execute("""SELECT Marks,TMarks FROM senddocsadmin where Marks = '' AND Email = '%s'"""%(session['Email']))
    value2 = conn.execute("""SELECT * FROM asprequest where marks = '' AND user2 = '%s'"""%(session['Email']))
    if value >= 1 or value2 >= 1:
        con = MySQL.connection.cursor()
        con.execute("""SELECT * FROM senddocsadmin where Marks = '' AND Email = '%s'"""%(session['Email']))
        data = con.fetchall()
        cur = MySQL.connection.cursor()
        cur.execute("""SELECT * FROM asprequest where marks = '' AND user2 = '%s'"""%(session['Email']))
        data1 = cur.fetchall()
        MySQL.connection.commit()
        return render_template('Data.html',user = data,user1 = data1)
    else:
        msg = Markup("""
        <h1 class="display-1 text-danger text-center">Data Not Available!</h1>
        <hr>
        <h6 class="lead text-success text-center">Ask Admin to Send data!</h6>
        """)
        return render_template('Data.html',msg = msg)
    return render_template('data.html')
@app.route("/Request",methods=['GET','POST'])
def Request():
    id = request.form['id']
    if request.method == 'POST':
        conn = MySQL.connection.cursor()
        value = conn.execute("select * from tprequest where TPName2 = '%s' "%(session['Email']))
        value2 = conn.execute("select * from trequest where user2 = '%s' "%(session['Email']))
        if value == 0 and value2 == 0:
            cur = MySQL.connection.cursor()
            cur.execute("insert into tprequest (TPName1,TPName2) values(%s,%s)",(id,session['Email']))
            MySQL.connection.commit()
            flash("Request Send")
            return redirect('/Homes')
        else:
            msg = Markup("""<div class="display:flex"><strong style='color: red'>Request Declined   !</strong><br>
            You have already made request to admin. Please clear your request first. <br>Then Send a New Request.</div>""")
            flash(msg)
            return redirect('/Homes')
    return "close"
@app.route('/assignment',methods=['GET','POST'])
def assignment():
    comm = MySQL.connection.cursor()
    comm.execute("""select * from asprequest where user2 = '%s'"""%(session['Email']))
    data1 = comm.fetchall()
    if request.method == 'POST':
        RollNo = request.form['RollNo']
        con = MySQL.connection.cursor()
        user = con.execute("""select * from studentd where RollNo = '%s'"""%(RollNo))
        con.execute("""select * from studentd where RollNo = '%s'"""%(RollNo))
        data = con.fetchall()
        if user == 0:
            flash("No student Record found for             " + RollNo + "!")
        MySQL.connection.commit()
        return render_template('assignment.html',data = data)
    return render_template('assignment.html',data1 = data1)
@app.route('/AsPrequest', methods=['GET','POST'])
def AsPrequest():
    if request.method == 'POST':
        user = request.form['user1']
        Code = request.form['Code']
        date = request.form['date']
        sem = request.form['quantity']
        details = request.form['detail']
        con = MySQL.connection.cursor()
        con.execute("""
        insert into asprequest(user1,user2,SubCode,Sem,DD,details) values('%s','%s','%s','%s','%s','%s')
        """%(user,session['Email'],Code,sem,date,details))
        MySQL.connection.commit()
        flash("Assignement Request Made..")
        return redirect("/assignment")
    return "Error updating!"
@app.route("/delete")
def delete():
    con = MySQL.connection.cursor()
    con.execute("delete from tprequest where TPName2 = '%s'"%(session['Email']))
    MySQL.connection.commit()
    conn = MySQL.connection.cursor()
    conn.execute("delete from trequest where user2 = '%s'"%(session['Email']))
    MySQL.connection.commit()
    flash("Request Clear!")
    return redirect('/Homes')
if __name__ == "__main__":
            app.run(host='127.0.0.1', port=9000,debug=True)
