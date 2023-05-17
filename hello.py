from flask import Flask, render_template

# after importing the modules, start writing the functions. When a function is wrapped in @app.route,
# it is the code for a webpage. All the html documents must be in the 'templates' folder to be rendered.
# all the CSS/images/styling must be in the 'static' folder to get picked up

app = Flask(__name__)

# homepage route
@app.route('/')
def homepage():
    return render_template('index.html')

# search bar route
@app.route('/search')
def search():
    return render_template('search.html')

# account login route
@app.route('/savedplaylists', methods=["POST", "GET"])
def playlists():
    name = request.form["username"]
    return render_template("savedplaylists.html", username=name)

# search results route
@app.route('/results', methods=["POST", "GET"])
def results():
    year_of_release = request.form["decade"]
    bechdel_test_score = request.form["bechdel"]
    director_gender = request.form["director"]
    return render_template('results.html', year=year_of_release, score=bechdel_test_score,
                           director_value=director_gender)
if __name__ == "__main__":
    app.run(debug=True)

