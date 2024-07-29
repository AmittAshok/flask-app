from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configuration from environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Fetch form data
            userDetails = request.form
            name = userDetails.get('name')
            email = userDetails.get('email')
            
            if not name or not email:
                return 'Error: Name and email are required', 400
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()
            return 'Success'
        except Exception as e:
            return f'Error: {str(e)}', 500
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

