from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'schooldb'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()

    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        student_number = request.form['student_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        gender = request.form['gender']
        birthday = request.form['birthday']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (student_number, first_name, last_name, middle_name, gender, birthday) VALUES (%s, %s, %s, %s, %s, %s)",
                    (student_number, first_name, last_name, middle_name, gender, birthday))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        student_number = request.form['student_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        gender = request.form['gender']
        birthday = request.form['birthday']
        cur.execute("UPDATE students SET student_number=%s, first_name=%s, last_name=%s, middle_name=%s, gender=%s, birthday=%s WHERE id=%s",
                    (student_number, first_name, last_name, middle_name, gender, birthday, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cur.fetchone()
        cur.close()

        return render_template('students_edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__name__':
    app.run(debug=True)
