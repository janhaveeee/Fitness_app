import pandas as pd
from database import collection

def import_csv_to_mongo(csv_path):
    df = pd.read_csv(csv_path)
    records = df.to_dict(orient="records")
    collection.delete_many({})  # Optional: Clear previous data
    collection.insert_many(records)

def generate_meal_plan(target_calories):
    df = pd.read_csv("dataset/diet_data.csv")
    df = df.dropna()

    meal_plan = []
    total_calories = 0

    for _, row in df.sample(frac=1).iterrows():
        if total_calories + row['Calories (kcal)'] <= target_calories:
            meal_plan.append(row)
            total_calories += row['Calories (kcal)']
        if total_calories >= target_calories:
            break

    totals = {
        "Calories (kcal)": sum([m['Calories (kcal)'] for _, m in pd.DataFrame(meal_plan).iterrows()]),
        "Protein (g)": sum([m['Protein (g)'] for _, m in pd.DataFrame(meal_plan).iterrows()]),
        "Carbohydrates (g)": sum([m['Carbohydrates (g)'] for _, m in pd.DataFrame(meal_plan).iterrows()]),
        "Fats (g)": sum([m['Fats (g)'] for _, m in pd.DataFrame(meal_plan).iterrows()])
    }

    return pd.DataFrame(meal_plan).to_dict(orient='records'), totals
