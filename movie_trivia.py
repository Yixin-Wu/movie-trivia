'''
Created on Feb 15, 2016

@author: CNelson ColinWu
'''
# coding: utf-8
import csv
import webbrowser

def create_actors_DB(actor_file):
    '''create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0].lower().title()
        movies = [x.lstrip().rstrip().lower().title() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0].lower().title()] = [int(row[1]), int(row[2])]
    return scores_dict

def insert_actor_info(actor,movies,movie_Db):
    '''insert or update an actor's movies'''
    if movie_Db.has_key(actor):
        movie_Db[actor] = movie_Db[actor].union(set(movies))
    else:
        movie_Db[actor] = set(movies)

def insert_rating(movie,ratings,ratings_Db):
    '''insert or update a movie's ratings'''
    ratings_Db[movie] = ratings
        
def delete_movie(movie,movie_Db,ratings_Db):
    '''delete a movie's information'''
    has_this_movie = False
    if ratings_Db.has_key(movie):
        del ratings_Db[movie]
        has_this_movie = True
    for actor in movie_Db.keys(): # find the movie with actor
        if movie in movie_Db[actor]:
            movie_Db[actor].remove(movie)
    return has_this_movie

def select_where_actor_is(actor_name,movie_Db):      
    '''find the actor's movies'''
    if movie_Db.has_key(actor_name):
        return movie_Db[actor_name]
    else:
        return []

def select_where_movie_is(movie_name,movie_Db):
    '''find the movie's actors'''
    movie_actor = []
    for actor in movie_Db.keys(): # find every actor's movies to check whether it is the movie asked
        if movie_name in movie_Db[actor]:
            movie_actor.append(actor)
    return movie_actor

def select_where_rating_is(comparison,targeted_rating,is_critic,ratings_Db):
    '''find the targeted rating movies'''
    movie = []
    if comparison == '>':
        if is_critic:
            for movie_name in ratings_Db.keys(): # find every movie's score to check
                if ratings_Db[movie_name][0] > targeted_rating:
                    movie.append(movie_name)
        else:
            for movie_name in ratings_Db.keys():
                if ratings_Db[movie_name][1] > targeted_rating:
                    movie.append(movie_name)
    elif comparison == '<':
        if is_critic:
            for movie_name in ratings_Db.keys():
                if ratings_Db[movie_name][0] < targeted_rating:
                    movie.append(movie_name)
        else:
            for movie_name in ratings_Db.keys():
                if ratings_Db[movie_name][1] < targeted_rating:
                    movie.append(movie_name)
    elif comparison == '=':
        if is_critic:
            for movie_name in ratings_Db.keys():
                if ratings_Db[movie_name][0] == targeted_rating:
                    movie.append(movie_name)
        else:
            for movie_name in ratings_Db.keys():
                if ratings_Db[movie_name][1] == targeted_rating:
                    movie.append(movie_name)
    return movie
    
def get_co_actors(actor_name,movie_db):
    '''find the actor's workmates'''
    co_actor = []
    if movie_db.has_key(actor_name):
        for movie in movie_db[actor_name]: # find the actor's movies
            for actors in movie_db.keys(): # find all the actor in the same movie
                if movie in movie_db[actors]: # find a workmate
                    if actors != actor_name: # not the actor himself
                        if (actors in co_actor) == False: # no repeat names
                            co_actor.append(actors)
        return co_actor
    else:
        return []

def get_common_movie(actor1,actor2,movie_db):
    '''find the movies both actors are present'''
    movies = []
    if movie_db.has_key(actor1) and movie_db.has_key(actor2):
        for movie in movie_db[actor1]: # find if actor1's movie is in actor2's movie
            if movie in movie_db[actor2]:
                movies.append(movie)
        return movies
    else:
        return []

