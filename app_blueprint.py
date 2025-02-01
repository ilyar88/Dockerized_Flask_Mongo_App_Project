from flask import Blueprint, render_template, request
from Movie_db import Movie_db

# Create a Blueprint for the app to modularize routes
app_blueprint = Blueprint('app_blueprint', __name__)

# Route to handle the movie search and display the poster image
@app_blueprint.route('/search', methods=['GET', 'POST'])
def index():
    try:
        # Check if the request method is POST
        if request.method == 'POST': 
            # Call the Movie_db.search_movie() method to search for a movie based on the name inputted
            similar = Movie_db.search_movie(request.form['name'])
            
            # Create a dictionary with poster path for each result in the search
            dictionary = { "poster_path" : stu.poster_path for stu in similar }
            
            # Check if the movie poster path already exists in the database
            if Movie_db.search_value(dictionary):
                # If not found, insert the movie data into the database
                Movie_db.insert_data(dictionary)
                temp = dictionary  # Save the dictionary to temp to display the image
            else:
                temp = dictionary  # If the movie already exists, assign the dictionary to temp

        # Render the template with the movie poster image URL
        return render_template("index.html", image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
    except:
        # If an error occurs, render the template with no image
        return render_template("index.html")

# Route to handle the removal of a movie from the database
@app_blueprint.route('/remove', methods=['GET', 'POST'])
def remove():
    try:
        # Check if the request method is POST
        if request.method == 'POST': 
            # Get the movie name to remove from the form input
            similar = request.form['name']
            
            # Call Movie_db.remove_data() to remove the movie data from the database
            Movie_db.remove_data(similar)

            # Render the template after the movie has been removed
            return render_template("index.html")
    except:
        # If an error occurs, render the template without making any changes
        return render_template("index.html")

# Route to handle the update of a movie's data in the database
@app_blueprint.route('/update', methods=['GET', 'POST'])
def update_data():
    try:
        # Check if the request method is POST
        if request.method == 'POST':
            # Get the old movie name and the new movie name to update from the form inputs
            similar = request.form['name1']
            value = request.form['name2']
            
            # Call Movie_db.update_data() to update the movie data in the database
            Movie_db.update_data(similar, value)
            
            # Get the updated movie data based on the new name provided
            dictionary = Movie_db.search_movie(request.form['name2'])
            
            # Create a dictionary with the poster path for the updated movie
            temp = { "poster_path" : stu.poster_path for stu in dictionary }

            # Render the template with the updated movie poster image
            return render_template("index.html", image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
    except:
        # If an error occurs, get the updated movie data based on the new name and render the template
        dictionary = Movie_db.search_movie(request.form['name2'])
        temp = { "poster_path" : stu.poster_path for stu in dictionary }
        
        # Render the template with the updated movie poster image
        return render_template("index.html", image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
