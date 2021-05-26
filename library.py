from flask import Flask, render_template, request, redirect
from flask.ext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'BooksDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        book = request.form['book']
        # search by author or book
        cursor.execute("SELECT name, author from Book WHERE name LIKE %s OR author LIKE %s", (book, book))
        conn.commit()
        data = cursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and book == 'all':
            cursor.execute("SELECT name, author from Book")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
