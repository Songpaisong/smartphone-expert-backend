from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

df = pd.read_csv('mobile_recommendation_system_dataset.csv')
df['price'] = df['price'].astype(str).str.replace('[^0-9]', '', regex=True).astype(int)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['corpus'])
similarity = cosine_similarity(tfidf_matrix)

@app.route('/recommend', methods=['GET'])
def recommend():
    keyword = request.args.get('keyword')
    max_price = int(request.args.get('price'))

    idx = df[df['corpus'].str.lower().str.contains(keyword.lower())].index
    if len(idx) == 0:
        return jsonify([])

    scores = similarity[idx[0]]
    results = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)

    output = []
    for i, _ in results[:5]:
        output.append({
            'name': df.iloc[i]['name'],
            'price': df.iloc[i]['price'],
            'rating': df.iloc[i]['ratings'],
            'image': df.iloc[i]['imgURL']
        })

    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
