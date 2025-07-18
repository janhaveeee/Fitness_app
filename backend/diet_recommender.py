import pandas as pd

class DietRecommender:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)

    def recommend_diet(self, calorie_limit=500, protein_min=10):
        filtered = self.df[
            (self.df['Calories (kcal)'] <= calorie_limit) &
            (self.df['Protein (g)'] >= protein_min)
        ]
        return filtered.sort_values(by='Protein (g)', ascending=False).to_dict(orient='records')
