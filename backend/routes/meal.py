from flask import Blueprint, request, jsonify
import pickle
from database import get_meal_collection

meal_bp = Blueprint("meal_bp", __name__)
model = pickle.load(open("ml_models/meal_model.pkl", "rb"))

@meal_bp.route("/", methods=["POST"])
def get_meal_plan():
    try:
        user_input = request.get_json()

        # Extract input features
        features = [
            user_input["num_ingredients"],
            user_input["calories"],
            user_input["prep_time"],
            user_input["protein"],
            user_input["fat"],
            user_input["carbs"],
            user_input["vegan"],
            user_input["vegetarian"],
            user_input["keto"],
            user_input["paleo"],
            user_input["gluten_free"],
            user_input["mediterranean"],
        ]

        # Predict
        prediction = model.predict([features])[0]
        label = "Healthy" if prediction == 1 else "Not Healthy"

        # Store in DB
        get_meal_collection().insert_one({**user_input, "prediction": label})

        return jsonify({"health_status": label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