def critics_darling(movie_Db,ratings_Db):
    '''find the actors whose movie has highest average rating from critics'''
    actors = []
    actor_rating = 0
    highest_rating = 0
    total_score = 0
    count = 0
    for actor in movie_Db.keys(): # find an actor's movie rating
        for movie in movie_Db[actor]: # calculate the average score
            if ratings_Db.has_key(movie):
                total_score = total_score + ratings_Db[movie][0]
                count = count + 1
        if count != 0:
            actor_rating = total_score / count
        if actor_rating > highest_rating:
            highest_rating = actor_rating
            actors = []
            actors.append(actor)
        elif actor_rating == highest_rating:
            actors.append(actor)
        total_score = 0
        count = 0
    return actors

def audience_darling(movie_Db,ratings_Db):
    '''find the actors whose movie has highest average rating from audience'''
    actors = []
    actor_rating = 0
    highest_rating = 0
    total_score = 0
    count = 0
    for actor in movie_Db.keys(): # find an actor's movie rating
        for movie in movie_Db[actor]: # calculate the average score
            if ratings_Db.has_key(movie):
                total_score = total_score + ratings_Db[movie][1]
                count = count + 1.0
        if count != 0:
            actor_rating = total_score / count
        if actor_rating > highest_rating:
            highest_rating = actor_rating
            actors = []
            actors.append(actor)
        elif actor_rating == highest_rating:
            actors.append(actor)
        total_score = 0
        count = 0
    return actors

def good_movies(ratings_Db):
    ''' find movies that has ratings above 85 both from critics and audience'''
    movie_critic = []
    movie_audience = []
    for movie in ratings_Db.keys(): # find rating above 85 movies
        if ratings_Db[movie][0] >= 85.0:
            movie_critic.append(movie)
        if ratings_Db[movie][1] >= 85.0:
            movie_audience.append(movie)
    movie_good = set(movie_critic)
    movie_good.intersection(set(movie_audience))
    return movie_good

def get_common_actors(movie1,movie2,movies_Db):
    '''find actors in both movies'''
    actors = []
    for actor in movies_Db.keys(): # find movie from an actor
        if movie1 in movies_Db[actor] and movie2 in movies_Db[actor]:
            actors.append(actor)
    return actors

def get_bacon(actor,movie_Db):
    '''get the actor's bacon number'''
    url = 'https://www.google.com/?gws_rd=ssl#q=bacon+number+%s'%actor
    webbrowser.open_new(url)
    
def name_convert(name):
    '''convert all the input into standard format for search'''
    name_c = name.lower().title()
    return name_c   

