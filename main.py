from flask import *
import json
import pymysql as mysql

app = Flask(__name__, static_url_path='',
            static_folder='templates')

mydb = mysql.connect(host="localhost", user="root", password="root123", database="login")
mycursor = mydb.cursor()



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
            return render_template('homebootpages/index.html')
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

if __name__ == "__main__":
    app.run(debug=True)