from flask import Blueprint, request, jsonify
from app.models import db, Hero, Power, HeroPower
from sqlalchemy.orm import joinedload

api = Blueprint('api', __name__)

def serialize_power(power):
    return {
        "id": power.id,
        "name": power.name,
        "description": power.description,
    }

def serialize_hero_power(hero_power):
    return {
        "strength": hero_power.strength,
        "hero_id": hero_power.hero_id,
        "power_id": hero_power.power_id,
        "power": serialize_power(hero_power.power)
    }

def serialize_hero(hero):
    return {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [serialize_hero_power(hp) for hp in hero.hero_powers]
    }

@api.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([serialize_hero(hero) for hero in heroes]), 200

@api.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.options(joinedload(Hero.hero_powers).joinedload(HeroPower.power)).get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(serialize_hero(hero)), 200

@api.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([serialize_power(power) for power in powers]), 200

@api.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(serialize_power(power)), 200

@api.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if 'description' in data:
        if len(data['description']) < 20:
            return jsonify({"errors": ["Description must be at least 20 characters long"]}), 422
        power.description = data['description']
    
    db.session.commit()
    return jsonify(serialize_power(power)), 200

@api.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    required_fields = ['strength', 'hero_id', 'power_id']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if data['strength'] not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}), 422

    # Check if hero and power exist
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    if not power:
        return jsonify({"error": "Power not found"}), 404

    hero_power = HeroPower(
        strength=data['strength'],
        hero_id=data['hero_id'],
        power_id=data['power_id']
    )
    
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(serialize_hero_power(hero_power)), 201
