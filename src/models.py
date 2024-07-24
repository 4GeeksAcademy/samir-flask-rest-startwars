from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user" 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False)
    last_name = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)
    is_active = db.Column(db.Boolean(), unique=False)

    

    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,  
            "last_name": self.last_name
        }
    
class Character(db.Model):
   __tablename__ = "character"
   id = db.Column(db.Integer, primary_key=True)
   first_name =db.Column(db.String(120))
   species =db.Column(db.String(120))
   homeworld =db.Column(db.String(120))
   age =db.Column(db.String(120))
   discipline =db.Column(db.String(120))

   def __repr__(self):
        return '<Character %r>' % self.first_name

   def serialize(self):
      return {"id": self.id,
              "first_name": self.first_name,
              "species": self.species,
              "homeworld": self.homeworld,
              "age": self.age,
              "discipline": self.discipline
              }
   
class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(200))
    surface = db.Column(db.String(200))
    population = db.Column(db.String(200))
    climate = db.Column(db.String(200))

    def __repr__(self):
        return 'Planet %r>' % self.name
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "surface": self.surface,
            "population": self.description,
            "climate": self.climate
        }
    
class Favorite_Planet(db.Model):
    __tablename__ = "favorite_planet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User, backref="favorites_planet")
    planet_id=db.Column(db.Integer, db.ForeignKey("planets.id"))
    planet=db.relationship(Planet)


    def __repr__(self):
        return f"{self.user.first_name} likes {self.planet.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "planet": self.planet.name
        }

class Favorite_Character(db.Model):
    __tablename__ = "favorite_character"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User, backref="favorites_character")
    character_id=db.Column(db.Integer, db.ForeignKey("character.id"))
    character=db.relationship(Character)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "planet": self.character.first_name
        }
