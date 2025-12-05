from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"

# simple in-memory store: { email: { first, last, password } }
users = {}

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
	# if already logged in, go to home
	if session.get('user'):
		return redirect(url_for('home'))
	return render_template('login.html')

# login form POST handler - simple demo auth (no real auth)
@app.route('/api/login', methods=['POST'])
def api_login():
	email = request.form.get('email')
	password = request.form.get('password')
	# very basic check: require non-empty fields; replace with real auth
	if email and password:
		session['user'] = {'email': email}
		return redirect(url_for('home'))
	flash('Please provide email and password')
	return redirect(url_for('login'))

@app.route('/api/signup', methods=['POST'])
def api_signup():
    first = request.form.get('first_name', '').strip()
    last = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not (first and last and email and password):
        flash('Please fill in all fields.')
        return redirect(url_for('signup'))

    if email in users:
        flash('An account with that email already exists. Please login.')
        return redirect(url_for('login'))

    # create user (replace with real DB in production)
    users[email] = {
        'first_name': first,
        'last_name': last,
        'password': password
    }

    # after successful signup, redirect user to the login page
    return redirect(url_for('login'))

@app.route('/home')
def home():
	# require login
	if not session.get('user'):
		return redirect(url_for('login'))
	user = session.get('user')
	return render_template('home.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
