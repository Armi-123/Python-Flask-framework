from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors  
import base64 

app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = '12345'
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_DB"] = 'armi'

db = MySQL(app) 

@app.route('/')
def index():
    return render_template('form.html')

@app.route("/store",methods = ['GET','POST'])   
def store():
       if request.method == 'POST':
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
        cursor.execute("INSERT INTO form (First_Name,Last_Name,Address,Mobile,Dob,Email,Gender,State,City,Hobbies,Education,Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(First_Name,Last_Name,Address,Mobile,Dob,Email,Gender,State,City,[a],[b],Image.read(),))
        db.connection.commit()
        cursor.close()
        return 'scueesfull'

@app.route("/data")
def data():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM form")
    store = cursor.fetchall()
    cursor.close()
    return render_template('data.html',store = store)
    
@app.route('/delete/<id>')
def delete(id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM form WHERE id = %s", (id,))
    db.connection.commit()
    cursor.close()
    return redirect(url_for('data'))

@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from form where id = %s",(id,))
    id = cursor.fetchone()
    encoded_image = base64.b64encode(id["Image"]).decode('utf-8')
    id['Image']  = encoded_image
    return render_template('edit.html',id = id)


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
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
        cursor.execute("UPDATE form SET First_Name = %s,Last_Name = %s,Address = %s,Mobile = %s,Dob = %s,Email = %s,Gender = %s,State = %s,City = %s,Hobbies = %s,Education = %s,Image = %s WHERE id = %s",(First_Name,Last_Name,Address,Mobile,Dob,Email,Gender,State,City,[a],[b],Image.read(),id,))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('data'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id form WHERE id = %s", (id,))
    id = cursor.fetchone()
    cursor.close()
    return render_template('form.html', id = id )
   
@app.route("/display1/<int:id>",methods = ['GET'])
def display1(id):    
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from form WHERE id = %s", (id,))
    upload = cursor.fetchone()
    encoded_image = base64.b64encode(upload["Image"]).decode('utf-8')
    upload['Image']  = encoded_image
    return render_template('display1.html',upload=upload)

if __name__ == '__main__':
    app.run(debug=True)