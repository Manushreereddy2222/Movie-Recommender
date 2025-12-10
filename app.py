from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

OMDB_API_KEY = "b7f6619"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def results():
    query = request.args.get('q', '').strip()

    # If user submits nothing
    if query == "":
        return render_template("results.html", results=[], query=query)

    # Call OMDb API
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": OMDB_API_KEY,
        "s": query  # search for movies that match the title
    }

    response = requests.get(url, params=params).json()

    # If no movies found
    if response.get("Response") == "False":
        return render_template("results.html", results=[], query=query)

    movies = []

    # Loop through each movie result
    for item in response.get("Search", []):
        title = item.get("Title")
        year = item.get("Year")

        # Get full movie details
        params_full = {
            "apikey": OMDB_API_KEY,
            "t": title
        }
        full = requests.get(url, params=params_full).json()

        movie_data = {
            "title": title,
            "year": year,
            "genre": full.get("Genre", "Unknown"),
            "description": full.get("Plot", "No description available."),
            "poster": full.get("Poster") if full.get("Poster") != "N/A" else None
        }

        movies.append(movie_data)

    return render_template("results.html", results=movies, query=query)


if __name__ == "__main__":
    app.run(debug=True)
