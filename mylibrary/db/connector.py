"""
database connector implementation
"""

import configparser
from functools import cached_property

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL

from mylibrary.db import logger
from mylibrary.helpers.helpers import get_parameter
from mylibrary.models.book import BookModel


class BooksDBConnector:
    """
    A database connector for database books
    """

    def __init__(self, config: configparser):
        """
        Db connector
        """
        self.__config = config

    @property
    def __debug_db(self):
        """
        get debug flag from config if we should enable debug for the database or not
        """
        debug_db = get_parameter("DB", "debug", self.__config)
        if not debug_db:
            return False
        elif debug_db.lower() in ["true", "on", "yes", "1", "enabled", "enable", "t", "y"]:
            return True
        elif debug_db.lower() in ["false", "off", "no", "0", "disabled", "disable", "f", "n"]:
            return False
        raise Exception("Could not understand provided value",
                        "You provided a value that we cannot understand for DATABASE DEBUG")

    @cached_property
    def db_engine(self):
        """
        create engine
        """
        url = URL.create(
            drivername=get_parameter("DB", "driver", self.__config),
            username=get_parameter("DB", "username", self.__config),
            password=get_parameter("DB", "password", self.__config),
            host=get_parameter("DB", "host", self.__config),
            port=get_parameter("DB", "port", self.__config),
            database=get_parameter("DB", "db_name", self.__config)
        )
        logger.info("creation db engine")
        return create_engine(url, echo=self.__debug_db)

    def create_table(self) -> bool:
        """
        A method that checks if the database has the user_notifications table and creates if it doesn't exist.
        """
        if not inspect(self.db_engine).has_table(BookModel.__tablename__):
            logger.info("table %s does not exist in the database, attempting to create it", BookModel.__tablename__)
            try:
                BookModel.__table__.create(bind=self.db_engine)
                return True
            except Exception:
                logger.exception("Cannot create table %s", BookModel.__tablename__)
                return False
        else:
            logger.info("Table %s already exists", BookModel.__tablename__)
            return True
