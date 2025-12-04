from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

# Load movies data from JSON file
with open('movies.json') as f:
    movies = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/results')
def results():
    query = request.args.get('q', '').lower()
    
    # Filter movies by title
    matched = [m for m in movies if query in m['title'].lower()]

    return render_template('results.html', results=matched, query=query)

if __name__ == '__main__':
    app.run(debug=True)


