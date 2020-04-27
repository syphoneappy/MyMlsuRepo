from flask import Flask, render_template , flash,request,session,abort,redirect,url_for
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

@app.route("/Homes")
def index():
    cur = MySQL.connection.cursor()
    cur.execute("select * from collegescheme;")
    data = cur.fetchall()
    cur.close()
    return render_template("index.html",user = data)
@app.route('/deleteS/<string:id_data>', methods = ['POST','GET'])
def delete(id_data):
        cur = MySQL.connection.cursor()
        cur.execute("DELETE FROM collegescheme WHERE id = %s",(id_data,))
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
@app.route("/updateInScheme",methods=['GET','POST'])
def update():
    if request.method == 'POST':
        userDetails = request.form
        table1 = userDetails['Change1']
        table2 = userDetails['Change2']
        con = MySQL.connection.cursor()
        con.execute("RENAME TABLE %s TO %s"%(table1,table2))
        MySQL.connection.commit()
        con.close()
        flash("Updated In Scheme")
        return redirect('/Homes')
    return "cannot Fetch"
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
#----------------------------Excel---------------------
#*********************This Not Working Now*************
@app.route('/Excel/',methods = ['POST','GET'])
def Excel():
    con=connect(user="root",password="1234",host="localhost",database="mlsu")
    Selected = request.form["Selected"]
    flaskapp=sql.read_sql('select * from %s'%(Selected))
    print(flaskapp)
    flaskapp.to_excel('Excel.xls')
    flash('data Has been Saved In Excel')
    return "Converted"
#---------------------------exit-------------------------
if __name__ == "__main__":
            app.run(debug=True)
