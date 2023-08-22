#!/usr/bin/python3
""" summary """
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ DBStorage class """

    __engine = None
    __session = None

    def __init__(self):
        """ init function """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ summary
        Args:
            cls type, optional: description. defaults to None
        """
        _dict = {}
        query = []
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls).all()

        if cls is None:
            query += self.__session.query(State).all()
            query += self.__session.query(User).all()
            query += self.__session.query(City).all()
            query += self.__session.query(Amenity).all()
            query += self.__session.query(Place).all()
            query += self.__session.query(Review).all()

        for val in query:
            key = "{}.{}".format(val.__class__.__name__, val.id)
            _dict[key] = val
        return _dict

    def new(self, obj):
        """ add object to db """
        self.__session.add(obj)

    def save(self):
        """ commit all changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete obj from db """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ reload all tables """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        self.__session.close()
