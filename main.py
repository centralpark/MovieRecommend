import os
import sys
import time

sys.path.append(os.getcwd())

import prepare
import recommendation

prepare.create_mv_statistic_file()
prepare.create_usr_statistic_file()

movies = ['mv_0013581','mv_0011328','mv_0008433','mv_0004607','mv_0000001',
          'mv_0000408']
# Predict the ratings corresponding to (movie,user) pair in test files in test
# folder
result = open('result','w')
for movie in movies:
    f = open('test/'+movie+'.txt')
    lines = f.readlines()
    f.close()
    user_list = []
    for i in range(1,len(lines)):
        line = lines[i]
        u = line.split(',',1)[0]
        user_list.append(u)

    for user in user_list:
        start = time.clock()
        test = recommendation.getRate(user,movie)
        print movie+'\t'+user+'\t'+str(test)
        print 'Prediction time: '+str(time.clock()-start)+' seconds\n'
        result.write(movie+'\t'+user+'\t'+str(test)+'\t'+str(time.clock()-start)
                     +'\n')
result.close()

# Evaluate accuracy
accuracy = recommendation.rmse('result')
print 'RMSE: '+str(accuracy)
prepare.create_error_statistic_file('result')

