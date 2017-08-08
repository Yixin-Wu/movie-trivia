import unittest
from movie_trivia import *

'''
    Author: Nelson Chen, Colin Wu
                                    '''

class Test_movie_trivia(unittest.TestCase):

    def test_insert_actor_info(self):
        ''' This test is used to examine whether the insert_actor_info is working properly. '''
        movie_Db = create_actors_DB('movies.txt')
        
            # The following part is used to examine whether the function of insert_actor_info returns
            # exactly what we want.
                                
        insert_actor_info('Nelson Chen', ['Hougong Gong'], movie_Db)
        self.assertEqual(set(['Hougong Gong']), movie_Db['Nelson Chen'])
        insert_actor_info('Yixin Wu', ['California', 'Berkeley', 'San Francisco'], movie_Db)
        self.assertEqual(set(['California', 'Berkeley', 'San Francisco']), movie_Db['Yixin Wu'])
        insert_actor_info('Christian Bale', ['Oklahoma', 'The Book of Mormon'], movie_Db)
        self.assertEqual(set(['The Fighter', 'The Dark Knight', 'The Dark Knight Rises', 'The Machinist',
                              'American Psycho', 'American Hustle', 'Oklahoma', 'The Book of Mormon']),
                         movie_Db['Christian Bale'])
        insert_actor_info('Diane Kruger', ['Hello'], movie_Db)
        self.assertEqual(set(['Troy', 'National Treasure', 'Inglourious Basterds', 'Hello']),
                         movie_Db['Diane Kruger'])
        
            # The following part is used to examine whether the function of insert_actor_info returns
            # something different from what we don't want.
                                                        
        insert_actor_info('Jiajia Li', ['My girlfriend'], movie_Db)
        self.assertNotEqual(set(['GT']), movie_Db['Jiajia Li'])
        insert_actor_info('Yixin Wu', ['Atlanta','UPenn'], movie_Db)
        self.assertNotEqual(set(['California', 'Berkeley', 'San Francisco']), movie_Db['Yixin Wu'])

    def test_insert_rating(self):
        ''' This test is used to examine whether the insert_rating is working properly. '''
        ratings_Db = create_ratings_DB('moviescores.csv')
        # The following part is inserting a new movie to the dictionary, and we will see whether the
        # result is the same.
        insert_rating('Neon Evangelion Genesis',[100,100],ratings_Db)
        self.assertEqual([100,100], ratings_Db['Neon Evangelion Genesis'])
        insert_rating('Avenue Q', [80,96], ratings_Db)
        self.assertNotEqual([78,96], ratings_Db['Avenue Q'])
        insert_rating('In The Heights', [90,83], ratings_Db)
        self.assertNotEqual([89,83], ratings_Db['In The Heights'])
        insert_rating('The Pride of Hiigara',[100,100],ratings_Db)
        self.assertNotEqual([90,90], ratings_Db['The Pride of Hiigara'])
        # The following part is changing an old movie's rating in the dictionary, and we will see
        # whether the rating has been changed.
        insert_rating('Casablanca',[98,99],ratings_Db)
        self.assertEqual([98,99], ratings_Db['Casablanca'])
        insert_rating('Milk',[1,2], ratings_Db)
        self.assertNotEqual([1,3], ratings_Db['Milk'])
        insert_rating('Casablanca',[100,98], ratings_Db)
        self.assertNotEqual([99,98], ratings_Db['Casablanca'])
        insert_rating("Gentleman's Agreement", [80,80], ratings_Db)
        self.assertNotEqual([79,79], ratings_Db["Gentleman'S Agreement"])

    def test_delete_movie(self):
        ''' This test is used to examine whether the delete_movie has successfully
            delete the movies in the movie_Db and ratings_Db.'''
        
        ratings_Db = create_ratings_DB('moviescores.csv')
        movie_Db = create_actors_DB('movies.txt')
        delete_movie('Mission Impossible',movie_Db,ratings_Db)
        self.assertFalse(ratings_Db.has_key('Mission Impossible'))
        has_movie = False
        for movie in movie_Db['Tom Cruise']:
            if movie == 'Mission Impossible':
                has_movie = True
        self.assertFalse(has_movie)
        delete_movie('Gentlemen Prefers Blondes',movie_Db,ratings_Db)
        self.assertFalse(ratings_Db.has_key('Gentlemen Prefers Blondes'))
        for movie in movie_Db['Marilyn Monroe']:
            if movie == 'Gentlemen Prefers Blondes':
                has_movie = True

    def test_select_where_actor_is(self):
        ''' This test is used to examine whether the select_where_actor_is will find
            the right movie.
                                                                        '''
        movie_Db = create_actors_DB('movies.txt')
        self.assertEqual(set(['Apollo 13', 'Catch Me If You Can', 'Philadelphia',
                              "You'Ve Got Mail", 'Sleepless In Seattle', 'Forrest Gump']),
                             select_where_actor_is('Tom Hanks',movie_Db))
        self.assertEqual([],select_where_actor_is('Yixin Wu', movie_Db))
        self.assertEqual(set(['Dial M For Murder', 'The Lost Weekend']), select_where_actor_is('Ray Milland', movie_Db))
        self.assertNotEqual(set(['Rain Man', 'Mission Impossible']),select_where_actor_is('Tom Cruise', movie_Db))
        self.assertNotEqual(set(["Nelson Chen's Happy Life"]),select_where_actor_is('Christian Bale', movie_Db))
        self.assertNotEqual(set(['Dark Knight']), select_where_actor_is('Julia Li', movie_Db))
        self.assertNotEqual(set(["You Can'T Take It With You", 'Mr Smith Goes To Washington', 'Apollo 13']),
                            select_where_actor_is('Jean Arthur', movie_Db))

    def test_select_where_movie_is(self):
        ''' This test is used to examine whether the select_where_movie_is will find
            the right actor.
                                                                        '''
        movie_Db = create_actors_DB('movies.txt')
        self.assertNotEqual(set(['Tom Cruise']), set(select_where_movie_is('Rain Man', movie_Db)))
        self.assertNotEqual(set(['Yixin Wu']), set(select_where_movie_is('High Society', movie_Db)))
        self.assertNotEqual(set(['Dustin Hoffman', 'Yixin Wu']), set(select_where_movie_is('Rain Man', movie_Db)))
        self.assertEqual(set(['Dustin Hoffman', 'Tom Cruise']), set(select_where_movie_is('Rain Man', movie_Db)))
        self.assertEqual(set([]),set(select_where_movie_is('Neon Evangelion Genesis', movie_Db)))
        self.assertEqual(set(['Tom Hanks']), set(select_where_movie_is('Philadelphia', movie_Db)))
        
    def test_select_where_rating_is(self):
        ''' This test is used to examine whether the select_where_rating_is will return
            the right movies. '''
        ratings_Db = create_ratings_DB('moviescores.csv')
        self.assertEqual(set(['It Happened One Night', 'Roman Holiday', 'Annie Hall', 'The French Connection', 'The Wrestler', 'Patton']),
                         set(select_where_rating_is('=', 98, True, ratings_Db)))
        self.assertEqual(set(['Lara Croft Tomb Raider', 'Bone Collector', 'Kazaam', 'Wild Wild West', 'Original Sin', 'Assassins']),
                         set(select_where_rating_is('<', 30, True, ratings_Db)))
        self.assertEqual(set([]),set(select_where_rating_is('>', 100, True, ratings_Db)))
        self.assertEqual(set([]),set(select_where_rating_is('<', 0, False, ratings_Db)))
        self.assertEqual(set(['The Virgin Queen']), set(select_where_rating_is('=', 60, False, ratings_Db)))
        self.assertEqual(set(['The Avengers']), set(select_where_rating_is('>', 99, False, ratings_Db)))
        self.assertNotEqual(set(['The Avengers']), set(select_where_rating_is('>', 99, True, ratings_Db)))
        self.assertNotEqual(set(['Lara Croft Tomb Raider', 'Bone Collector', 'Kazaam', 'Wild Wild West', 'Original Sin', 'Assassins']),
                            set(select_where_rating_is('<', 30, False, ratings_Db)))
        self.assertNotEqual(set(['Lara Croft Tomb Raider', 'Bone Collector', 'Wild Wild West', 'Original Sin', 'Assassins']),
                            set(select_where_rating_is('<', 30, True, ratings_Db)))

    def test_get_co_actors(self):
        ''' This test is used to examine whether the get_co_actor will return the right
            co-actors with a certain actor in all movies in the movie_Db. '''
        movie_Db = create_actors_DB('movies.txt')
        self.assertEqual(set(['Amy Adams', 'Tom Hardy', 'Bradley Cooper', 'Jeremy Renner', 'Jennifer Lawrence'])
                         , set(get_co_actors('Christian Bale', movie_Db)))
        self.assertEqual(set([]), set(get_co_actors('Yixin Wu', movie_Db)))
        self.assertEqual(set(['Jack Lemmon']), set(get_co_actors('Marilyn Monroe', movie_Db)))
        self.assertNotEqual(set(['Yixin Wu']), set(get_co_actors('Nelson Chen', movie_Db)))
        self.assertNotEqual(set(['Gene Hackman', 'Renee Zellweger']), set(get_co_actors('Clint Eastwood', movie_Db)))
        self.assertNotEqual(set(['Ellen Page', 'Leonardo Di Caprio', 'Charlize Theron']), set(get_co_actors('Tom Hardy', movie_Db)))

    def test_get_common_movie(self):
        ''' This test is used to examine whether the get_common_movie will return the
            right common movie(s) 2 actors have acted together.  '''
        movie_Db = create_actors_DB('movies.txt')
        self.assertEqual(set(['Titanic']), set(get_common_movie('Leonardo Di Caprio','Kate Winslet', movie_Db)))
        self.assertEqual(set([]), set(get_common_movie('Yixin Wu','Jiajia Li', movie_Db)))
        self.assertEqual(set(['The Apartment']), set(get_common_movie('Jack Lemmon','Shirley Maclaine', movie_Db)))
        self.assertNotEqual(set(['The Big O']), set(get_common_movie('Roger Smith','Dorothy', movie_Db)))
        self.assertNotEqual(set([]), set(get_common_movie('Jack Lemmon','Marilyn Monroe', movie_Db)))

    def test_critics_darling(self):
        ''' This test is used to examine whether the critics_darling is returning the
            right actor, whose score is the highest from the critics. '''
        movie_Db = create_actors_DB('movies.txt')
        ratings_Db = create_ratings_DB('moviescores.csv')
        self.assertEqual(['Joan Fontaine'], critics_darling(movie_Db, ratings_Db))

    def test_audience_darling(self):
        ''' This test is used to examine whether the audience_darling is returning the
            right actor, whose score is the highest from the audience. '''
        movie_Db = create_actors_DB('movies.txt')
        ratings_Db = create_ratings_DB('moviescores.csv')
        self.assertEqual(['Diane Keaton'], audience_darling(movie_Db, ratings_Db))

    def test_good_movies(self):
        ''' This test is used to examine whether the good_movies is returning the right
            list, in which the movies are all getting scores more than 85, both from
            critics and audience. '''
        ratings_Db = create_ratings_DB('moviescores.csv')
        good_movie_set = set(['Big Sleep', "What'S Eating Gilbert Grape", 'Star Trek Into Darkness', 'To Kill A Mockingbird',
                              'Lilies Of The Field', 'From Here To Eternity', 'Mrs. Miniver', 'Unforgiven', 'Dr Strangelove',
                              'Argo', 'Inception', 'American Hustle', 'Escape From Alcatraz', 'Guns Of Navarone', 'Leaving Las Vegas',
                              'Ordinary People', 'It Happened One Night', 'For A Few Dollars More', 'As Good As It Gets', 'Ben-Hur',
                              'Dial M For Murder', 'Mrs Miniver', 'Maltese Falcon', 'Casablanca', 'The Sixth Sense', 'Rear Window',
                              'In The Heat Of The Night', 'Guardians Of The Galaxy', 'Enchanted', 'The Accused', 'From Russia With Love',
                              'Eternal Sunshine Of The Spotless Mind', 'Milk', 'Silver Linings Playbook', 'The Sting', 'Rain Man',
                              'To Sir With Love', 'Roman Holiday', 'Annie Hall', 'X Men: First Class', 'High Noon', 'Double Indemnity',
                              'My Fair Lady', 'Dirty Harry', 'Scent Of A Woman', 'The French Connection', 'Some Like It Hot',
                              'The Hurt Locker', 'Jfk', 'Titanic', 'On The Waterfront', 'Apollo 13', 'The Fighter', 'The Deer Hunter',
                              'An American In Paris', 'All About Eve', 'West Side Story', 'Goodfellas', 'Mystic River',
                              '12 Years A Slave', 'Gentlemen Prefer Blondes', 'The Last Emperor',
                              'The Lord Of The Rings: The Return Of The King', 'Mr Smith Goes To Washington', 'How Green Was My Valley',
                              'The Lion In Winter', 'Three Musketeers', 'The Bridge On The River Kwai', 'Sound Of Music',
                              'Pulp Fiction', 'Juno', 'Kramer Vs. Kramer', 'The Dark Knight', 'Silence Of The Lambs',
                              'How To Steal A Million', 'Dog Day Afternoon', 'Rebecca', 'Cool Hand Luke', 'Rocky', 'Mash',
                              'Shakespeare In Love', 'Terms Of Endearment', 'The Odd Couple', 'Gone With The Wind', 'Departed',
                              'Field Of Dreams', 'Ted', 'Sabrina', 'Mary Poppins', 'Singin In The Rain', 'The Imitation Game',
                              'Road To Morocco', 'Kind Hearts And Coronets', 'Good Will Hunting', 'My Cousin Vinny', 'Superman',
                              "You Can'T Take It With You", 'The Apartment', 'Bourne Ultimatum', "Schindler'S List", 'Moonstruck',
                              'Lawrence Of Arabia', 'Amadeus', 'The Stranger', 'Patton', 'The Wrestler', 'Million Dollar Baby',
                              'The Philadelphia Story', 'Gandhi', 'No Country For Old Men', 'Midnight In Paris', 'Jerry Maguire',
                              'Ali', 'Catch Me If You Can', 'The Departed', 'The Godfather', 'Edward Scissorhands',
                              'The Godfather Part Ii', 'Speed'])
        self.assertEqual(good_movie_set, good_movies(ratings_Db))

    def test_get_common_actors(self):
        ''' This test is used to examine whether the get_common_actors is returning the
            right actors acting in two different movies.'''
        movie_Db = create_actors_DB('movies.txt')
        self.assertEqual(set([]), set(get_common_actors('The Big O', 'Neon Evangelion Genesis', movie_Db)))
        self.assertEqual(set(['Christian Bale']), set(get_common_actors('The Dark Knight', 'The Dark Knight Rises', movie_Db)))
        self.assertNotEqual(set(['Yixin Wu', 'Nelson Chen']), set(get_common_actors('Titanic', 'Chicago', movie_Db)))

if __name__ == '__main__':
    unittest.main()
        
