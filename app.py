from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
import secrets

# Generate a secure random key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


@app.route('/api')
def hello_world():
    # print(f"Generated secret key: {secret_key}")
    return 'Hello world!'

users = []
# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if any(user['username'] == username for user in users):
            flash('Username is already taken. Please choose a different one.', 'error')
        else:
            # Add the user to the list (in a real app, this is where you'd store it in a database)
            users.append({'username': username, 'password': password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match any registered user
        if any(user['username'] == username and user['password'] == password for user in users):
            flash('Login successful!', 'success')
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')



if __name__ == '__main__':
    app.run()