#use these first 2 functions to create your 2 dictionaries
import csv

### Functions
#### Helper Functions
def name_converter(name):
    '''Convert a string to a 'name' format regardless of it original form'''
    return name.title()

def intersect_two_list(list1,list2):
    '''return a set which is the intersection of the elements 
    in the given two lists'''
    return set(list1)&set(list2)

def set_to_sorted_list(the_set):
    '''return the sorted list form of the given set'''
    the_list=list(the_set)
    the_list.sort()
    return the_list

def guide_set_up():
    '''return 3 docstring guides in a tuple'''
    ## The guide for the main stage
    main_guide='''
    Enter 1 to search based on actor names
    Enter 2 to search based on movies names
    Enter 8 to update the actor database
    Enter 9 to update the rating database
    Enter EXIT leave the program
    Enter any other word to see this guide again'''
    ## The guide for the actor stage
    actor_guide='''
    Enter 1 to find all the movies starred by the searched actor
    Enter 2 to find the co-actors of the searched actor
    Enter 3 to see the averaged rating of all the movies feartured by the actor
    Enter 4 to find the common movies of two actors
    Enter 0 to back to the home stage
    Enter any other word to see this guide again'''
    ## The guide for the movie stage
    movie_guide='''
    Enter 1 to search movies based on preference
    Enter 2 to find the good movies
    Enter 3 to find the common actors in the two movies
    Enter 4 to find all the actors in the searched moive
    Enter 5 to see the ratings of the searched movie
    Enter 0 to back to the home stage
    Enter any other word to see this guide again'''
    return (main_guide, actor_guide,movie_guide)

def create_lowered_dict(actordb,ratingsdb):
    '''return the lower-cased movie name verison of actordb and ratingsdb'''
    ##create the lower-cased actordb

    lowered_actordb=dict()
    # create a lower-cased movie name list for the actor in the actordb 
    for actor in actordb:
        movie_list=list()
        for movie in actordb[actor]:
            movie_list.append(movie.lower())
        # add the lower-cased movies and the actor to the lower-cased actordb
        insert_actor_info(actor, movie_list, lowered_actordb)

    # create the new dict
    lowered_ratingsdb=dict()
    # only need to change the key to lower case, and update in the lowered dict
    for movie in ratingsdb:
        insert_rating(movie.lower(), ratingsdb[movie], lowered_ratingsdb)

    return(lowered_actordb,lowered_ratingsdb)

def calculate_avg_rating(actor_name,actordb,ratingsdb):
    '''return the avgerage rating of the movie starred by the actor'''

    all_ratings=list()
    movies=select_where_actor_is(actor_name, actordb)
    # find all the ratings of the movies, calculate and return the average
    for movie in movies:
        if movie in ratingsdb:
            all_ratings.append(\
                int(ratingsdb[movie][0])+int(ratingsdb[movie][1]))
    if len(all_ratings)==0:
        return 'No movie rating of the actor recorded'
    return sum(all_ratings)/len(all_ratings)/2

def get_input_to_filter():
    '''return the required parameter to filter movies from the input,
    this is a input-output function and doesn't need unit test'''

    # stay in the stage until the a right input is received
    # get the input for the comparison symbol
    while True:
        comp=input('''Please enter > for larger than, = for equal to,
        < for smaller than the target rating\n''')
        if comp in ['<','>','=']:
            break
        print('Wrong input! Please check and input again.')

    # get the input for the targeted rating
    while True:
        target=input('''Please enter the targeted rating, which should 
            be an integer between 0 to 100\n''')
        if target.isdigit() and int(target)>=0 and int(target)<=100:
            target=int(target)
            break
        print('Wrong input! Please check and input again.')

    # get the input for the type of the rating to search
    while True:
        isC=input('''Please enter C to search based on critics rating, 
            or A to search based on audience rating\n''')
        if isC.lower()=='c':
            isC=True
            break
        elif isC.lower()=='a':
            isC=False
            break
        print('Wrong input! Please check and input again.')

    # return the gathered inputs
    return (comp,target,isC)

