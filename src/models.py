from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    gender: Mapped[str | None] = mapped_column(String(40))
    birth_year: Mapped[str | None] = mapped_column(String(40))
    eye_color: Mapped[str | None] = mapped_column(String(40))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    climate: Mapped[str | None] = mapped_column(String(120))
    terrain: Mapped[str | None] = mapped_column(String(120))
    population: Mapped[str | None] = mapped_column(String(120))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }


class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    __table_args__ = (
        UniqueConstraint("user_id", "people_id", name="uq_user_people"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    user = relationship("User", backref="favorite_people")
    people = relationship("People")

    def serialize(self):
        return {
            "id": self.id,
            "type": "people",
            "people": self.people.serialize(),
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    __table_args__ = (
        UniqueConstraint("user_id", "planet_id", name="uq_user_planet"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user = relationship("User", backref="favorite_planets")
    planet = relationship("Planet")

    def serialize(self):
        return {
            "id": self.id,
            "type": "planet",
            "planet": self.planet.serialize(),
        }