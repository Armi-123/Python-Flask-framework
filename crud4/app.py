from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = "ABC"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "12345"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = "armi"

mysql = MySQL(app)

@app.route("/Retrive")
def retrive2():
    coursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    coursor.execute("select * from customer")
    store = coursor.fetchall()
    print(store)
    return render_template('retrive.html',store = store)

@app.route("/create",methods = ['GET','POST'])
def create():
    return render_template('create.html')

@app.route("/store",methods = ['GET','POST'])
def store():
    if request.method == 'POST':
        c_name = request.form['c_name']
        c_city = request.form['c_city']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into customer(c_name,c_city) values(%s,%s)",(c_name,c_city,))

        mysql.connection.commit()

        cursor.close()
    return redirect(url_for('create'))

@app.route('/delete/<int:task_id>')
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("Delete from customer where id = %s",(id,))
    mysql.connection.commit()
    return redirect(url_for('retrive'))

@app.route("/edit/<int:task_id>",methods = ['GET','POST'])
def edit(id):
    return render_template('edit.html',task_id = id)

@app.route('/update/<int:task_id>',methods = ['GET','POST'])
def update(task_id):
    if request.method == 'POST':
        c_name = request.form['c_name']
        c_city = request.form['c_city']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update customer set c_name = %s,c_city = %s where id = %s",(c_name,c_city,task_id,))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('retrive'))

if __name__ == "__main__":
    app.run(debug = True)