def get_input_for_common_actor():
    ''' get the input to search for common actors,
    this is a input-output function and doesn't need unit test'''

    # get the inputs
    movie1=input('Please input the name of the movie:\n').lower()
    movie2=input('Please input the name of the other movie:\n').lower()
    # return the inputs
    return (movie1,movie2)

def actor_stage(actordb,ratingsdb,guide):
    '''the stage to have further opeations based on actors
    this is a input-output function and doesn't need unit test'''

    # stay in the stage until the user opts out
    while True:
        # print the guide and take input
        print(guide)
        scanner=input('Please enter the number\n').lower()

        # user opts quit to main stage
        if scanner=='0':
            break

        # find all the movies starred by the searched actor when input is 1
        elif scanner=='1':
            scanner=input('Please input the name of the actor:\n').title()
            # search the inputed name, and show result
            if scanner in actordb:
                    print('All the movies of the actor are:')
                    print (', '.join(actordb[scanner]))
            else:
                print('Actor not found in the database.')

        # find the co-actors of the searched actor when input is 2
        elif scanner=='2':
            scanner=input('Please input the name of the actor:\n').title()
            # print the search result using get_co_actors()
            if scanner in actordb:
                print('The co-actros of the searched actor are',\
                    '(blank for no co-actor found)')
                print(', '.join(get_co_actors(scanner, actordb)))
            else:
                print('Actor not found in the database.')

        # show the averaged rating of the movies feartured by the actor
        elif scanner=='3':
            scanner=input('Please input the name of the actor:\n').title()
            # if the input name found in the actordb
            if scanner in actordb:
                # print the result
                print('The averaged rating is',\
                    calculate_avg_rating(scanner,actordb,ratingsdb))
            # print indicater if the actor is not found
            else:
                print('Actor not found in the database.')

        # find the common movies of two actors when input is 4
        elif scanner=='4':
            # get the actor names
            actor1=\
                input('Please input the name of the first actor:\n').title()
            actor2=\
                input('Please input the name of the other actor:\n').title()
            # do the search
            movie_list=get_common_movie(actor1, actor2, actordb)
            # print the result
            if movie_list==[]:
                print('No common movie found, please check again')
            else:
                print('The common movies are:')
                print(', '.join(movie_list))

def movie_stage(actordb,ratingsdb,guide):
    '''the stage to have further opeartions based on movies,
    this is a input-output function and doesn't need unit test'''

    # create the lowered cased movie name datebase for search convinence
    lowered_actordb,lowered_ratingsdb=create_lowered_dict(actordb,ratingsdb)

    # stay in the stage until the user opts out
    while True:
        # get the input
        print(guide)
        scanner=input('Please enter the number\n').lower()

        # back to main stage if the input is 0
        if scanner == '0':
            break

        # search movies based on preference if the input is 1
        elif scanner=='1':
            # get the inputs
            comp, target, isC=get_input_to_filter()
            #do the search
            movie_list=select_where_rating_is(comp, target, isC, ratingsdb)
            # show the result
            if movie_list!=[]:
                print('The movies meeting the requirements are:')
                print(', '.join(movie_list))
            else:
                print('No movie meets the requirements found.')

        # show the good movies in the database if the input is 2
        elif scanner=='2':
            good_mv=good_movies(ratingsdb)
            print('The highly rated movies are:\n',', '.join(good_mv))

        # show the common actors of two moives if the input is 3
        elif scanner=='3':
            # get the input
            movie1, movie2=get_input_for_common_actor()
            # do the search
            actor_list=get_common_actors(movie1, movie2, lowered_actordb)
            # print the result
            if actor_list==[]:
                print('No common actor found, please check again')
            else:
                print('Common actors are:')
                print(', '.join(actor_list))

        # show the actors in a searched movie if the input is 4
        elif scanner=='4':
            # take the input
            movie=input('Please input the name of the movie:\n').lower()
            # do the search
            actor_list=select_where_movie_is(movie, lowered_actordb)
            # print the result
            if actor_list==[]:
                print('No actor found, please check again')
            else:
                print('The actors in the movie are:')
                print(', '.join(actor_list))

        # show the rating of a serached movie if the input is 5 
        elif scanner=='5':
            # take the input
            movie=input('Please input the name of the movie:\n').lower()
            # print the result
            if movie in lowered_ratingsdb:
                print('The critics rating is',lowered_ratingsdb[movie][0])
                print('The audience rating is',lowered_ratingsdb[movie][1])
            else:
                print('No rating of the movie is found in the database.')

