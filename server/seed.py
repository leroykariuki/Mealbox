# seed.py
from app import app, db, User, Meal, Ingredient
from faker import Faker

fake = Faker()

def seed_data():
    with app.app_context():
        # Drop and create tables
        db.drop_all()
        db.create_all()

        # Seed Users
        users = [
            User(username=fake.user_name(), password_hash=fake.password(), email=fake.email()),
            User(username=fake.user_name(), password_hash=fake.password(), email=fake.email()),
        ]

        db.session.add_all(users)
        db.session.commit()

        meals = []
        ingredients = []

        user_ids = [user.id for user in users]

        for user_id in user_ids:
            for _ in range(5):  
                meal = Meal(
                    title=fake.word(),
                    description=fake.sentence(),
                    category=fake.word(),
                    user_id=user_id,
                )
                db.session.add(meal)
                db.session.flush()

                for _ in range(3):  
                    ingredient = Ingredient(
                        name=fake.word(),
                        quantity=fake.random_int(1, 100),
                        unit=fake.word(),
                        meal_id=meal.id,
                    )
                    ingredients.append(ingredient)

        db.session.add_all(ingredients)
        db.session.commit()

        print("Seed completed!")

if __name__ == "__main__":
    seed_data()
