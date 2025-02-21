from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app1 = Flask(__name__)

app1.secret_key = "ABC"

app1.config['MYSQL_HOST'] = "localhost"
app1.config['MYSQL_USER'] = "root"
app1.config['MYSQL_PASSWORD'] = "12345"
app1.config['MYSQL_PORT'] = 3306
app1.config['MYSQL_DB'] = "employee"

mysql = MySQL(app1)

@app1.route("/Retrive1")
def retrive1():
    coursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    coursor.execute("select * from country")
    store = coursor.fetchall()
    print(store)
    return render_template('retrive1.html',store = store)

@app1.route("/create1",methods = ['GET','POST'])
def create1():
    return render_template('create1.html')

@app1.route("/store",methods = ['GET','POST'])
def store():
    if request.method == 'POST':
        country_name = request.form['cname']

        coursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        coursor.execute("insert into country(country_name) values(%s)",(country_name,))

        mysql.connection.commit()

        coursor.close()
    return redirect(url_for('create1'))

@app1.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("Delete from country where id = %s",(id,))
    mysql.connection.commit()
    return redirect(url_for('retrive1'))

@app1.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    return render_template('edit.html',id = id)

@app1.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    if request.method == 'POST':
        country_name = request.form['cname']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update country set country_name = %s where id = %s",(country_name,id,))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('retrive1'))

if __name__ == "__main__":
    app1.run(debug = True)