def main():
    '''main function of the program'''
    # create database
    movie_Db = create_actors_DB('movies.txt')
    ratings_Db = create_ratings_DB('moviescores.csv')
    # welcome message
    print '''Welcome to Movie Trivia!\n\nHere is all the functions:
1.  Insert or update an actor and his/her movies.
2.  Insert or update a movie's ratings.
3.  Delete a movie's information and ratings.
4.  Find an actor's movies.
5.  Find an movie's actors.
6.  Find movies with ratings.
7.  Find an actor's workmates.
8.  Find movies where two actors both acted.
9.  Find actors with highest average movie ratings from critics.
10. Find actors with highest average movie ratings from audience.
11. Find movies with ratings above 85 from both critics and audience.
12. Find actors acted in both movies.
13. Find an actor's Bacon number.
-1. Quit the Movie Trivia.'''

    # function start
    while(1):
        choose = input('\n\nPlease choose a function: ')
        if choose == 1:
            actor = name_convert(raw_input('Please input the actor name: '))
            while actor == '':
                actor = name_convert(raw_input('The movie trivia does not receive any actor name. Please input the actor name: '))
            movies = name_convert(raw_input("Please input the actor's movies:(separated by ',') ")).split(',')
            while movies == ['']:
                movies = name_convert(raw_input('The movie trivia does not receive any movie name. Please input the actor name: ')).split(',')
            insert_actor_info(actor, movies, movie_Db)
            print 'Your information has been updated:\nActor: %s\nMovies: '%actor,
            for movie in movie_Db[actor]: # print updated movies
                print '%s,'%movie,
        elif choose == 2:
            movie = name_convert(raw_input('Please input the movie name: '))
            rating = raw_input("Please input the movie's ratings:(separated by 'critics,audience') ").split(',')
            while len(rating) != 2:
                rating = raw_input("The rating doesn't fit the format. Please input the movie's ratings:(separated by 'critics,audience') ").split(',')
            ratings = (rating[0],rating[1])
            insert_rating(movie, ratings, ratings_Db)
            print 'Your information has been updated:\nMovie: %s\nRatings: critics %s, audience %s'%(movie,ratings_Db[movie][0],ratings_Db[movie][1]) # print updated ratings
        elif choose == 3:
            movies = name_convert(raw_input("Please input the movie you want to delete:(separated by ',') ")).split(',')
            for movie in movies: # can delete multiple movies one time
                if delete_movie(movie, movie_Db, ratings_Db):
                    print '%s is deleted!'%movie
                else:
                    print 'No such a movie.'
        elif choose == 4:
            actor_name = name_convert(raw_input('Please input the actor name: '))
            movies = select_where_actor_is(actor_name, movie_Db)
            print 'The actor acted in: ',
            for movie in movies:
                print '%s, '%movie,
        elif choose == 5:
            movie_name = name_convert(raw_input('Please input the movie name: '))
            actors = select_where_movie_is(movie_name, movie_Db)
            print 'The movie has actors: ',
            for actor in actors:
                print '%s, '%actor,
        elif choose == 6:
            comparison = raw_input('Please input the comparison:(< = >) ')
            targeted_rating = input('Please input the targeted rating: ')
            critic = raw_input('Please input whether it is the critics rating:(y/n) ').lower()
            if critic == 'y':
                is_critic = True
            else:
                is_critic = False
            movies = select_where_rating_is(comparison,targeted_rating,is_critic,ratings_Db)
            print 'The movies with ratings %s %.1f are: '%(comparison,targeted_rating),
            for movie in movies:
                print '%s, '%movie,
        elif choose == 7:
            actor_name = name_convert(raw_input('Please input the actor name: '))
            actors = get_co_actors(actor_name, movie_Db)
            print 'The actor has workmates: ',
            for actor in actors:
                print '%s, '%actor,
        elif choose == 8:
            actor1 = raw_input('Please input the name of the first actor.')
            while actor1 == '':
                actor1 = raw_input('The movie trivia is not receiving any actor name. Please input the first actor: ')
            actor2 = raw_input('Please input the name of the second actor.')
            while actor2.lower() == actor1.lower():
                actor2 = raw_input('You are inputing the same actor. Please input the name of another actor.')
            while actor2 == '':
                actor2 = raw_input('The movie trivia is not receiving any actor name. Please input the second actor: ')
            movies = get_common_movie(actor1, actor2, movie_Db)
            print 'The actors have worked together in: ',
            for movie in movies:
                print '%s, '%movie,
        elif choose == 9:
            actors = critics_darling(movie_Db, ratings_Db)
            print 'The actor with highest average critics ratings: ',
            for actor in actors:
                print '%s '%actor,
        elif choose == 10:
            actors = audience_darling(movie_Db, ratings_Db)
            print 'The actor with highest average audience ratings: ',
            for actor in actors:
                print '%s '%actor,
        elif choose == 11:
            movies = good_movies(ratings_Db)
            print 'The good movies: ',
            for movie in movies:
                print '%s, '%movie,
        elif choose == 12:
            movie1 = raw_input('Please input the first movie: ')
            while movie1 == '':
                movie1 = raw_input('The movie trivia is not receiving any movie name. Please input the first movie: ')
            movie2 = raw_input('Please input the second movie: ')
            while movie2.lower() == movie1.lower():
                movie2 = raw_input('You are typing in the same movie. Please input another movie: ')
            while movie2 == '':
                movie2 = raw_input('The movie trivia is not receiving any movie name. Please input the second movie: ')
            actors = get_common_actors(movie1, movie2, movie_Db)
            print 'The movies have common actors: ',
            for actor in actors:
                print '%s, '%actor,
        elif choose == 13:
            actor = name_convert(raw_input('Please input the actor name: '))
            get_bacon(actor, movie_Db)
        elif choose == -1:
            break
        else:
            print 'Please choose a function from -1 to 13!',

    
if __name__ == '__main__':
    main()
