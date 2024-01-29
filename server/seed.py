from app import app
from models import db, User, Meal, Ingredient

def seed_data():
    with app.app_context():
        
        db.drop_all()
        db.create_all()

        # Seed Users
        users = [
            User(username='user1', password_hash='password1', email='user1@example.com'),
            User(username='user2', password_hash='password2', email='user2@example.com'),
            User(username='user3', password_hash='password3', email='user3@example.com'),
            User(username='user4', password_hash='password4', email='user4@example.com'),
            User(username='user5', password_hash='password5', email='user5@example.com'),
            User(username='user6', password_hash='password6', email='user6@example.com'),
            User(username='user7', password_hash='password7', email='user7@example.com'),
            User(username='user8', password_hash='password8', email='user8@example.com'),
            User(username='user9', password_hash='password9', email='user9@example.com'),
            User(username='user10', password_hash='password10', email='user10@example.com'),
        ]

        db.session.add_all(users)
        db.session.commit()

        meals = []
        ingredients = []

        user_ids = [user.id for user in users]

        for user_id in user_ids:
            for meal_data in [
                {'title': 'Spaghetti Bolognese', 'description': 'Classic Italian dish', 'category': 'Pasta','image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiVy62R4n8Kq_CLdybgwDDIK6OGggWuiS2wQ&usqp=CAU'},
                {'title': 'Chicken Stir Fry', 'description': 'Healthy and delicious', 'category': 'Asian'},
                {'title': 'Vegetarian Pizza', 'description': 'Delicious veggie pizza', 'category': 'Pizza'},
                {'title': 'Grilled Salmon', 'description': 'Fresh and flavorful salmon', 'category': 'Seafood'},
                {'title': 'Caesar Salad', 'description': 'Classic Caesar salad', 'category': 'Salad'},
                {'title': 'Beef Tacos', 'description': 'Tasty beef tacos', 'category': 'Mexican'},
                {'title': 'Mushroom Risotto', 'description': 'Creamy mushroom risotto', 'category': 'Italian'},
                {'title': 'Shrimp Scampi', 'description': 'Garlic butter shrimp pasta', 'category': 'Seafood'},
                {'title': 'Vegetable Stir Fry', 'description': 'Fresh and crunchy vegetables', 'category': 'Asian'},
                {'title': 'Margherita Pizza', 'description': 'Classic margherita pizza', 'category': 'Pizza'},
                {'title': 'Meal 11', 'description': 'Description 11', 'category': 'Category 11'},
                {'title': 'Meal 12', 'description': 'Description 12', 'category': 'Category 12'},
                {'title': 'Meal 13', 'description': 'Description 13', 'category': 'Category 13'},
                {'title': 'Meal 14', 'description': 'Description 14', 'category': 'Category 14'},
                {'title': 'Meal 15', 'description': 'Description 15', 'category': 'Category 15'},
                {'title': 'Meal 16', 'description': 'Description 16', 'category': 'Category 16'},
                {'title': 'Meal 17', 'description': 'Description 17', 'category': 'Category 17'},
                {'title': 'Meal 18', 'description': 'Description 18', 'category': 'Category 18'},
                {'title': 'Meal 19', 'description': 'Description 19', 'category': 'Category 19'},
                {'title': 'Meal 20', 'description': 'Description 20', 'category': 'Category 20'},
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
