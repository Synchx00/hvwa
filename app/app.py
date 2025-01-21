from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': 'db',
    'user': 'root',
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init')
def init_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create user table if it doesn't exist
        print("Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        """)
        print("Users table created or already exists.")

        # Insert dummy data if the table is empty
        print("Checking if users table is empty...")
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count == 0:
            print("Inserting dummy data...")
            users = [
                ('admin', 'apahayoo'),
                ('user1', 'password1'),
                ('user2', 'password2'),
                ('user3', 'password3'),
                ('user4', 'password4'),
                ('user5', 'password5')
            ]
            cursor.executemany("INSERT INTO users (username, password) VALUES (%s, %s)", users)
            conn.commit()
            print("Dummy data inserted.")
        else:
            print("Users table already has data.")
        
        return jsonify(message="Database initialized"), 200
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify(error=str(err)), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

@app.route('/login', methods=['POST'])
def login():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            return jsonify(message="Login successful"), 200
        else:
            return jsonify(message="Invalid username or password"), 401
    except mysql.connector.Error as err:
        return jsonify(error=str(err)), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.cli.command('init-db')
def init_db_command():
    """CLI command to initialize the database."""
    init_db()
    print("Database initialized via CLI command.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)