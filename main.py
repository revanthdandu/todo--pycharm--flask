from flask import *
from flask import request
import json
import pymysql as mysql




app = Flask(__name__, static_url_path='',
            static_folder='templates')

mydb = mysql.connect(host="localhost", user="root", password="root123", database="login")
mycursor = mydb.cursor()

app.secret_key="abc"

@app.route("/")
def index():
    return render_template('loginbootpages/index.html')



@app.route('/logintest', methods =['GET', 'POST'])
def logintest():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM logintest2 WHERE username = %s AND password = %s', (username, password))
        logintest = mycursor.fetchone()
        print(logintest)
        if logintest:
            msg = 'Logged in successfully !'
            session['username']=username
            return (display())
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginbootpages/index.html',msg=msg)

@app.route("/signuptest", methods=['GET', 'POST', 'PUT'])
def signuptest():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        print(name, username, password)

        mycursor.execute("SELECT * FROM logintest2")
        cmd = "INSERT INTO `logintest2`(`name`, `username`,`password`) VALUES(%s,%s,%s)"
        val = (name, username, password)
        res = mycursor.execute(cmd, val)
        mydb.commit()
        print(res)

    return render_template('signupbootpage/index.html')

@app.route("/newtask", methods=['GET', 'POST', 'PUT'])
def newtask():
    if request.method == "POST":
        date = request.form['date']
        task = request.form['task']
        user=session['username']
        print(user, date, task)

        mycursor.execute("SELECT * FROM tasks")
        cmd = "INSERT INTO `tasks`(`username`,`date`,`task`) VALUES(%s,%s,%s)"
        val = (user, date, task)
        res = mycursor.execute(cmd, val)
        mydb.commit()
        print(res)

    return render_template('homebootpages/untitled.html')

@app.route("/display", methods=['GET', 'POST', 'PUT'])
def display():
    user = session['username']
    cmd="select * from `tasks` where `username`=%s"
    val=(user)
    mycursor.execute(cmd, val)
    data = mycursor.fetchall()
    # data = dict(data)
    print(data)
    return render_template("homebootpages/index.html", value=data)

@app.route("/getid", methods=['GET', 'POST'])
def getid():
    item=request.args.get("item")
    print(item)
    cmd="DELETE FROM tasks WHERE Id=%s"
    val=(item)
    mycursor.execute(cmd,val)
    mydb.commit()
    data = mycursor.fetchall()
    print(data)
    return redirect(display())

@app.route("/logout", methods=['GET', 'POST', 'PUT'])
def logout():
    return (index())

if __name__ == "__main__":
    app.run(debug=True)