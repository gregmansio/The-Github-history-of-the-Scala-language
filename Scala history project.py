# ## 1. Scala's real-world project repository data
# Importing pandas, matplotlib, nbconvert
import pandas as pd
import matplotlib
import nbconvert

# Loading in the data
pulls_one = pd.read_csv('pulls_2011-2013.csv')
pulls_two = pd.read_csv('pulls_2014-2018.csv')
pull_files = pd.read_csv('pull_files.csv')


# ## 2. Preparing and cleaning the data
# Append pulls_one to pulls_two
pulls = pd.concat([pulls_two, pulls_one], verify_integrity=True, ignore_index=True)

# Convert the date for the pulls object
pulls['date'] = pd.to_datetime(pulls['date'], utc = True)


# ## 3. Merging the DataFrames
# Merge the two DataFrames
data = pulls.merge(pull_files, on = 'pid', suffixes = ('_req', '_files'), validate = 'one_to_many')


# ## 4. Is the project still actively maintained?
# Create a column that will store the month
data['month'] = data['date'].dt.month

# Create a column that will store the year
data['year'] = data['date'].dt.year

# Group by the month and year and count the pull requests
counts = data.groupby(['year', 'month'])['pid'].count()

# Plot the results
counts.plot(kind='bar', figsize = (20,6), rot = 40, title = 'Number of contributions per month')


## %% 5. Is there camaraderie in the project?
# Group by the submitter
by_user = data.groupby('user').count()
by_user = by_user.sort_values('pid')

# Plot the histogram
countspull = by_user['pid'].plot(kind = 'bar', title = 'Number of pull requests by yeach user', figsize = (20,6), logy = True)
countspull.grid(axis = 'y')
countspull.axhline(by_user['pid'].median(), linestyle = 'dashed')

# ## 6. What files were changed in the last ten pull requests?
# Identify the last 10 pull requests
last_10 = pulls.sort_values('date')[-10:]
#print(last_10.head())

# Join the two data sets
joined_pr = last_10.merge(pull_files, on = 'pid')
#print(joined_pr.head())

# Identify the unique files
files = set(joined_pr['file'].unique())

# Print the results
files


# ## 7. Who made the most pull requests to a given file?
# This is the file we are interested in:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Identify the commits that changed the file
file_pr = data[data['file'] == file]

# Count the number of changes made by each developer
author_counts = file_pr.groupby('user').count()

# Print the top 3 developers
author_counts.nlargest(3, 'file')


# ## 8. Who made the last ten pull requests on a given file?
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests that changed the target file
file_pr = data[data['file'] == file]

# Merge the obtained results with the pulls DataFrame
joined_pr = file_pr.merge(pulls, on = 'pid')

# Find the users of the last 10 most recent pull requests
users_last_10 = set(joined_pr.nlargest(10, 'date_x')['user_x'])

# Printing the results
users_last_10


# ## 9. The pull requests of two special developers
# The developers we are interested in
authors = ['xeno-by', 'soc']

# Get all the developers' pull requests
by_author = pulls[pulls['user'].isin(authors)]
#print(by_author.head())

# Count the number of pull requests submitted each year
counts = by_author.groupby([by_author['user'], by_author['date'].dt.year]).agg({'pid': 'count'}).reset_index()

# Convert the table to a wide format
counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)

# Plot the results
counts_wide.plot(kind='bar')


# ## 10. Visualizing the contributions of each developer
authors = ['xeno-by', 'soc']
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Merge DataFrames and select the pull requests by the author
by_author = data[data['user'].isin(authors)]

# Select the pull requests that affect the file
by_file = by_author[by_author['file'] == file]

# Group and count the number of PRs done by each user each year
grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()

# Transform the data into a wide format
by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)

# Plot the results
by_file_wide.plot(kind='bar')

