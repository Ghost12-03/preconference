from flask import Flask, request, jsonify
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the preprocessed data
new_df = pd.read_csv("movies_data.csv")  # Save and load the processed data
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [new_df.iloc[i[0]].title for i in movies_list]

@app.route('/recommend', methods=['GET'])
def recommend_movies():
    movie_name = request.args.get('movie')
    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400
    
    try:
        recommendations = recommend(movie_name)
        return jsonify({"movie": movie_name, "recommendations": recommendations})
    except IndexError:
        return jsonify({"error": "Movie not found in database"}), 404

if __name__ == '__main__':
    app.run(debug=True)
