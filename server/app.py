from flask import Flask, make_response, jsonify, request, render_template, session
from models import db, User, Meal, Ingredient
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)
FieldError = "Missing Required fields"

@app.route('/')
def home():
    return render_template('index.html')

# route to get all meals
@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    mealsdata = [
        {
            "id": meal.id,
            "title": meal.title,
            "description": meal.description,
            "category": meal.category,
            "created_at": meal.created_at,
            "updated_at": meal.updated_at,
            "image": meal.image
        }
        for meal in meals
    ]
    return jsonify(mealsdata)

# route to get a specific meal by its ID
@app.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if meal:
        mealdata = {
            "id": meal.id,
            "title": meal.title,
            "description": meal.description,
            "category": meal.category,
            "created_at": meal.created_at,
            "updated_at": meal.updated_at,
            "image": meal.image
        }
        return jsonify(mealdata)
    else:
        return jsonify({"error": "Meal not found"}), 404

# route to create a new meal
@app.route('/meals', methods=['POST'])
def create_meal():
    meal_data = request.get_json()
    title = meal_data.get('title')
    description = meal_data.get('description')
    category = meal_data.get('category')
    image = meal_data.get('image')

    if not title or not description or not category:
        return jsonify({"error": FieldError}), 400

    new_meal = Meal(title=title, description=description, category=category, image=image)
    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message": "New Meal created successfully"}), 201

# route to update an existing meal
@app.route('/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"error": "Meal not found"}), 404

    meal_data = request.get_json()
    title = meal_data.get('title')
    description = meal_data.get('description')
    category = meal_data.get('category')
    image = meal_data.get('image')

    if title:
        meal.title = title
    if description:
        meal.description = description
    if category:
        meal.category = category
    if image:
        meal.image = image

    db.session.commit()

    return jsonify({"message": "Meal updated successfully"}), 200

# route to delete an existing meal
@app.route('/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"error": "Meal not found"}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({"message": "Meal deleted successfully"}), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
        for user in users
    ]
    return jsonify(users_data)

# route to get a specific user by their ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        userdata = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
        return jsonify(userdata)
    else:
        return jsonify({"error": "User not found"}), 404

# route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')

    if not username or not email or not password:
        return jsonify({"error": FieldError}), 400

    new_user = User(username=username, email=email, password_hash=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New User created successfully"}), 201

#  route to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = request.get_json()
    username = user_data.get('username')
    email = user_data.get('email')

    if username:
        user.username = username
    if email:
        user.email = email

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

#  route to delete an existing user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200


#  route to get all ingredients
@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    ingredients_data = [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "unit": ingredient.unit,
            "meal_id": ingredient.meal_id
        }
        for ingredient in ingredients
    ]
    return jsonify(ingredients_data)

#  route to get a specific ingredient by its ID
@app.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if ingredient:
        ingredient_data = {
            "id": ingredient.id,
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "unit": ingredient.unit,
            "meal_id": ingredient.meal_id
        }
        return jsonify(ingredient_data)
    else:
        return jsonify({"error": "Ingredient not found"}), 404

#  route to create a new ingredient
@app.route('/ingredients', methods=['POST'])
def create_ingredient():
    ingredient_data = request.get_json()
    name = ingredient_data.get('name')
    quantity = ingredient_data.get('quantity')
    unit = ingredient_data.get('unit')
    meal_id = ingredient_data.get('meal_id')

    if not name or not quantity or not unit or not meal_id:
        return jsonify({"error": FieldError}), 400

    new_ingredient = Ingredient(name=name, quantity=quantity, unit=unit, meal_id=meal_id)
    db.session.add(new_ingredient)
    db.session.commit()

    return jsonify({"message": "New Ingredient created successfully"}), 201

# route to update an existing ingredient
@app.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({"error": "Ingredient not found"}), 404

    ingredient_data = request.get_json()
    name = ingredient_data.get('name')
    quantity = ingredient_data.get('quantity')
    unit = ingredient_data.get('unit')
    meal_id = ingredient_data.get('meal_id')

    if name:
        ingredient.name = name
    if quantity:
        ingredient.quantity = quantity
    if unit:
        ingredient.unit = unit
    if meal_id:
        ingredient.meal_id = meal_id

    db.session.commit()

    return jsonify({"message": "Ingredient updated successfully"}), 200

# route to delete an existing ingredient
@app.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({"error": "Ingredient not found"}), 404

    db.session.delete(ingredient)
    db.session.commit()

    return jsonify({"message": "Ingredient deleted successfully"}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
