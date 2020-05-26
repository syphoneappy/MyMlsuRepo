from flask import Flask, render_template , flash,request,session,abort,redirect,url_for,send_file
from flask_login import login_manager, login_required,logout_user
from pymysql import *
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pandas.io.sql as sql
import yaml,xlwt,re,os

app = Flask(__name__)
app.secret_key = 'This'
#-----------------------------database connection-----------
db = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] =  db['mysql_host']
app.config["MYSQL_USER"] =  db['mysql_user']
app.config["MYSQL_PASSWORD"] =  db['mysql_password']
app.config["MYSQL_DB"] =  db['mysql_db']

MySQL = MySQL(app)
@app.route('/', methods=['GET','POST'])
def index():
    msg = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form:
        userDetails = request.form
        RegisterNumber = userDetails['userId']
        password = userDetails['password']
        if len(password) < 8:
            flash("Password Should have atlest 8 char")
        elif re.search('[0-9]',password) is None:
            flash("Make sure you have Any One Numeric Value")
        elif re.search('[A-Z]',password) is None:
            flash("Make Sure you have One Capital letter")
        else:
            cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM collauth Where (RegistrationId = %s OR ProfName = %s) AND Password=%s',(RegisterNumber,RegisterNumber,password,))
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
    return render_template('LogIn.html',msg = msg)

@app.route("/Register",methods =['GET','POST'])
def Register():
    msg = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form and 'Prof.Name' in request.form:
        userDetails = request.form
        AnId = userDetails['userId']
        Psw = userDetails['Prof.Name']
        password = userDetails['password']
        if len(password) < 8:
            flash("Password Should have atlest 8 char")
        elif re.search('[0-9]',password) is None:
            flash("Make sure you have Any One Numeric Value")
        elif re.search('[A-Z]',password) is None:
            flash("Make Sure you have One Capital letter")
        else:
            con = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            con.execute("insert into CollAuth( RegistrationId,ProfName,Password) value(%s, %s, %s)",(AnId,Psw,password))
            cur = MySQL.connection.cursor()
            cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("select * from collegescheme,collegecourse;")
            cursor.execute('SELECT * FROM collauth Where RegistrationId = %s OR ProfName = %s AND Password =%s;',(AnId,Psw,password))
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
    flaskapp = sql.read_sql('select id,Scheme_Id,Scheme_Name,Cname,Year from collegecourse,collegescheme',con)
    print(flaskapp)
    flaskapp.to_excel('Excel.xls')
    flash('Data has been saved in excel')
    return redirect('/Homes')

@app.route("/download")
def download():
    path = "./Excel.xls"
    return send_file(path,as_attachment=True)

@app.route("/Homes")
def Homes():
    cur = MySQL.connection.cursor()
    cur.execute("select * from collegescheme,collegecourse;")
    data = cur.fetchall()
    cur.close()
    if 'loggedin' in session:
        return render_template("index.html",user = data, username=session['RegistrationId'],Name=session['ProfName'])
    return render_template('Error.html')
@app.route('/deleteS/<string:id_data>', methods = ['POST','GET'])
def deleteS(id_data):
        cur = MySQL.connection.cursor()
        cur.execute("DELETE FROM collegescheme WHERE id = %s",(id_data,))
        MySQL.connection.commit()
        flash("deleted")
        return redirect("/Homes")
@app.route('/deleteC/<string:id_data>', methods = ['POST','GET'])
def deleteC(id_data):
        cur = MySQL.connection.cursor()
        cur.execute("DELETE FROM collegecourse WHERE Cid = %s",(id_data,))
        MySQL.connection.commit()
        flash("deleted")
        return redirect("/Homes")
@app.route("/views",methods=['GET','POST'])
def views():
        cur = MySQL.connection.cursor()
        cur.execute("select * from collegescheme")
        MySQL.connection.commit()
        data = cur.fetchall()
        cur.close()
        return render_template("view.html",users = data)
#------------------------Create Table----------------------
@app.route("/CreateAScheme",methods=['GET','POST'])
def CreateAScheme():
    if request.method == 'POST':
        userDetails = request.form
        Scheme = userDetails['Scheme']
        SchemeName = userDetails['SchemeName']
        con = MySQL.connection.cursor()
        con.execute("INSERT into collegescheme (Scheme_Id,Scheme_Name) values('%s','%s')"%(Scheme,SchemeName))
        MySQL.connection.commit()
        con.close()
        flash("Succesfully Created Scheme")
        return redirect('/Homes')
    return "Cannot Fetch"
@app.route("/insertInScheme",methods=['GET','POST'])
def insertInScheme():
    if request.method == 'POST':
        userDetails = request.form
        Course = userDetails['Course']
        Year = userDetails['Year']
        con = MySQL.connection.cursor()
        con.execute("INSERT INTO collegecourse (Cname,Year) values('%s', '%s')"%(Course,Year))
        MySQL.connection.commit()
        con.close()
        flash("Inserted In Scheme")
        return redirect('/Homes')
    return "Cannot Fetch"

#--------------------UpdateInScheme---------------------
@app.route("/updateS/<string:id>",methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        userDetails = request.form
        SchemeId = userDetails['SchemeIdU']
        SchemeName = userDetails['SchemeNameU']
        con = MySQL.connection.cursor()
        con.execute("UPDATE collegescheme SET Scheme_Id = %s, Scheme_Name =%s, WHERE id = %s"%(SchemeId,SchemeName,id,))
        MySQL.connection.commit()
        con.close()
        flash("Updated In Scheme")
        return redirect('/Homes')
    return render_template("UpdateChech.html")
#-----------------------UpdateInScheme--------------------------------
@app.route("/updateInTable/<int:id>",methods=['GET','POST'])
def updateInTable(id):
    if request.method == 'POST':
        userDetails = request.form
        table = userDetails['tableU']
        Course = userDetails['CourseU']
        Year = userDetails['YearU']
        con = MySQL.connection.cursor()
        con.execute("UPDATE %s SET Course = '%s',Year ='%s' WHERE id = '%s'"%(table,Course,Year,id))
        MySQL.connection.commit()
        con.close()
        flash("UPDATED Succesfully")
        return redirect('/Homes')
    return "Cannot fetch"
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
#---------------------------exit-------------------------
if __name__ == "__main__":
            app.run(debug=True)
