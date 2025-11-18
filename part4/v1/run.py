from app import create_app
from flask import Flask, render_template

app = create_app()


@app.route('/api/v1/auth/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


