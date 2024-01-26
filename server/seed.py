from app import app
from models import db, User, Meal, Ingredient

def seed_data():

    with app.app_context():
        # Drop and create tables
        db.drop_all()
        db.create_all()

        # Seed Users
        users = [
            User(username='user1', password_hash='password1', email='user1@example.com'),
            User(username='user2', password_hash='password2', email='user2@example.com'),
            
        ]

        db.session.add_all(users)
        db.session.commit()

    
        meal = []
        ingredients = []

        user_ids = [user.id for user in users]

        for user_id in user_ids:
            for meal_data in [
                {'title': 'Spaghetti Bolognese', 'description': 'Classic Italian dish', 'category': 'Pasta'},
                {'title': 'Chicken Stir Fry', 'description': 'Healthy and delicious', 'category': 'Asian'},
                
            ]:
                meal = Meal(
                    title=meal_data['title'],
                    description=meal_data['description'],
                    category=meal_data['category'],
                    user_id=user_id,
                )
                db.session.add(meal)
                db.session.flush()

                for ingredient_data in [
                    {'name': 'Pasta', 'quantity': 200, 'unit': 'grams'},
                    {'name': 'Ground Beef', 'quantity': 300, 'unit': 'grams'},
                    
                ]:
                    ingredient = Ingredient(
                        name=ingredient_data['name'],
                        quantity=ingredient_data['quantity'],
                        unit=ingredient_data['unit'],
                        meal_id=meal.id,
                    )
                    ingredients.append(ingredient)

        db.session.add_all(ingredients)
        db.session.commit()

        print("Seed completed!")

if __name__ == "__main__":
    seed_data()
