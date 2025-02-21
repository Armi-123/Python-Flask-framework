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
    return render_template('index.html')

@app.route("/data")
def data():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from employee")
    store = cursor.fetchall()
    cursor.close()
    return render_template('data.html',store = store)

@app.route("/store",methods = ['GET','POST'])   
def store():
       if request.method == 'POST':
        Name = request.form["Name"]
        DOB = request.form["DOB"]
        Mobile = request.form["Mobile"]
        Join_Date = request.form['Join_Date']
        Salary =  request.form['Salary']
        Role = request.form.getlist("Role")
        a = ','.join(Role)
        Image = request.files["Image"]
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into employee (Name,DOB,Mobile,Join_Date,Salary,Role,Image) VALUES (%s,%s,%s,%s,%s,%s,%s)",(Name,DOB,Mobile,Join_Date,Salary,[a],Image.read(),))
        db.connection.commit()
        cursor.close()
        return 'scueesfull'
       
@app.route('/delete/<id>')
def delete(id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("delete from employee where id = %s", (id,))
    db.connection.commit()
    cursor.close()
    return redirect(url_for('data')) 

@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from employee where id = %s",(id,))
    id = cursor.fetchone()
    return render_template('edit.html',id = id)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        Name = request.form["Name"]
        DOB = request.form["DOB"]
        Mobile = request.form["Mobile"]
        Join_Date = request.form['Join_Date']
        Salary =  request.form['Salary']
        Role = request.form.getlist("Role")
        a = ','.join(Role)
        Image = request.files["Image"]
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update employee set Name = %s,DOB = %s,Mobile = %s,Join_Date = %s,Salary = %s,Role = %s,Image = %s WHERE id = %s",(Name,DOB,Mobile,Join_Date,Salary,[a],Image.read(),id,))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('data'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id employee WHERE id = %s", (id,))
    id = cursor.fetchone()
    cursor.close()
    return render_template('index.html', id = id )

@app.route("/display/<int:id>",methods = ['GET'])
def display(id):    
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from employee WHERE id = %s", (id,))
    upload = cursor.fetchone()
    encoded_image = base64.b64encode(upload["Image"]).decode('utf-8')
    upload['Image']  = encoded_image
    return render_template('display.html',upload=upload)

if __name__ == '__main__':
    app.run(debug=True)