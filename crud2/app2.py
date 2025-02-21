from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app2 = Flask(__name__)

app2.secret_key = "ABC"

app2.config['MYSQL_HOST'] = "localhost"
app2.config['MYSQL_USER'] = "root"
app2.config['MYSQL_PASSWORD'] = "12345"
app2.config['MYSQL_PORT'] = 3306
app2.config['MYSQL_DB'] = "sql_task1"

mysql = MySQL(app2)

@app2.route("/Retrive2")
def retrive2():
    coursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    coursor.execute("select * from task")
    store = coursor.fetchall()
    print(store)
    return render_template('retrive2.html',store = store)

@app2.route("/create2",methods = ['GET','POST'])
def create2():
    return render_template('create2.html')

@app2.route("/store",methods = ['GET','POST'])
def store():
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form['description']
        date = request.form['date']
        status = request.form['status']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into task(subject,description,date,status) values(%s,%s,%s,%s)",(subject,description,date,status,))

        mysql.connection.commit()

        cursor.close()
    return redirect(url_for('create2'))

@app2.route('/delete/<int:task_id>')
def delete(task_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("Delete from task where task_id = %s",(task_id,))
    mysql.connection.commit()
    return redirect(url_for('retrive2'))

@app2.route("/edit2/<int:task_id>",methods = ['GET','POST'])
def edit2(task_id):
    return render_template('edit2.html',task_id = task_id)

@app2.route('/update/<int:task_id>',methods = ['GET','POST'])
def update(task_id):
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form['description']
        date = request.form['date']
        status = request.form['status']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("update task set subject = %s,description=%s,date=%s,status=%s where task_id = %s",(subject,description,date,status,task_id,))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for('retrive2'))

if __name__ == "__main__":
    app2.run(debug = True)