def main_stage(actordb,ratingsdb,main_guide,actor_guide,movie_guide):
    ''' The main stage of the program, 
    lead the user to the next stage or to update the database.
    This function is IO-based and does not need unit test'''

    # stay in main stage until the user want to move to another stage or quit
    while True:
        # print the guide and get the input
        print(main_guide)
        scanner=input('Please enter the number\n').lower()

        # close the program if the input is exit
        if scanner.lower()=='exit':
            break

        # jump to actor stage if the input is 1
        elif scanner=='1':
            actor_stage(actordb,ratingsdb,actor_guide)

        # jump to movie stage if the input is 2
        elif scanner=='2':
            movie_stage(actordb,ratingsdb,movie_guide)

        # let the user manually update the actor database if the input is 8
        elif scanner=='8':
            update_actordb(actordb)

        # let the user manually update the ratings database if the input is 9
        elif scanner=='9':
            update_ratingsdb(ratingsdb)

def update_actordb(actordb):
    '''update the actordb mannually,
    this function is IO-based and does not need the unit test'''

    # take the inputs
    actor_name=name_converter(input('Please enter the name of the actor:\n'))
    movies=list()
    movies.append(input('Please enter the movie featrued by the actor:\n'))
    while True:
        scanner=input('''Please enter another movie featrued by the actor,
            or enter 0 to find movie inputing:\n''')
        if scanner=='0':
            break
        else:
            movies.append(scanner)
    # confirmation of update
    print('The actor is:    ',actor_name)
    print('The movies are:    ',','.join(movies))
    if input('''Are you sure to update?
        Enter Y to confirm or any other word to cancel:\n''').lower()=='y':
        # do the update
        insert_actor_info(actor_name, movies, actordb)
    # show feedback
        print('Operation Succeed')
    else:
        print('Operation Canceled')

def update_ratingsdb(ratingsdb):
    '''update the ratingsdb mannually,
    this function is IO-based and does not need the unit test'''

    #take the inputs
    movie_name=input('Please enter the name of the movie:\n')
    ratings=list()
    ratings.append(input('Please enter the critics rating (int 0-100):\n'))
    ratings.append(input('Please enter the audience rating (int 0-100):\n'))

    # check if the input is in the right range
    if ratings[0].isdigit() and ratings[1].isdigit() \
        and int(ratings[0])<=100 and int(ratings[0])>=0 \
        and int(ratings[1])<=100 and int(ratings[1])>=0:
        # confirmation check
        print('The movie is:    ',movie_name)
        print('The critics rating is {}\nThe audience rating is {}'\
            .format(ratings[0],ratings[1]))
        if input('''Are you sure to update?
        Enter Y to confirm or any other word to cancel:\n''').lower()=='y':
            # do the update
            insert_rating(movie_name,list(map(int,ratings)), ratingsdb)
    # print feedback
            print('Operation Succeed')
        else:
            print('Operation Canceled')
    else:
        print('Wrong rating input, operation canceled.')

#### Required Functions
#### Utility Functions
def insert_actor_info(actor, movies, actordb):
    ''' Add the actor-movie relationships to the actordb'''

    # convert the name to the right version first
    actor=name_converter(actor)

    # if the actor is in the actordb, updates the new movies
    if actor in actordb:
        for movie in movies:
            if movie not in actordb[actor]:
                actordb[actor].append(movie)
    # if the actor is not in, create a new entity
    else:
        actordb[actor]=movies

def insert_rating(movie, ratings, ratingsdb):
    '''Add/update the ratings to the move'''

    # change or create the rating entity of the movie in the database
    ratingsdb[movie]=ratings

def select_where_actor_is(actor_name, actordb):
    '''Return all the movie(s) recorded in the db featured by the actor'''
    # convert the name to a right version first
    actor_name=name_converter(actor_name)
    # if the entity exist, return the movie list
    return actordb.get(actor_name,[])

