# Required Packages
from sqlalchemy import create_engine, Column, Integer, VARCHAR, ForeignKey, TEXT, text
from sqlalchemy.orm import Session, DeclarativeBase, relationship

import pandas as pd
import numpy as np
import os
import sys

# Get Tables Directory
try:
    directory = sys.argv[1]
except:
    directory = 'Output'

# Get tables Data
movie_table = pd.read_csv(os.path.join(directory, 'movie_table.csv')).drop_duplicates().replace({np.nan: None})
person_table = pd.read_csv(os.path.join(directory, 'person_table.csv')).drop_duplicates().replace({np.nan: None})
crew_table = pd.read_csv(os.path.join(directory, 'crew_table.csv')).drop_duplicates().replace({np.nan: None})

crew_table['role'].replace('Directors','Director',inplace=True)
crew_table['role'].replace('Writers','Writer',inplace=True)

cast_table = pd.read_csv(os.path.join(directory, 'cast_table.csv')).drop_duplicates().replace({np.nan: None})
genre_table = pd.read_csv(os.path.join(directory, 'genre_table.csv')).drop_duplicates().replace({np.nan: None})
country_table = pd.read_csv(os.path.join(directory, 'country_table.csv')).drop_duplicates().replace({np.nan: None})
language_table = pd.read_csv(os.path.join(directory, 'language_table.csv')).drop_duplicates().replace({np.nan: None})
storyline_table = pd.read_csv(os.path.join(directory, 'storyline_table.csv')).drop_duplicates().replace({np.nan: None})

movie_table = movie_table.to_dict(orient='records')
person_table = person_table.to_dict(orient='records')
crew_table = crew_table.to_dict(orient='records')
cast_table = cast_table.to_dict(orient='records')
genre_table = genre_table.to_dict(orient='records')
country_table = country_table.to_dict(orient='records')
language_table = language_table.to_dict(orient='records')
storyline_table = storyline_table.to_dict(orient='records')

# Creating engine and Database

engine = create_engine('mysql+pymysql://root:Zahra1376@localhost/')
conn = engine.connect()

DB_NAME = 'IMDB_mini'

with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
    conn.execute(text(f"USE {DB_NAME}"))

class Base(DeclarativeBase):
    pass

engine = create_engine(f'mysql+pymysql://root:Zahra1376@localhost/{DB_NAME}')
conn = engine.connect()

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(VARCHAR(8), primary_key=True)
    title = Column(VARCHAR(128))
    year = Column(Integer)
    runtime = Column(Integer)
    parental_guide = Column(VARCHAR(8))
    gross_us_canada = Column(Integer, nullable=True)

    # Define relationships
    crews = relationship("Crew", back_populates="movie")
    casts = relationship("Cast", back_populates="movie")
    genres = relationship("Genre", back_populates="movie")
    languages = relationship("Language", back_populates="movie")
    storylines = relationship("Storyline", back_populates="movie")
    countries = relationship("Country", back_populates="movie")

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(VARCHAR(8), primary_key=True)
    name = Column(VARCHAR(32))

    # Define relationships
    crews = relationship("Crew", back_populates="person")
    casts = relationship("Cast", back_populates="person")

class Crew(Base):
    __tablename__ = "crews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(VARCHAR(8), ForeignKey('movies.id'))
    person_id = Column(VARCHAR(8), ForeignKey('persons.id'))
    role = Column(VARCHAR(8))

    # Define relationships
    movie = relationship("Movie", back_populates="crews")
    person = relationship("Person", back_populates="crews")

class Cast(Base):
    __tablename__ = "casts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(VARCHAR(8), ForeignKey('movies.id'))
    person_id = Column(VARCHAR(8), ForeignKey('persons.id'))

    # Define relationships
    movie = relationship("Movie", back_populates="casts")
    person = relationship("Person", back_populates="casts")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(VARCHAR(8), ForeignKey('movies.id'))
    genre = Column(VARCHAR(16))

    # Define relationships
    movie = relationship("Movie", back_populates="genres")

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(VARCHAR(8), ForeignKey('movies.id'))
    country = Column(VARCHAR(16))

    # Define relationships
    movie = relationship("Movie", back_populates="countries")

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(VARCHAR(8), ForeignKey('movies.id'))
    language = Column(VARCHAR(225))

    # Define relationships
    movie = relationship("Movie", back_populates="languages")

class Storyline(Base):
    __tablename__ = "storylines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(VARCHAR(8), ForeignKey('movies.id'))
    content = Column(TEXT)

    # Define relationships
    movie = relationship("Movie", back_populates="storylines")

# Create tables
Base.metadata.create_all(engine)

# Creating a session in order to insert data to the database tables:
session = Session(engine)

try:
    # Inserting data to database tables:

    # Movie
    for mo in movie_table:
        movie_obj = Movie(
            id=mo['id'],
            title=mo['title'],
            year=int(mo['year']),
            runtime=int(mo['runtime']),
            parental_guide=mo['parental_guide'],
            gross_us_canada=mo['gross_us_canada']
        )
        session.add(movie_obj)

    # Crew
    for cr in crew_table:
        crew_obj = Crew(
            movie_id=cr['movie_id'],
            person_id=cr['person_id'],
            role=cr['role']
        )
        session.add(crew_obj)

    # Cast
    for ca in cast_table:
        cast_obj = Cast(
            movie_id=ca['movie_id'],
            person_id=ca['person_id']
        )
        session.add(cast_obj)

    # Genre
    for ge in genre_table:
        genre_obj = Genre(
            movie_id=ge['movie_id'],
            genre=ge['genre']
        )
        session.add(genre_obj)
    
    # Country
    for co in country_table:
        country_obj = Country(
            movie_id=co['movie_id'],
            country=co['country']
        )
        session.add(country_obj)
    
    # Language
    for la in language_table:
        language_obj = Language(
            movie_id=la['movie_id'],
            language=la['language']
        )
        session.add(language_obj)
    
    # Storyline
    for st in storyline_table:
        storyline_obj = Storyline(
            movie_id=st['movie_id'],
            content=st['content']
        )
        session.add(storyline_obj)

    # Person
    for pe in person_table:
        person_obj = Person(
            id=pe['id'],
            name=pe['name']
        )
        session.add(person_obj)

    session.commit()

except Exception as e:
    print(f"Error: {e}")
    session.rollback()

finally:
    session.close()
