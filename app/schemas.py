from .models import Hero, Power, HeroPower

class PowerSchema:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def serialize_list(cls, powers):
        return [power.serialize() for power in powers]


class HeroPowerSchema:
    def __init__(self, strength, hero_id, power_id, power):
        self.strength = strength
        self.hero_id = hero_id
        self.power_id = power_id
        self.power = power  

    def serialize(self):
        return {
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'power': self.power.serialize()  
        }

    @classmethod
    def serialize_list(cls, hero_powers):
        return [hero_power.serialize() for hero_power in hero_powers]


class HeroSchema:
    def __init__(self, id, name, super_name, hero_powers):
        self.id = id
        self.name = name
        self.super_name = super_name
        self.hero_powers = hero_powers  

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'hero_powers': HeroPowerSchema.serialize_list(self.hero_powers)
        }

    @classmethod
    def serialize_list(cls, heroes):
        return [hero.serialize() for hero in heroes]
