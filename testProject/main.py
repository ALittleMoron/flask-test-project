from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# initial
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('blog/home.html')


if __name__ == "__main__":
    app.run(debug=True)
