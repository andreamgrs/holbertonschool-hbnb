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


@app.route('/api/v1/place')
def place():
    return render_template('place.html')

@app.route('/api/v1/add_review')
def add_review():
    return render_template('add_review.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


