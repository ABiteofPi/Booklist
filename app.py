
#importing libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#setting up flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

#defining book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publicationyear = db.Column(db.Integer, nullable=False)

#creating an index route to redirect to the two required routes
@app.route('/')
def indexpage():
    return render_template('index.html')

#creating route /books that would show the list of books added to the db
@app.route('/books')
def listbooks():
    books = Book.query.all()
    return render_template('list.html', books=books)

#creating route /add_book that lets users add books using title, author and publication year to the db
@app.route('/add_book', methods=['GET', 'POST'])
def addbook():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pubyear = request.form['pubyear']

        new_book = Book(title=title, author=author, publicationyear=pubyear)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('listbooks'))

    return render_template('add.html')


#context error did occur and adding the two additional lines here fixed it
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
