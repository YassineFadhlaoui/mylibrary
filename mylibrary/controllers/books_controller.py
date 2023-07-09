"""
Books controller module
"""
import configparser
from dataclasses import asdict

from sqlalchemy.orm import Session

from mylibrary.controllers import logger
from mylibrary.db.connector import BooksDBConnector
from mylibrary.models.book import BookModel


class BooksController:
    """
    A simple controller that implements CRUD operations
    """
    def __init__(self, config: configparser):
        self.__config = config
        self.__db_engine = BooksDBConnector(self.__config).db_engine

    def get_all(self):
        """Read all entries from the database"""
        with Session(self.__db_engine) as session:
            logger.debug("Getting all books")
            all_books = session.query(BookModel).order_by(BookModel.finished).all()
            if all_books:
                return list(map(lambda book: asdict(book), all_books))
            return []

    def add(self, book: BookModel):
        """add book to DB"""
        with Session(self.__db_engine) as session:
            try:
                logger.info("checking if book '%s' already exists", book.title)
                _book = session.query(BookModel).filter(BookModel.title==book.title).one_or_none()
                if _book:
                    logger.info("book '%s' already exists", _book)
                    return False, "Book already exists"

                logger.info("adding book '%s'", book.title)
                session.add(book)
                session.commit()
                return True, None
            except Exception:
                logger.exception("Failed to add book")
                return False, "Error adding book"

    def get_currently_reading(self):
        """
        Add a user notification entry based on the dataclass Task
        """
        logger.debug("getting currently reading books")
        with Session(self.__db_engine) as session:
            currently_reading = session.query(BookModel).filter(BookModel.progress < 100)
            if currently_reading:
                return list(map(lambda book: asdict(book), currently_reading))
            return []

    def update(self, book: BookModel):
        """
        Update an already existing entry with the new data
        """
        logger.debug("Updating existing book with name '%s'", book.title)
        with Session(self.__db_engine) as session:
            logger.info("finding book '%s'", book.title)
            old_book_entry = session.get(BookModel, book.title)
            if old_book_entry:
                if book.progress:
                    logger.info("updating progress for '%s'", book.title)
                    old_book_entry.progress = book.progress

                old_book_entry.notes = book.notes
                logger.info("committing changes for '%s'", book.title)
                session.commit()
                return True
            return False

    def delete(self, title: str):
        """
        Remove a user notification entry using the primary key uname
        """
        logger.debug("Deleting book with title '%s'", title)
        with Session(self.__db_engine) as session:
            book = session.get(BookModel, title)
            if not book:
                return None
            session.delete(book)
            session.commit()
            return True
