from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship

from config import db

book_user = db.Table('book_user',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('comment', db.String(255), nullable=False)
)

# Author Model
class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-users.author', '-users.books')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship('Book', back_populates='author', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Author {self.name}>'

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name cannot be empty')
        if len(name) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return name


# Book Model
class Book(db.Model, SerializerMixin):
    __tablename__= 'books'

    serialize_rules = ('-user.book',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    author = db.relationship('Author', back_populates="books")
    users = db.relationship('User', secondary=book_user, back_populates='books')

    def __repr__(self):
        return f'<Book {self.title}>'

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title cannot be empty')
        if len(title) < 3:
            raise ValueError('Title must be at least 3 characters long')
        return title


# User Model
class User(db.Model, SerializerMixin):
    __tablename__= 'users'

    serialize_rules = ('-books.users', '-author.users')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    books = db.relationship('Book', secondary=book_user, back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username cannot be empty')
        if len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return username
