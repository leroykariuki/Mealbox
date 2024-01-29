import os
from flask import Flask, make_response, jsonify, request, render_template
from models import db, User, Meal, Ingredient
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from faker import Faker  
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__, static_folder='../client/dist', template_folder='../client/dist', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/leroy/code/phase4/Mealbox/server/instance/endphase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1111'
app.config['JWT_SECRET_KEY'] = '1111'
jwt = JWTManager(app)
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)
FieldError = "Missing Required fields"

fake = Faker()
Faker.seed(123)

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.validate_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

def load_user_callback(identity):
    return User.query.get(identity)

class SeedDataResource(Resource):
    def get(self):
        seed_data()
        return {"message": "Seed data created successfully"}, 200

api.add_resource(SeedDataResource, '/seed-data')  

def seed_data():
    with app.app_context():
        # Drop and create tables
        db.drop_all()
        db.create_all()

    
        for _ in range(5):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)

        db.session.commit()

        users = User.query.all()
        for user in users:
            for _ in range(3):  
                meal = Meal(
                    title=fake.word(),
                    description=fake.sentence(),
                    category=fake.word(),
                    user_id=user.id
                )
                db.session.add(meal)
                db.session.flush()

                for _ in range(2): 
                    ingredient = Ingredient(
                        name=fake.word(),
                        quantity=fake.random_int(min=1, max=100),
                        unit=fake.word(),
                        meal_id=meal.id
                    )
                    db.session.add(ingredient)

        db.session.commit()

        print("Seed completed!")    


@app.route('/')
def home():
    return render_template('index.html')


class UsersResource(Resource):
    def get(self):
        user_list = []
        for user in User.query.all():
            user_dict = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            user_list.append(user_dict)

        response = make_response(
            jsonify(user_list),
            200
        )
        return response

    def post(self):
        user_data = request.get_json()
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')

        if not username or not email or not password:
            return {"error": FieldError}, 400

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        response_data = {
            "message": "New User created successfully",
            "user_id": new_user.id
        }

        return response_data, 201


api.add_resource(UsersResource, '/users')


class UserResource(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return user_data, 200
        else:
            return {"error": "User not found"}, 404


api.add_resource(UserResource, '/users/<int:id>')


class MealResource(Resource):
     def get(self, id=None):
        if id is None:
            meal_list = []
            for meal in Meal.query.all():
                meal_dict = {
                    "id": meal.id,
                    "title": meal.title,
                    "description": meal.description,
                    "category": meal.category,
                    "ingredients": []  
                }

                ingredients = Ingredient.query.filter_by(meal_id=meal.id).all()
                for ingredient in ingredients:
                    ingredient_data = {
                        "name": ingredient.name,
                        "quantity": ingredient.quantity,
                        "unit": ingredient.unit
                    }
                    meal_dict["ingredients"].append(ingredient_data)

                meal_list.append(meal_dict)

            response = make_response(
                jsonify(meal_list),
                200
            )
            return response
        else:
            meal = Meal.query.filter_by(id=id).first()
            if meal:
                meal_data = {
                    "id": meal.id,
                    "title": meal.title,
                    "description": meal.description,
                    "category": meal.category,
                    "ingredients": []
                }

                ingredients = Ingredient.query.filter_by(meal_id=meal.id).all()
                for ingredient in ingredients:
                    ingredient_data = {
                        "name": ingredient.name,
                        "quantity": ingredient.quantity,
                        "unit": ingredient.unit
                    }
                    meal_data["ingredients"].append(ingredient_data)

                return meal_data, 200
            else:
                return {"error": "Meal not found"}, 404
                
     def post(self):
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        image_url = request.form.get('image_url')  
        user_id = get_jwt_identity()

        if not title or not description or not category or not user_id:
            return {"error": FieldError}, 400

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        new_meal = Meal(title=title, description=description, category=category, image_url=image_url, user=user)
        db.session.add(new_meal)
        db.session.commit()

        response_data = {
            "message": "New Meal created successfully",
            "meal_id": new_meal.id
        }

        return response_data, 201


api.add_resource(MealResource, '/meal', '/meal/<int:id>')

class IngredientResource(Resource):
    def get(self, id=None):
        if id is None:
            ingredient_list = []
            for ingredient in Ingredient.query.all():
                ingredient_data = {
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "unit": ingredient.unit,
                    "meal_id": ingredient.meal_id
                }
                ingredient_list.append(ingredient_data)

            response = make_response(
                jsonify(ingredient_list),
                200
            )
            return response
        else:
            ingredient = Ingredient.query.filter_by(id=id).first()
            if ingredient:
                ingredient_data = {
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "unit": ingredient.unit,
                    "meal_id": ingredient.meal_id
                }
                return ingredient_data, 200
            else:
                return {"error": "Ingredient not found"}, 404

api.add_resource(IngredientResource, '/ingredient', '/ingredient/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
