# python 2.7.2
# author: Siheng He (Email: sh2980@columbia.edu)

from math import sqrt
import os
##import prepare

cwd = 'D:/DDM/Project'
##user_loc = prepare.create_address()
preference = {}

def rate(movie):
    pref = {}
    f = open(cwd+'/train/'+movie+'.txt')
    f1 = f.readlines()
    f.close()
    for i in range(1,len(f1)):
        line = f1[i]
        field = line.split(',')
        pref.setdefault(field[0],int(field[1]))
    return pref

# Returns a distance-based similarity score for movie1 and movie2
def sim_distance(movie1,movie2):
    # A dictionary of movie ratings by different users
    prefs = {movie1:rate(movie1),movie2:rate(movie2)}

    items = [item for item in prefs[movie1].keys() if item in prefs[movie2].keys()]
    if len(items)==0:
        return 0.0
    # Add up the squares of all the differences of common rating item
    sum_of_squares=sum([pow(prefs[movie1][item]-prefs[movie2][item],2)
                        for item in items])

    return 1.0/(1+sum_of_squares)

# Return a list of movies that user (input argument) has rated in train files
def user_rated_movies(user):
    part = user_loc[user]
    f = open(part)
    info = f.read()
    ind = info.find('\n'+user)+1
    f.seek(ind)
    line = f.readline().replace('\n','')
    f.close()
    mv = line.split('\t',1)[1]
    movies = mv.split(',')
    return movies

# Predict how a user will rate a movie by using a weighted average of rates the
# user gives to other movies
def getRate(user,movie,prefs=preference,similarity=sim_distance,rates=rate):
    rateSums = {}
    simSums = {}
    if movie not in prefs.keys():
        prefs[movie] = rates(movie)
    mvs = user_rated_movies(user)
    for item in mvs:
        if item not in prefs.keys():
            prefs[item] = rates(item)
    for other in mvs:
        # don't compare to oneself
        if other == movie:
            continue
        sim = similarity(movie,other)

        # ignore scores of zero or lower
        if sim<=0:
            continue
        else:
            rateSums[other] = prefs[other][user]
            simSums[other] = sim
    rate = sum([rateSums[item]*simSums[item] for item in rateSums.keys()])/sum(
        [simSums[item] for item in rateSums.keys()])
    return rate
    

def rmse(filename):
    f = open(filename)
    f1 = f.readline()
    err = 0.0
    n = 0
    while f1!='':
        movie,user,rating,time = f1.rstrip().split('\t')
        test = open('test/'+movie+'.txt')
        testfile = test.read()
        ind = testfile.find('\n'+user)
        line = testfile[ind:ind+20]        
        actual = line.split(',')[1]
        err = err+pow(float(rating)-float(actual),2)
        n = n+1
        test.close()
        f1 = f.readline()
    f.close()
    return sqrt(err/n)
