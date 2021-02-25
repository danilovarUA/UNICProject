import os

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_PATH = "sqlite:///{}/data/database.db?check_same_thread=False".format(os.path.dirname(os.path.abspath(
    __file__)))
engine = create_engine(DATABASE_PATH, echo=False)
Base = declarative_base()
session_maker = sessionmaker(bind=engine)
session = session_maker()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return "User(id={}, name={}, password={})".format(self.id, self.name, self.password)


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "Movie(id={}, name={})".format(self.id, self.name)


class Rating(Base):
    __tablename__ = 'ratings'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    mark = Column(Integer)

    def __repr__(self):
        return "Rating(user_id={}, movie_id={}, mark={})".format(self.user_id, self.movie_id, self.mark)


class Recommendation(Base):
    __tablename__ = 'recommendations'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    expected_mark = Column(Float)

    def __repr__(self):
        return "Recommendation(user_id={}, movie_id={}, mark={})".format(
            self.user_id, self.movie_id, self.expected_mark)


if __name__ == "__main__":
    #Base.metadata.drop_all(engine)
    #Base.metadata.create_all(engine)
    print(session.query(Recommendation).all())
