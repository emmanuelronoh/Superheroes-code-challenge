import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://super:12345@localhost:5432/superhero')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

