# author: Siheng He (Email: sh2980@columbia.edu)

import os
from shutil import copyfile

# Create the movie statistcs file to provide data to MATLAB for visualization
def create_mv_statistic_file():
    n_file = len(os.listdir('train'))
    f = open('movie_stat','w')
    for i in range(1,n_file+1):
        index = '0000000'+str(i)
        mv_name = 'mv_'+index[-7:]
        f1 = open('train/'+mv_name+'.txt')
        f2 = f1.readlines()
        f.write(mv_name+'\t'+str(len(f2)-1)+'\n')
    f.close()

# Create the movie statistcs file to provide data to MATLAB for visualization
def create_usr_statistic_file():
    g = open('user_stat','w')
    for i in range(26):
        num = '0000'+str(i)
        loc = 'part-'+num[-5:]
        f = open(loc)
        line = f.readline()
        while line!='':
            usr,mv = line.split('\t',1)
            n_mv = len(mv.split(','))
            g.write(usr+'\t'+str(n_mv)+'\n')
            line = f.readline()
        f.close()
    g.close()


# Create the error statistcs file to provide data to MATLAB for visualization
def create_error_statistic_file(filename):
    f = open(filename)
    g = open('error_stat','w')
    f1 = f.readline()
    while f1!='':
        movie,user,rating,time = f1.rstrip().split('\t')
        test = open('test/'+movie+'.txt')
        testfile = test.read()
        ind = testfile.find('\n'+user)
        line = testfile[ind:ind+20]
        actual = line.split(',')[1]
        err = float(rating)-float(actual)
        g.write(actual+'\t'+rating+'\t'+str(err)+'\n')
        test.close()
        f1 = f.readline()
    f.close()
    g.close()
# create address dictionanry, whose key is user id and value is the filename
# that contain the user information. The files are from the output of Amazon
# ElasticMapReduce job
def create_address():
    uf_loc = {}
    for i in range(26):
        num = '0000'+str(i)
        loc = 'part-'+num[-5:]
        f = open(loc)
        line = f.readline()
        while line!='':
            usr = line.split('\t',1)[0]
            uf_loc[usr] = loc
            line = f.readline()
        f.close()
    return uf_loc

# create one single file containing the users and movies, which is later
# used by MapReduce job
def create_user_file():
    names = os.listdir('train')
    train_file = open('trainfile','a')
    for name in names:
        f = open('train/'+name).read()
        ind = f.find(':')+2
        f1 = f[ind:]
        f2 = f1.replace('\n',','+name[:-4]+'\n')
        train_file.write(f2)
    train_file.close()

# split training_set data into train data and test data, based on file probe.txt
def prepare():
    cwd = os.getcwd()
    probe_file = cwd+'/probe.txt'
    train_dir = cwd+'/train'
    test_dir = cwd+'/test'
    movie_dir = cwd+'/training_set'
    n_movie = len(os.listdir(movie_dir))
    try:
        os.mkdir(train_dir)
        os.mkdir(test_dir)
    except OSError:
        print ''
    f = open(probe_file)
    probe = f.read()
    
    for i in range(1,n_movie+1):
        index = '0000000'+str(i)
        mv_name = 'mv_'+index[-7:]+'.txt'
        where = probe.find('\n'+str(i)+':')+1
        src = movie_dir+'/'+mv_name
        dst1 = train_dir+'/'+mv_name
        dst2 = test_dir+'/'+mv_name
        if where == -1:
            copyfile(src,dst1)
        else:
            f.seek(where)
            f.readline()
            usr = f.readline()
            test_list = []
            while usr[-2:]!=':\n' and usr!='':
                test_list.append(usr.replace('\n',''))
                usr = f.readline()
            mv_file = open(src)
            train_file = open(dst1,'a')
            test_file = open(dst2,'a')
            content = mv_file.readlines()
            train_file.write(content[0])
            test_file.write(content[0])
            for j in range(1,len(content)):
                rate = content[j].split(',')
                usr_id = rate[0]
                if usr_id in test_list:
                    test_file.write(content[j])
                else:
                    train_file.write(content[j])
            train_file.close()
            test_file.close()
    print 'Successfully split data into training and testing sets!'
    f.close()
    return
