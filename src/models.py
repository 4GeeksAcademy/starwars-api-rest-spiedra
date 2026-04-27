from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    people_id: Mapped[int] = mapped_column(
        ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates="favorites")
    people: Mapped['People'] = relationship(back_populates="favorites")
    planet: Mapped['Planet'] = relationship(back_populates="favorites")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
        }


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")
    profile: Mapped['Profile'] = relationship(back_populates='user')
    posts: Mapped[List['Posts']] = relationship(back_populates='author')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "profile": self.profile.serialize() if self.profile else None,
            "posts": [post.serialize() for post in self.posts] if self.posts else None,
            "favorites": [fav.serialize() for fav in self.favorites] if self.favorites else None

        }


class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(100), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)
    mass: Mapped[float] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(String(20), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "favorites": [fav.serialize() for fav in self.favorites] if self.favorites else None
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[int] = mapped_column(unique=False, nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)
    surface_water: Mapped[int] = mapped_column(nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "favorites": [fav.serialize() for fav in self.favorites] if self.favorites else None
        }


class Profile(db.Model):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='profile')

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "user": self.user.id if self.user else None,
            "favorites": [fav.serialize() for fav in self.favorites] if self.favorites else None
        }


class Posts(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    author: Mapped['User'] = relationship(back_populates='posts')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "author": self.author.id if self.author else None,
            "favorites": [fav.serialize() for fav in self.favorites] if self.favorites else None
        }
