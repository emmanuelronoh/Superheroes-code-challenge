from app import create_app, db
from .models import Hero, Power, HeroPower

app = create_app()

heroes_data = [
    {"name": "Chebet", "super_name": "The Swift"},
    {"name": "Kipkoech", "super_name": "The Strong"},
    {"name": "Cherono", "super_name": "The Fearless"},
    {"name": "Kibet", "super_name": "The Watchful"},
]

powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"},
]

hero_powers_data = [
    {"strength": "Strong", "hero_id": 1, "power_id": 1},  
    {"strength": "Average", "hero_id": 2, "power_id": 2}, 
    {"strength": "Weak", "hero_id": 3, "power_id": 3},   
    {"strength": "Strong", "hero_id": 4, "power_id": 4},  
    
]

def seed_database():
    with app.app_context():
        db.drop_all()  
        db.create_all()

        # Insert heroes
        for hero in heroes_data:
            new_hero = Hero(**hero)
            db.session.add(new_hero)
        
        # Insert powers
        for power in powers_data:
            new_power = Power(**power)
            db.session.add(new_power)

        db.session.commit()  # Commit to save heroes and powers

        # Insert hero powers
        for hero_power in hero_powers_data:
            new_hero_power = HeroPower(**hero_power)
            db.session.add(new_hero_power)

        db.session.commit()  # Commit to save hero powers

        print("Database seeded!")

if __name__ == "__main__":
    seed_database()
