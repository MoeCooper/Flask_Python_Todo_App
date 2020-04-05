from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jeonju123@localhost/flask_todo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# creates models, similar with mongoose
class Todo(db.Model):
    __tablename__ = 'Todos'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    data_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']

        if task_content == '':
            return render_template('index.html', message='Please enter a task')

        if db.session.query(Todo).filter(Todo.content == task_content).count() == 0:
            # add data to database
            data = Todo(task_content)
            db.session.add(data)
            db.session.commit()
            return render_template('index.html', message="Added Task!")
    else:

        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
