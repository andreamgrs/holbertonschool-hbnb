from app import create_app
from flask import Flask, render_template
from flask_cors import CORS

app = create_app()
CORS(app)

@app.route('/api/v1/auth/login')
def login():
    return render_template('login.html')

@app.route('/api/v1/index')
def index():
    return render_template('index.html')


@app.route('/api/v1/place/<place_id>')
def place():
    return render_template('place.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


