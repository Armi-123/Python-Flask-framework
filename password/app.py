from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors  
import base64
from datetime import timedelta
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "ABC"
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = '12345'
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_DB"] = 'armi'

db = MySQL(app) 

@app.route('/')
def index():
    return render_template('login.html')

@app.route("/store",methods = ['GET','POST'])   
def store():
       if request.method == 'POST':
        user_name = request.form["user_name"]
        Password = request.form["Password"]
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Address = request.form["Address"]
        Mobile = request.form["Mobile"]
        Dob = request.form["Dob"]
        Email = request.form["Email"]
        Gender = request.form["Gender"]
        State = request.form['State']
        City = request.form['City']
        Hobbies = request.form.getlist("Hobbies")
        a = ','.join(Hobbies)
        Education = request.form.getlist("Education")
        b = ','.join(Education)
        Image = request.files["Image"]

        hashed_password = bcrypt.generate_password_hash (Password).decode('utf-8')
        print(hashed_password)
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into form1 (user_name,Password,First_Name,Last_Name,Address,Mobile,Dob,Email,Gender,State,City,Hobbies,Education,Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_name,hashed_password,First_Name,Last_Name,Address,Mobile,Dob,Email,Gender,State,City,[a],[b],Image.read(),))
        db.connection.commit()

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from form1 where user_name = %s', (user_name,))
        upload = cursor.fetchone()

        encoded_image = base64.b64encode(upload["Image"]).decode('utf-8')
        upload['encode_Image']  = encoded_image

        return redirect(url_for("form"))

@app.route("/data")
def data():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM form1")
    store = cursor.fetchall()
    cursor.close()
    return render_template('data.html',store = store)

@app.route("/form")
def form():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM form1")
    store = cursor.fetchall()
    cursor.close()
    return render_template('form.html',store = store)
    
@app.route('/delete/<id>')
def delete(id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM form1 WHERE id = %s", (id,))
    db.connection.commit()
    cursor.close()
    return redirect(url_for('data'))

@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from form1 where id = %s",(id,))
    id = cursor.fetchone()
    encoded_image = base64.b64encode(id["Image"]).decode('utf-8')
    id['Image']  = encoded_image
    return render_template('edit.html',id = id)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        user_name = request.form["user_name"]
        Password = request.form["Password"]
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Address = request.form["Address"]
        Mobile = request.form["Mobile"]
        Dob = request.form["Dob"]
        Email = request.form["Email"]
        Gender = request.form["Gender"]
        State = request.form['State']
        City = request.form['City']
        Hobbies = request.form.getlist("Hobbies")
        a = ','.join(Hobbies)
        Education = request.form.getlist("Education")
        b = ','.join(Education)
        Image = request.files["Image"]
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE form1 SET user_name = %s,Password = %s, First_Name = %s,Last_Name = %s,Address = %s,Mobile = %s,Dob = %s,Email = %s,Gender = %s,State = %s,City = %s,Hobbies = %s,Education = %s,Image = %s WHERE id = %s",(user_name,Password,First_Name,Last_Name,Address,Mobile,Dob,Email,Gender,State,City,[a],[b],Image.read(),id,))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('login'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id form1 WHERE id = %s", (id,))
    id = cursor.fetchone()
    cursor.close()
    return render_template('form.html', id = id )
   
@app.route("/display1",methods = ['GET'])
def display1():
    if 'loggedin' in session:
        user_name = session['user_name']

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from form1 WHERE user_name = %s", (user_name,))
        upload = cursor.fetchone()
        encoded_image = base64.b64encode(upload["Image"]).decode('utf-8')
        upload['Image']  = encoded_image

        if upload :
            return render_template('display1.html',upload=upload)
        else:
            return render_template('login.html')
    else:
        return redirect(url_for('login'))   

@app.route("/login",methods = ['GET','POST'])
def login():   
    msg = '' 
    if request.method == 'POST' and 'user_name' in request.form and 'Password'  in request.form:
        user_name = request.form['user_name']
        Password = request.form['Password']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from form1 WHERE user_name = %s",(user_name,))
        upload = cursor.fetchone()

        if upload and bcrypt.check_password_hash(upload['Password'],Password):
            encoded_image = base64.b64encode(upload["Image"]).decode('utf-8')
            upload['encode_Image']  = encoded_image

            session['loggedin'] = True
            session['id'] = upload['id']
            session['user_name'] = upload['user_name']
            return redirect (url_for('display1',upload = upload['user_name']))
        else:
            msg = 'Incorrect username / password '
            return render_template('login.html',msg = msg)
    
    return render_template('login.html')

@app.route("/update_password/<int:id>",methods = ['GET','POST'])
def update_password(id):
    msg = ''
    if request.method == 'POST' and 'Old_Password' in request.form and 'New_Password'  in request.form:
        Old_Password = request.form['Old_Password']
        New_Password = request.form['New_Password']
        user_name = session['user_name']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from form1 where user_name = %s",(user_name,))
        upload = cursor.fetchone()
        is_true = bcrypt.check_password_hash(upload['Password'],Old_Password)
        if is_true:
            if upload:
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                hashed_password = bcrypt.generate_password_hash (New_Password).decode('utf-8')
                print(hashed_password)
                cursor.execute("update form1 set Password = %s where id = %s",(hashed_password,))
                db.connection.commit()

                return redirect(url_for('display1'))
        else:
            msg = 'Old password does not match'

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from form1 where id = %s', (id,))
        upload = cursor.fetchone()

        encoded_image = base64.b64encode(id["Image"]).decode('utf-8')
        id['Image']  = encoded_image
        return render_template('edit.html',id = id)
    
    return render_template('change_password.html',id =  id)

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('user_name',None)
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)