import os
from flask import Flask, make_response, jsonify, request, render_template, session
from models import db, User, Meal, Ingredient
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__, static_folder='../client/dist', template_folder='../client/dist', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/leroy/code/phase-2/sample/server/instance/endphase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)
FieldError = "Missing Required fields"

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
                }
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
                    "image_url": meal.image_url  
                }
                return meal_data, 200
            else:
                return {"error": "Meal not found"}, 404

    def post(self):
        meal_data = request.get_json()
        title = meal_data.get('title')
        description = meal_data.get('description')
        category = meal_data.get('category')
        image_url = meal_data.get('image_url') 
        user_id = meal_data.get('user_id')  

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
                ingredient_dict = {
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "unit": ingredient.unit
                }
                ingredient_list.append(ingredient_dict)

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
                    "unit": ingredient.unit
                }
                return ingredient_data, 200
            else:
                return {"error": "Ingredient not found"}, 404
    

api.add_resource(IngredientResource, '/ingredient', '/ingredient/<int:id>')

@app.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        user_data = request.get_json()
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')

        if not username or not email or not password:
            return jsonify({"error": FieldError}), 400

        new_user = User(username=username, email=email, password_hash=password)  

        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id

        return jsonify({"message": "New User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        login_data = request.get_json()
        username = login_data.get('username')
        password = login_data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.validate_password(password):  
            session['user_id'] = user.id
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
