"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite_Character, Favorite_Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"info":"Notfound"}), 404
    
    return jsonify(user.serialize()), 200

@app.route('/users/', methods=['GET'])
def get_all_users():
    users_query=User.query.all()
    users_list=list(map(lambda user:user.serialize(),users_query))
    return jsonify(users_list)

@app.route('/user',methods=['POST'])
def create_user():
    user_body = request.get_json()
    user_db = User(first_name=user_body["first_name"],
                 last_name=user_body["last_name"],
                 email=user_body["email"],
                 password=user_body["password"],
                 is_active=user_body["is_active"]
                 )
    db.session.add(user_db)
    db.session.commit()
    return jsonify(user_db.serialize()),201

@app.route('/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user_db = User.query.filter_by(id=user_id).first()
    if user_db is None:
        return jsonify({"info": "Not found"}), 404
    user_body = request.get_json()
    
    if "first_name" in user_body:
        user_db.first_name=user_body["first_name"]

    if "last_name" in user_body:
        user_db.last_name=user_body["last_name"]

    if "emai" in user_body:
        user_db.email=user_body["email"]

    if "password" in user_body: 
        user_db.password=user_body["password"]

    if "is_active" in user_body:
        user_db.is_active=user_body["is_active"]

    db.session.add(user_db)
    db.session.commit()
    return jsonify(user_db.serialize())

@app.route('/user/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):
    user_db = User.query.filter_by(id=user_id).first()
    if user_db is None:
        return jsonify({"info":"Notfound"}), 404
    db.session.delete(user_db)
    db.session.commit()
    return jsonify({"info":"user deleted"})

# endpoind personaje

@app.route('/character', methods=['GET'])
def get_all_character():
    character_query = Character.query.all()
    character_list = list(map(lambda character: character.serialize(), character_query))
    return jsonify(character_list)

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(character.serialize())

# endpoind planetas

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets_query = Planet.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), planets_query))
    return jsonify(planets_list)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(planet.serialize())

# endpoind Favoritos

# Get

@app.route('/users/favorites/', methods=['GET'])
def get_all_favorites():
    favorites_characters = Favorite_Character.query.all()
    favorites_planets = Favorite_Planet.query.all()
    
    favorites_characters_list = list(map(lambda favorite:favorite.serialize(), favorites_characters))
    favorites_planets_list=list(map(lambda favorite:favorite.serialize(), favorites_planets))
    
    return jsonify({
        "characters": favorites_characters_list,
        "planets": favorites_planets_list
    })




# post

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    favorite_planet = Favorite_Planet(user=user, planet=planet)
    db.session.add(favorite_planet)
    db.session.commit()
    return jsonify({"info": "Favorite added"})

@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    
    favorite_character = Favorite_Character(user=user, character=character)
    db.session.add(favorite_character)
    db.session.commit()
    return jsonify({"info": "Favorite character added"})

# Delete

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    favorite_planet = Favorite_Planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404
    
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"info": "Favorite planet deleted"})

@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    
    favorite_character = Favorite_Character.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite_character is None:
        return jsonify({"error": "Favorite character not found"}), 404
    
    db.session.delete(favorite_character)
    db.session.commit()
    return jsonify({"info": "Favorite character deleted"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
