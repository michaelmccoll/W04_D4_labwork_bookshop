from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import book_repository, author_repository
from models.book import Book

books_blueprint = Blueprint("books",__name__)


@books_blueprint.route('/books')
def books():
    books = book_repository.select_all()                            
    return render_template("books/index.html", all_books=books)  

@books_blueprint.route('/books/<id>/delete', methods=['POST'])
def delete_book(id):
    book_repository.delete(id)
    return redirect('/books')

@books_blueprint.route('/books/new')
def new_book():
    authors = author_repository.select_all()
    return render_template('books/new.html', all_authors=authors)

@books_blueprint.route('/books', methods=['POST'])
def create_book():
    title = request.form["title"]
    description = request.form["description"]
    author_id = request.form["author"]
    theme = request.form["theme"]
    author = author_repository.select(author_id)
    book = Book(title, description, author, theme)
    book_repository.save(book)
    return redirect('/books')  

@books_blueprint.route('/books/<id>')
def show_book(id):                                            
    book = book_repository.select(id)                       
    return render_template('/books/show.html', selected_book=book)  


@books_blueprint.route('/books/<id>/edit', methods=['GET'])
def edit_book(id):
    book = book_repository.select(id)
    authors = author_repository.select_all()
    return render_template('books/edit.html', book = book, all_authors = authors)

@books_blueprint.route('/books/<id>', methods=['POST'])
def update_book(id):
    title = request.form['title']
    author_id = request.form['author_id']
    description = request.form['description']
    theme = request.form['theme']
    author = author_repository.select(author_id)
    book = Book(title, description, author, theme, id)
    book_repository.update(book)
    return redirect('/books')