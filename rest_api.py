from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database configuration
host = 'localhost'
username = 'root'
password = ''
database = 'chatapp'

# Create a database connection
db = pymysql.connect(host=host, user=username, password=password, db=database, cursorclass=pymysql.cursors.DictCursor)

# Define the HTTP methods
methods = ['GET', 'POST', 'PUT', 'DELETE']

@app.route('/api/users', methods=methods)
def api_users():
    method = request.method

    # Check if the method is supported
    if method not in methods:
        return jsonify({'message': 'Invalid HTTP method'}), 405

    if method == 'GET':
        # Retrieve data
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)

    elif method == 'POST':
        # Create a new record
        new_record = request.get_json()
        cursor = db.cursor()
        insert_query = "INSERT INTO users (unique_id, fname, lname, email, password, img, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (
            new_record['unique_id'],
            new_record['fname'],
            new_record['lname'],
            new_record['email'],
            new_record['password'],
            new_record['img'],
            new_record['status']
        ))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Record created'})

    elif method == 'PUT':
        # Update a record
        updated_record = request.get_json()
        cursor = db.cursor()
        update_query = "UPDATE users SET unique_id = %s, fname = %s, lname = %s, email = %s, password = %s, img = %s, status = %s WHERE user_id = %s"
        cursor.execute(update_query, (
            updated_record['unique_id'],
            updated_record['fname'],
            updated_record['lname'],
            updated_record['email'],
            updated_record['password'],
            updated_record['img'],
            updated_record['status'],
            updated_record['user_id']
        ))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Record updated'})

    elif method == 'DELETE':
        # Delete a record
        record_to_delete = request.get_json()
        cursor = db.cursor()
        delete_query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(delete_query, (record_to_delete['user_id'],))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Record deleted'})

if __name__ == '__main__':
    app.run()