def select_where_movie_is(movie_name, actordb):
    '''Return all the actors featuring the movie'''

    if type(movie_name) != str:
        raise TypeError
    # create an empty list to save the result
    actor_list=list()
    # for each actor-movie_list pair in the actordb
    for actor,movie_list in zip(actordb.keys(),actordb.values()):
        # add the name of actor if the searched movie is in the moive list
        if movie_name in movie_list:
            actor_list.append(actor)

    return actor_list

def select_where_rating_is(comparison, targeted_rating, is_critic, ratingsdb):
    '''Return the search result of movies based on the requirement'''

    # create an empty list to save the search result
    search_result=list()
    # locate the specified rating position in the rating list
    rating_position=0 if is_critic else 1
    # zip the movie name-rating pairs
    zipped_dict=zip(ratingsdb.keys(),ratingsdb.values())

    # do the specified relation search for each entity in the ratings database
    # append the qualifying movies to the list
    if comparison == '<':
        for movie,ratings in zipped_dict:
            if int(ratings[rating_position])<targeted_rating:
                search_result.append(movie)
    elif comparison == '=':
        for movie,ratings in zipped_dict:
            if int(ratings[rating_position])==targeted_rating:
                search_result.append(movie)
    elif comparison > '<':
        for movie,ratings in zipped_dict:
            if int(ratings[rating_position])>targeted_rating:
                search_result.append(movie)
    return search_result

#### Fun Functions
def get_co_actors(actor_name, actor_db):
    ''' returns a list of all actors that given actor has ever worked with'''

    # get the list of movie where the actor has been
    movie_list=select_where_actor_is(actor_name, actor_db)
    # create a set to save the name of co-actors
    co_actors=set()
    # add all the actors of all the movies in the list to the result set
    for movie in movie_list:
        co_actors|=set(select_where_movie_is(movie, actor_db))
    # remove the name of the searched actor
    co_actors.remove(actor_name)
    # return the sorted list version of the result list
    return set_to_sorted_list(co_actors)


def get_common_movie(actor1, actor2, actor_db):
    '''return a list of common movies os the two given actors'''

    # get the the movies performed by the two actors respectivley
    movie_list1=select_where_actor_is(actor1, actor_db)
    movie_list2=select_where_actor_is(actor2, actor_db)

    # return the common movies
    return set_to_sorted_list(intersect_two_list(movie_list1,movie_list2))


def good_movies(ratingsdb):
     '''returns the set​ of movies that both critics and the audience have 
     rated above 85 '''

     # find the good movies under the two independent taste respectively
     critically_good=select_where_rating_is(">", 85, True, ratingsdb)
     loved_by_people=select_where_rating_is(">", 85, False, ratingsdb)
     # return the common movies
     return intersect_two_list(critically_good,loved_by_people)

def get_common_actors(movie1, movie2, actor_db):
    ''' returns the common actors of two movies'''

    # find the all the actors of the two movies respectively
    movie1_actors=select_where_movie_is(movie1, actor_db)
    movie2_actors=select_where_movie_is(movie2, actor_db)
    # return the common actors
    return set_to_sorted_list(intersect_two_list(movie1_actors,movie2_actors))

#### Given Functions
def create_actors_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        # NOTE: not movieInfo[actor] = set(movies)
        movieInfo[actor] = movies
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    # NOTE: the parameter encoding='utf-8' is necessary if you are running into an encoding error
    with open(ratings_file, 'r',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            # NOTE: cast the ratings list elements to ints
            scores_dict[row[0]] = [int(row[1]), int(row[2])]
    return scores_dict

def main():
    # environment setup
    actor_DB = create_actors_DB('moviedata.txt')
    ratings_DB = create_ratings_DB('movieratings.csv')
    main_guide, actor_guide, movie_guide=guide_set_up()

    # welcome information
    print('''   Welcome! You can enter the following numbers 
    to view the corresponding contents''')

    # enter the main stage of the progrram
    main_stage(actor_DB,ratings_DB,main_guide,actor_guide,movie_guide)

if __name__ == '__main__':
    main()
