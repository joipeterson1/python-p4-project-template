#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Author, Book, User, book_user
from sqlalchemy import text

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Remove any existing data
        db.session.execute(text('DELETE FROM authors'))
        db.session.execute(text('DELETE FROM books'))
        db.session.execute(text('DELETE FROM users'))
        db.session.commit()

        Author.query.delete()
        Book.query.delete()
        User.query.delete()
        db.session.commit()

        # Add authors
        author1 = Author(name="J.K. Rowling")
        author2 = Author(name="George R.R. Martin")
        author3 = Author(name="J.R.R. Tolkien")

        # Add books
        book1 = Book(title="Harry Potter and the Sorcerer's Stone", author=author1)
        book2 = Book(title="Harry Potter and the Chamber of Secrets", author=author1)
        book3 = Book(title="A Game of Thrones", author=author2)
        book4 = Book(title="A Clash of Kings", author=author2)
        book5 = Book(title="The Fellowship of the Ring", author=author3)

        # Add users
        user1 = User(username="alice")
        user2 = User(username="bob")
        user3 = User(username="charlie")

        # Add authors, books, and users to the session
        db.session.add_all([author1, author2, author3, book1, book2, book3, book4, book5, user1, user2, user3])
        db.session.commit()

        # Create many-to-many relationships (book-user associations with comments)
        # Alice comments on Harry Potter books
        db.session.execute(book_user.insert().values(book_id=book1.id, user_id=user1.id, comment="Amazing start to the series!"))
        db.session.execute(book_user.insert().values(book_id=book2.id, user_id=user1.id, comment="Loved the plot twists!"))

        # Bob comments on Game of Thrones books
        db.session.execute(book_user.insert().values(book_id=book3.id, user_id=user2.id, comment="The intrigue is fantastic."))
        db.session.execute(book_user.insert().values(book_id=book4.id, user_id=user2.id, comment="Epic battles, but a slow start."))

        # Charlie comments on The Fellowship of the Ring
        db.session.execute(book_user.insert().values(book_id=book5.id, user_id=user3.id, comment="A beautiful world, slow pacing though."))

        # Commit all changes
        db.session.commit()

        print("Database seeded successfully!")

