from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = "ABC"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = "armi"

mysql = MySQL(app)

# @app.route("/")
# def hello():
#     return "<h1>Hello Nandit</h1>"

# @app.route("/armi")
# def raju():
#     return "<h1>Hello Im armi let's go to the College</h1>"


@app.route("/Retrive")
def retrive():
    coursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    coursor.execute("select * from table1")
    store = coursor.fetchall()
    print(store)
    return render_template('retrive.html',store = store)

@app.route("/create",methods = ['GET','POST'])
def create():
    return render_template('create.html')

@app.route("/store",methods = ['GET','POST'])
def store():
    if request.method == 'POST':
        name = request.form['dname']

        coursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        coursor.execute("insert into table1(name) values(%s)",(name,))

        mysql.connection.commit()

        coursor.close()
    return redirect(url_for('create'))

@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("Delete from table1 where id = %s",(id,))
    mysql.connection.commit()
    return redirect(url_for('retrive'))

@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    return render_template('edit.html',id = id)

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['dname']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update table1 set name = %s where id = %s",(name,id,))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('retrive'))

if __name__ == "__main__":
    app.run(debug = True)