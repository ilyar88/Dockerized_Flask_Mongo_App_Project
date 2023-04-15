from flask import Blueprint, jsonify, render_template, request
from Movie_db import Movie_db

app_blueprint = Blueprint('app_blueprint',__name__)

@app_blueprint.route('/search',methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST': 
            similar = Movie_db.search_movie(request.form['name'])
            dictionary = { "poster_path" : stu.poster_path for stu in similar }
            if Movie_db.search_value(dictionary):
                Movie_db.insert_data(dictionary)
                temp = dictionary
            else:
                temp = dictionary

        return render_template("index.html",image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
    except:
        return render_template("index.html")

@app_blueprint.route('/remove',methods=['GET', 'POST'])
def remove():
    try:
        if request.method == 'POST': 
            similar = request.form['name']
            Movie_db.remove_data(similar)

            return render_template("index.html")
    except:
        return render_template("index.html")

@app_blueprint.route('/update',methods=['GET', 'POST'])
def update_data():
        try:
            if request.method == 'POST':
                similar = request.form['name1']
                value = request.form['name2']
                Movie_db.update_data(similar,value)
                dictionary = Movie_db.search_movie(request.form['name2'])
                temp = { "poster_path" : stu.poster_path for stu in dictionary }

                return render_template("index.html",image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
        except:
            dictionary = Movie_db.search_movie(request.form['name2'])
            temp = { "poster_path" : stu.poster_path for stu in dictionary }
            
            return render_template("index.html",image="https://image.tmdb.org/t/p/original/" + str(temp["poster_path"]))
