% Visualize the statistics in the project and create corresponding figure
% Need to run python script first to output the file in the directory
cwd = pwd;

% Movie statistics
importfile(strcat(cwd,'\movie_stat'));
[n,xout] = hist(data(:,1),50);
bar(xout,n)
set(gca,'YScale','log')
% labels
xlabel('Number of audience')
ylabel('Counts of movie')
title('Distribution of movie popularity')

% User statistics
importfile1(strcat(cwd,'\user_stat'));
figure
[n,xout] = hist(user_stat(:,2),50);
bar(xout,n)
set(gca,'YScale','log')
% labels
xlabel('Number of movies wathced')
ylabel('Counts of user')
title('Distribution of user record')

% Runtime statistics
importfile(strcat(cwd,'\result'));
figure
hist(data(:,3)/60)  % convert time to minutes
% labels
xlabel('Prediction Time (min)')
ylabel('Counts')
title('Distribution of runtime for recommendation')

% Accuracy statistics
importfile1(strcat(cwd,'\error_stat'));
figure
hist(error_stat(:,3))
% labels
xlabel('Error (prediction-actual)')
ylabel('Counts')
title('Distribution of error')

