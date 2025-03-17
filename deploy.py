from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Load the cleaned movie dataset
new_df = pd.read_csv("movies_data.csv")

# Vectorize the text data
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags'].fillna('')).toarray()

# Compute cosine similarity, ensuring no NaN values
similarity = cosine_similarity(vectors)
similarity = np.nan_to_num(similarity)  # Replace NaNs with 0

# Define recommendation function
def recommend(movie):
    if movie.lower() not in new_df['title'].str.lower().values:
        return ["Movie not found in database"]

    # Find the correct movie index (case-insensitive)
    movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index[0]

    # Compute similarity scores
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = [new_df.iloc[i[0]].title for i in movies_list]
    return recommended_movies

# Flask API Endpoint
@app.route('/recommend', methods=['GET'])
def recommend_movies():
    movie_name = request.args.get('movie')

    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400

    recommendations = recommend(movie_name)
    return jsonify({"movie": movie_name, "recommendations": recommendations})

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
