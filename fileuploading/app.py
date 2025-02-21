from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import base64

app = Flask(__name__)

app.secret_key = "!25/^54662Skssfgab&%vcdvjs"

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_PASSWORD"] = '12345'
app.config["MYSQL_DB"] = 'armi'

db = MySQL(app)

@app.route('/display')
def display():
    cursor = db.connection.cursor()
    cursor.execute("SELECT id,filename, data FROM new_table")
    displaydata = cursor.fetchall()
    cursor.close()

    # Encode image data as base64
    encoded_images = []
    for upload in displaydata:
        image_id, filename, image_data = upload[0], upload[1], upload[2]
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        encoded_images.append({'id': image_id, 'filename': filename, 'encoded_image': encoded_image})
    
    return render_template('display.html', encoded_images=encoded_images)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO new_table (filename, data) VALUES (%s, %s)", (file.filename, file.read()))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, filename FROM new_table")
    uploads = cursor.fetchall()
    cursor.close()

    return render_template('index.html', uploads =uploads)

@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    return render_template('edit.html',upload_id = id)

@app.route('/delete/<upload_id>')
def delete(upload_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM new_table WHERE id = %s", (upload_id,))
    db.connection.commit()
    cursor.close()
    return redirect(url_for('display'))

@app.route('/update/<upload_id>', methods=['GET', 'POST'])
def update(upload_id):
    if request.method == 'POST':
        new_filename = request.files["file"]
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE new_table SET filename = %s,data = %s WHERE id = %s", (new_filename.filename,new_filename.read(),upload_id))
        db.connection.commit()
        cursor.close()
        return redirect(url_for('display'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, filename FROM new_table WHERE id = %s", (upload_id,))
    upload = cursor.fetchone()
    cursor.close()

    if upload:
        return render_template('display.html', upload=upload)
    else:
        return 'File not found'

if __name__ == '__main__':
    app.run(debug=True)