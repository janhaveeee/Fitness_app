from flask import Flask
from diet_routes import diet_bp
from utils import import_csv_to_mongo

app = Flask(__name__)

# Import data from CSV at startup (one-time, or control with flag)
import_csv_to_mongo("dataset/Indian_Food_Nutrition_Processed.csv")

# Register Blueprint
app.register_blueprint(diet_bp, url_prefix="/api")

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    from utils import generate_meal_plan  # function you'll create
    data = request.get_json()
    target_calories = data.get("calories", 2000)
    plan, totals = generate_meal_plan(target_calories)
    return jsonify({"meal_plan": plan, "totals": totals})

if __name__ == "__main__":
    app.run(debug=True)
