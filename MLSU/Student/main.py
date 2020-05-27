from flask import Flask, render_template , flash,request,session,abort,redirect,url_for
from pymysql import *
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pandas.io.sql as sql
import yaml,xlwt,re,os
import time
app = Flask(__name__)
app.secret_key = 'This'
#-----------------------------database connection-----------
db = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] =  db['mysql_host']
app.config["MYSQL_USER"] =  db['mysql_user']
app.config["MYSQL_PASSWORD"] =  db['mysql_password']
app.config["MYSQL_DB"] =  db['mysql_db']
app.config["SERVER_NAME"] = 'localhost:8000'
MySQL = MySQL(app)
@app.route('/test')
def test():
    return render_template('LogIn.html')
def func_name(foo):
    return render_template('expression')
@app.route("/", methods=['GET','POST'])
def index():
    seconds = 1
    for i in range(seconds):
        times = print(str(seconds - i) + "seconds remain")
        time.sleep(1)

    return """
    <h1 style='text-align:center;margin-top:200px;'><kbd>Welcome To student Portal</kbd></h1>
    <h3 style='text-align:center;color:red'><kbd>Work In progress...</kbd></h3>
    <p id="demo" style='text-align:center;color:red'></p>
    <script>
    var countDownDate = new Date("June 17, 2020 15:37:25").getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {

    // Get today's date and time
    var now = new Date().getTime();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Output the result in an element with id="demo"
    document.getElementById("demo").innerHTML = days + ":days| " + hours + " :hours| " + minutes + ":   minutes| " + seconds + ": seconds";

    // If the count down is over, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("demo").innerHTML = "EXPIRED";
        }
    }, 1000);
    </script>
    """


if __name__ == "__main__":
            app.run(host='127.0.0.1', port=8000,debug=True)
