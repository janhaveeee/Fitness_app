from flask import Blueprint, jsonify, request
from database import collection

diet_bp = Blueprint('diet_bp', __name__)

@diet_bp.route('/dishes', methods=['GET'])
def get_all_dishes():
    dishes = list(collection.find({}, {'_id': 0}))
    return jsonify(dishes)

@diet_bp.route('/recommend', methods=['POST'])
def recommend_dishes():
    user_input = request.json
    max_calories = float(user_input.get("max_calories", 500))

    results = list(collection.find(
        {"Calories (kcal)": {"$lte": max_calories}},
        {'_id': 0}
    ).sort("Calories (kcal)", 1))

    return jsonify(results)


@diet_bp.route("/save_meal", methods=["POST"])
def save_meal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Insert data into MongoDB
    result = collection.insert_one(data)
    return jsonify({"message": "Meal saved", "id": str(result.inserted_id)}), 201
