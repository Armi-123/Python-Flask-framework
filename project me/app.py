from flask import Flask,redirect,render_template,request,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import base64
from datetime import date, timedelta
from flask_bcrypt import Bcrypt 
import os

app = Flask(__name__)
bcrypt = Bcrypt(app) 

app.secret_key = 'happpyyyy_birthdayyyy_om'
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=5)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password1 = request.form['password']

        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute('select * from data where username = %s ',(username,))
        account = mycursor.fetchone()

        if account and bcrypt.check_password_hash(account['password'], password1):
            encoded_image = base64.b64encode(account['image']).decode('utf-8')
            account['encoded_image'] = encoded_image

            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('index',account=account['username']))
        
        else:
            msg = 'Incorrect Username/Password !'
            return render_template('login.html',msg=msg)

    return render_template('login.html')

@app.route('/register')
def insert():
    msg = ''
    return render_template('registration.html',msg = msg)

@app.route('/index')
def index():
    if 'loggedin' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from data where username=%s',(username,))
        account = cur.fetchone()
        
        encoded_image = base64.b64encode(account['image']).decode('utf-8')
        account['encoded_image'] = encoded_image

        if account:
            return render_template('index.html',account=account)
        else:
            return render_template('login.html')
    else:
        return redirect(url_for('login'))

@app.route('/store',methods = ['GET','POST'])
def store():
    if request.method == 'POST':
        u_name = request.form['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from data where username=%s',(u_name,))
        account = cur.fetchone()

        if account:
            msg = 'Account Already Exists!!'
            render_template('registration.html',msg=msg)
        else:
            u_name = request.form['username']
            f_name = request.form['fname']
            m_name = request.form['mname']
            l_name = request.form['lname']
            mobile = request.form['mobile']
            email = request.form['email']
            dob = request.form['DOB']
            gender = request.form['gender']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']
            password = request.form['password']
            f = request.files['image']

            hashed_password = bcrypt.generate_password_hash (password).decode('utf-8') 
            print(hashed_password)
            
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('insert into data(username, fname, mname, lname, mobile, email, gender, address,DOB,state, city, password, image) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(u_name,f_name,m_name,l_name,mobile, email, gender, address,dob,state,city,hashed_password,f.read(),))
            mysql.connection.commit()

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('select * from data where username = %s', (u_name,))
            account = cur.fetchone()

            encoded_image = base64.b64encode(account['image']).decode('utf-8')
            account['encoded_image'] = encoded_image

            return redirect(url_for('login'))
        
    return render_template('registration.html')

@app.route('/userdelete/<int:id>')
def userdelete(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('delete from data where user_id = %s',(id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('login'))

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        u_name = request.form['username']
        f_name = request.form['fname']
        m_name = request.form['mname']
        l_name = request.form['lname']
        mobile = request.form['mobile']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        f = request.files['file']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('update data set username = %s, firstname = %s, middlename = %s, lastname = %s, mobile = %s, email = %s, birthdate = %s, gender = %s, address = %s, state = %s, city = %s, filename = %s,image = %s where user_id = %s',(u_name,f_name,m_name,l_name,mobile,email,dob,gender,address,state,city,f.filename,f.read(),id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('select * from data where user_id = %s',(id,))
    result = cur.fetchone()

    encoded_image = base64.b64encode(result['image']).decode('utf-8')
    result['encoded_image'] = encoded_image
    
    return render_template('update.html',account = result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/updatepass/<int:id>',methods = ['POST','GET'])
def updatepass(id):
    msg = ''
    if request.method == 'POST' and 'oldPassword' in request.form and 'newPassword' in request.form:
        oPassword = request.form['oldPassword']
        nPassword = request.form['newPassword']
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from data where username=%s',(username,))
        account = cur.fetchone()
        is_true = bcrypt.check_password_hash(account['password'], oPassword)
        if is_true:
            if account:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                hashed_password = bcrypt.generate_password_hash (nPassword).decode('utf-8')
                print(hashed_password)
                cur.execute('UPDATE data set password = %s where user_id = %s', (hashed_password,id,))
                mysql.connection.commit()
                
                return redirect(url_for('index'))
        else:
            msg = "Old Password is Doesn't match"
            
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('select * from data where user_id=%s',(id,))
    account = cur.fetchone()

    encoded_image = base64.b64encode(account['image']).decode('utf-8')
    account['encoded_image'] = encoded_image

    return render_template('updatepassword.html', account=account, msg = msg)


if __name__ == '__main__':
    app.run(debug=True)