import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

uber_df = pd.read_csv('uberdrive.csv')
print("Head: ",uber_df.head())
print("Tail: ",uber_df.tail())
uber_df.drop(uber_df.index[-1], inplace = True)
print("Removed the last row (total): ",uber_df)
# uber_df[:-1] - removing the last row using slicing method
print("Shape: ",uber_df.shape) # shows the row and column - shape is an attribute not an method, so paranthesis is no need
print("Info: ",uber_df.info()) # it is a method (functions for object)
print("Size: ",uber_df.size) # it is also an attribute -> output: 8085 ~ 1155*7 = 8085
print("Columns: ",uber_df.columns) # displaying the columns name
print("Columns in list: ",list(uber_df.columns))
print("Datatypes of column: ", uber_df.dtypes) # object are generic types (string) or (sometimes it maybe mixed with string and numeric)
print("Accessing the columns: ",uber_df.select_dtypes(include = ['str']))

""" Data Preprocessing """
print("Summarizing the null values: ",uber_df.isnull().sum())

"""  Having doubt in this 
uber_df = uber_df['PURPOSE*'].fillna('NOT', inplace = True) # replacing NULL with NOT
"""

""" Check for Duplicates """
print("Checking for duplicate: ",uber_df[uber_df.duplicated()])
print("Removing duplicate rows: ",uber_df.drop_duplicates(inplace = True))
print("Statistical summary (describe): ", uber_df.describe())

# Changing date format
uber_df['START_DATE*'] = pd.to_datetime(uber_df['START_DATE*'], errors = 'coerce')
uber_df['END_DATE*'] = pd.to_datetime(uber_df['END_DATE*'], errors = 'coerce')

# split date and time
from datetime import datetime
uber_df['date'] = pd.DatetimeIndex(uber_df['START_DATE*']).date
uber_df['hour'] = pd.DatetimeIndex(uber_df['START_DATE*']).hour
uber_df['time'] = pd.DatetimeIndex(uber_df['START_DATE*']).time
uber_df['day-night'] = pd.cut(x = uber_df['hour'], bins = [0,10,15,19,24], labels = ['Morning','Afternoon','Evening','Night'])



 ################ Data Visualization ################
 
plt.figure(figsize = (10,6))
sns.histplot(uber_df['MILES*'], bins = 20, color = 'pink', edgecolor = 'black', alpha = 0.7)
plt.xlabel('Miles')
plt.ylabel('Frequency')
plt.title('Distribution of Miles')
plt.show()

print(uber_df['START*'].unique()) # Shows the unqiue value
print(uber_df['START*'].nunique()) # display the count
print(uber_df['STOP*'].unique())
print(uber_df['STOP*'].nunique())
print(uber_df['START*'].value_counts().head(10))
plt.figure(figsize = (10,6))
sns.countplot(y = 'START*', order = uber_df['START*'].value_counts().head(10).index, data = uber_df, palette = 'viridis', edgecolor = 'black')
plt.xlabel('Count')
plt.ylabel('Start Location')
plt.title('Top 10 Most Frequent Start Locations ')
plt.show()

obj = (uber_df.dtypes == 'object')
object_cols = list(obj[obj].index)
unique_values = {}
for col in object_cols:
    unique_values[col] = uber_df[col].unique().size

print(unique_values)

plt.figure(figsize = (20,5))
plt.subplot(1,2,1)
sns.countplot(uber_df['CATEGORY*'], palette = 'Set2')
plt.xticks(rotation = 90) # xticks - controls properties such as the rotation, size, and color of the x-axis labels
plt.subplot(1,2,2)
sns.countplot(uber_df['PURPOSE*'], palette = 'Set3')
plt.xticks(rotation = 90) # rotation = 90 means showing the plots in horizontal
plt.tight_layout() # automatically adjust subplot for avoiding the overlap
plt.show()

sns.countplot(uber_df['day-night'], palette = 'coolwarm', edgecolor = 'black')
plt.xticks(rotation = 90)
plt.xlabel('Time of Days')
plt.ylabel('Count')
plt.title('Distributions of Day-Night Categories')
plt.show()

import warnings
# warnings.filterwarnings('once',message = 'deprecated') Show warning only once
# warning.filerwarnings('ignore',message = 'DeprecationWarning') Don't show warning
# warning.filerwarning('error', message = UserWarning) Treat warning as an error
warnings.filterwarnings('ignore') # This will says command to the python to ignore warning messages if any occurs - the warning will say about the issue occurs in the code

plt.figure(figsize = (10,6))
sns.countplot(data = uber_df, x = 'CATEGORY*', hue = 'day-night', palette = 'Set2')
plt.xticks(rotation = 90)
plt.title('Categories by Day-Night')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

plt.figure(figsize = (10,6))
sns.histplot(data = uber_df, x = 'CATEGORY*', hue = 'day-night', stat = 'probability', common_norm = False, palette = 'Set2')
plt.xticks(rotation = 90)
plt.title('Proportion of Categories by Day-Night')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

plt.figure(figsize = (10,6))
sns.countplot(data = uber_df, x = 'day-night', hue = 'CATEGORY*', palette = 'Set2')
plt.xticks(rotation = 90)
plt.title('Day-Night distribution by Ride Category')
plt.xlabel('Time of Day')
plt.ylabel('Count')
plt.show()

plt.figure(figsize = (10,6))
heatmap_data = uber_df.groupby(['PURPOSE*','day-night']).size().unstack() # size() will shows the no of occurance
sns.heatmap(heatmap_data, annot = True, cmap = 'YlGnBu', fmt = 'd') # annot = True prints the value inside, fmt = 'd' print the values in integer
plt.title('Heatmap of purpose vs Day-Night')
plt.xlabel('Day-Night')
plt.ylabel('Purpose')
plt.show()

# Propositional Heatmap
# cmap = 'coolwarm' -> it is used to show the high levels in darker shades
plt.figure(figsize = (10,6))
heatmap_data = uber_df.groupby(['PURPOSE*','day-night']).size().unstack()
heatmap_data = heatmap_data.div(heatmap_data.sum(axis = 1),axis = 0)
sns.heatmap(heatmap_data, annot = True, cmap = 'YlGnBu', fmt = '.2f')
plt.title('Propositional Heatmap of purpose vs Day-Night')
plt.xlabel('Day-Night')
plt.ylabel('Purpose')
plt.show()

# Aggregation heatmap
plt.figure(figsize = (10,6))
heatmap_data = uber_df.groupby(['CATEGORY*','PURPOSE*','day-night']).size().unstack(level = -1)
sns.heatmap(heatmap_data, annot = True, cmap = 'YlGnBu', fmt = 'd')
plt.title('Heatmap of purpose vs Day-Night')
plt.xlabel('Day-Night')
plt.ylabel('Purpose')
plt.show()

plt.figure(figsize = (10,6))
heatmap_data = uber_df.groupby(['PURPOSE*','day-night']).size().unstack()
total = heatmap_data.sum().sum()
sns.heatmap(heatmap_data, annot = heatmap_data.map(lambda x: f'{x}\n({x/total:.1%}'), cmap = 'YlGnBu', fmt = 's')
plt.title('Propositional Heatmap of purpose vs Day-Night')
plt.xlabel('Day-Night')
plt.ylabel('Purpose')
plt.show()

# Pie Chart
plt.figure(figsize = (8,8))
uber_df['CATEGORY*'].value_counts().plot.pie(autopct = '%1.1f%%', startangle = 90, cmap = 'Set3')
# autopct = '%1.1f%%' - it calculates for 100% prints in float
# startangle = 90 used to rotate the starting point of the first slice
plt.title('Proposition of categories')
plt.ylabel('')
plt.show()

# Exploded view
plt.figure(figsize = (8,8))
explode = [0.1 if cat == 'Business' else 0 for cat in uber_df['CATEGORY*'].value_counts().index]
uber_df['CATEGORY*'].value_counts().plot.pie(autopct = '%1.1f%%', startangle = 90,explode = explode, cmap = 'Set3')
plt.title('Proposition of Categories with Exploded Business Slice')
plt.ylabel('')
plt.show()

plt.figure(figsize = (8,8))
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
uber_df['CATEGORY*'].value_counts().plot.pie(autopct = '%1.1f%%', startangle = 90, colors = colors)
plt.title('Proposition of Categories ')
plt.ylabel('')
plt.show()

# Legends
plt.figure(figsize = (8,8))
uber_df['CATEGORY*'].value_counts().plot.pie(autopct = None, startangle = 90, cmap = 'Set3', labels = None)
plt.title('Proportion of Categories with Legend')
plt.ylabel('')
plt.legend(labels = uber_df['CATEGORY*'].value_counts().index, loc = 'upper right')
plt.show()

plt.figure(figsize = (8,8))
def autopct_with_counts(pct,values):
    total = sum(values)
    absolute = int(pct/100*total)
    return f'{pct: .1f}%\n({absolute})'

# autopct counts - total count of each slices
uber_df['CATEGORY*'].value_counts().plot.pie(autopct = lambda pct: autopct_with_counts(pct,uber_df['CATEGORY*'].value_counts()), startangle = 90, cmap = 'Set3')
plt.title('Proportion of Categories with Counts')
plt.ylabel('')
plt.show()


# Box Plot - covers only 50% of data, others are wishers,IQR and outliers
plt.figure(figsize = (10,6))
sns.boxplot(data = uber_df, x = 'day-night', y = 'MILES*', palette = 'coolwarm')
plt.title('Miles by Day-Night')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.show()

# Hue is used
plt.figure(figsize = (10,6))
sns.boxplot(data = uber_df, x = 'day-night', y = 'MILES*',hue = 'CATEGORY*', palette = 'coolwarm')
plt.title('Miles by Day-Night and Category')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.show()

# Individual data points with swarmplot
plt.figure(figsize = (10,6))
sns.boxplot(data = uber_df, x = 'day-night', y = 'MILES*', palette = 'coolwarm')
sns.swarmplot(data = uber_df, x = 'day-night',y = 'MILES*', color = 'black', size = 3)
plt.title('Miles by Day-Night with Individual data points')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.show()

# Category
plt.figure(figsize = (10,6))
sns.boxplot(data = uber_df, x = 'day-night', y = 'MILES*', palette = 'coolwarm')
plt.yscale('log') # it is looking very neat, clear and not congestted using logarithmic
plt.title('Miles by Day-Night and Category')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.show()

# Outliers Higheted
plt.figure(figsize = (10,6))
sns.boxplot(data = uber_df, x = 'day-night', y = 'MILES*', palette = 'coolwarm', showfliers = True, fliersize = 8)
plt.title('Miles by Day-Night with Outliers Highlighted')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.show()

# FacetGrid
g = sns.FacetGrid(uber_df, col = 'CATEGORY*', height = 6, aspect = 1.5)
g.map(sns.boxplot,'day-night','MILES*', palette = 'coolwarm')
g.set_axis_labels('Day-Night','Miles')
g.fig.suptitle('Miles by Day-Night split by Category', y = 1.05)
plt.show()

# Violin Plot - numerical variable distributions across different categories
plt.figure(figsize = (10,6))
sns.violinplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', palette = 'coolwarm')
plt.xticks(rotation = 90)
plt.title('Miles Distributions by purpose')
plt.show()

# Whitegrid
sns.set(style = 'whitegrid')
plt.figure(figsize = (10,6))
sns.violinplot(data = uber_df, x = 'day-night', y = 'MILES*', palette = 'coolwarm')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.title('Miles Distributions by Day-Night (Violin plot)')
plt.show()

# Adding hue = 'CATEGORY*'
sns.set(style = 'whitegrid')
plt.figure(figsize = (10,6))
sns.violinplot(data = uber_df, x = 'day-night', y = 'MILES*', hue = 'CATEGORY*', palette = 'coolwarm')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.title('Miles Distributions by Day-Night (Violin plot)')
plt.show()

# Printing in horizontal
sns.set(style = 'whitegrid')
plt.figure(figsize = (10,6))
sns.violinplot(data = uber_df, y = 'day-night', x = 'MILES*', hue = 'CATEGORY*', palette = 'coolwarm')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.title('Miles Distributions by Day-Night (Violin plot)')
plt.show()

# Inner = box - drawing box inside the violin plot
sns.set(style = 'whitegrid')
plt.figure(figsize = (10,6))
sns.violinplot(data = uber_df, y = 'day-night', x = 'MILES*',inner = 'box', palette = 'coolwarm')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.title('Miles Distributions by Day-Night (Violin plot) inner box')
plt.show()

# scale = width - shows all the violin plot in same width size
sns.set(style = 'whitegrid')
plt.figure(figsize = (10,6))
sns.violinplot(data = uber_df, y = 'day-night', x = 'MILES*',scale = 'width', palette = 'coolwarm')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.title('Miles Distributions by Day-Night (Violin plot) inner box')
plt.show()


# Bar plot - can give aggregate data(sum,avg,mean,median,mode,etc)
plt.figure(figsize = (10,6))
sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', estimator = sum, ci = None, palette = 'Set1')
plt.xticks(rotation = 30)
plt.title('Total Miles by Purpose')
plt.show()

# estimator = np.mean & estimator = np.median
plt.figure(figsize = (10,6))
sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', estimator = np.mean, ci = None, palette = 'Set1')
plt.xticks(rotation = 30)
plt.title('Mean Miles by Purpose')
plt.show()

# Removing confidence interval - ci = None, for horizonal change only the x and y positions
plt.figure(figsize = (10,6))
sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', estimator = sum, ci = 68, palette = 'Set1')
plt.xticks(rotation = 30)
plt.title('Mean Miles by Purpose')
plt.show()

# count plot
plt.figure(figsize = (10,6))
sns.countplot(data = uber_df, x = 'PURPOSE*', palette = 'Set1')
plt.xticks(rotation = 30)
plt.title('Count of trips by purpose')
plt.show()

# adding hue
plt.figure(figsize = (10,6))
sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*',hue = 'day-night', estimator = sum, ci = None, palette = 'Set1')
plt.xticks(rotation = 30)
plt.title('Total Miles by Purpose and Day-Night')
plt.show()

# Sorting the bar plot
plt.figure(figsize = (10,6))
order = uber_df.groupby('PURPOSE*')['MILES*'].sum().sort_values(ascending = False).index
sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', estimator = sum, ci = None, order = order, palette = 'Set1')
plt.xticks(rotation = 30)
plt.title('Total Miles by Purpose (Sorted)')
plt.show()


# adding fontsize, ha - horizontal
plt.figure(figsize = (10,6))

sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', estimator = sum, ci = None, palette = 'Set1')
plt.xticks(rotation = 30, ha = 'right', fontsize = 12)
plt.xlabel('Trip Purpose', fontsize = 14)
plt.ylabel('Total Miles', fontsize = 14)
plt.title('Trip Purpose')
plt.show()

# annotations - values of the height at tht top of each bar
plt.figure(figsize = (10,6))

ax = sns.barplot(data = uber_df, x = 'PURPOSE*', y = 'MILES*', estimator = sum, ci = None, palette = 'Set1')

for p in ax.patches: # patches means looping in each bar chart
    ax.annotate(f'{p.get_height(): .1f}',(p.get_x() + p.get_width()/2., p.get_height()), ha = 'center', va = 'center',xytext = (0,9), textcoords = 'offset points')
    # annotate means - x coordinate of the bar and calculate with width to find the height.
    # xytext = (0,9)->(x,y) displaying the text value in y axis (with distance of 9 units) , textcoords = 'offset points' - looping from each bar to display it neatly
plt.xticks(rotation = 30, ha = 'right', fontsize = 12)
plt.title('Total Miles by Purpose (with annotations)')
plt.show()



import warnings
warnings.filterwarnings('ignore') # This will says command to the python to ignore warning messages if any occurs - the warning will say about the issue occurs in the code
print(uber_df.columns)

# Scatter plot - Eg: sales, advertisement. Can find correlations, annomalis, error, data entry. each point is close means - strong correlations and relationship, scattered plot means - no correlations or weak
plt.figure(figsize = (10,6))
sns.scatterplot(data = uber_df, x = 'hour', y = 'MILES*', hue = 'CATEGORY*')
plt.title('Miles vs Time by Category')
plt.show()

# Regplot
plt.figure(figsize = (10,6))
sns.regplot(data = uber_df, x = 'hour', y = 'MILES*', scatter_kws = {'s':10}, line_kws = {'color':'red'})
plt.title('Miles vs Time with Trend Line')
plt.show()

# FacetGrid
g = sns.FacetGrid(uber_df, col = 'CATEGORY*', height = 5, aspect = 1.5)
g.map(sns.scatterplot, 'hour', 'MILES*')
g.add_legend()
plt.show()

# adding size
plt.figure(figsize = (10,6))
sns.scatterplot(data = uber_df, x = 'hour', y = 'MILES*', hue = 'CATEGORY*', sizes = (20,200))
plt.title('Miles vs Time by Category (Point size by durations)')
plt.show()

# Log
plt.figure(figsize = (10,6))
sns.scatterplot(data = uber_df, x = 'date', y = 'MILES*', hue = 'CATEGORY*', sizes = (20,200))
plt.yscale('log')
plt.title('Miles vs Time by Category (Log scale)')
plt.show()

# Stripplot using jitterplot  - show ellongate in y axis
plt.figure(figsize = (10,6))
sns.stripplot(data = uber_df, x = 'date', y = 'MILES*', hue = 'CATEGORY*', jitter = True)
plt.title('Miles vs Time by Category (with jitter)')
plt.show()

# alpha = 0.5 for points in transpareny
plt.figure(figsize = (10,6))
sns.scatterplot(data = uber_df, x = 'date', y = 'MILES*', hue = 'CATEGORY*', alpha = 0.5)
plt.title('Miles vs Time by Category (with transparency)')
plt.show()

# plots from start to end date
def round(x):
    if x['START*'] == x['STOP*']:
        return 'Yes'
    else:
        return 'No'
uber_df['ROUND_TRIP'] = uber_df.apply(round,axis = 1) # this will creates a new columns - will store the result of the functions
sns.countplot(uber_df['ROUND_TRIP'])
plt.show()

uber_df['MONTH'] = pd.DatetimeIndex(uber_df['START_DATE*']).month # creating new column month
print(uber_df['MONTH'])
dict = {1: 'Jan',2: 'Feb',3: 'Mar',4: 'Apr',5: 'May', 6: 'Jun',7: 'Jul',8: 'Aug', 9: 'Sep',10: 'Oct',11: 'Nov',12: 'Dec'}
uber_df['MONTH'] = uber_df['MONTH'].map(dict)
print(uber_df['MONTH'])
plt.figure(figsize = (15,7))
sns.countplot(uber_df['MONTH'])
plt.show()

print(uber_df.groupby(['MONTH','PURPOSE*'])['ROUND_TRIP'].count())


# Minutes taken to cover miles ?
uber_df['MINUTES'] = uber_df['END_DATE*'] - uber_df['START_DATE*']
print(uber_df.head())

# Line plot - converting seconds to minutes to print as Miles travelled in minutes
sns.lineplot(data = uber_df, x = uber_df['MINUTES'].dt.total_seconds() / 60, y = uber_df['MILES*'])
plt.show()

# Boxplot - subplot using purpose vs miles and minutes
plt.figure(figsize = (10,5))
plt.subplot(1,2,1)
sns.boxplot(data = uber_df, x = uber_df['PURPOSE*'], y = uber_df['MILES*'])
plt.xticks(rotation = 45)
plt.subplot(1,2,2)
sns.boxplot(data = uber_df, x = uber_df['PURPOSE*'], y = uber_df['MINUTES'])
plt.xticks(rotation = 45)

plt.show()

# For each purpose what is minimum miles travelled, mean miles travelled and what is maximum miles travelled?
print(pd.DataFrame({'Min': uber_df.groupby(['PURPOSE*'])['MILES*'].min(),
              'Mean': uber_df.groupby(['PURPOSE*'])['MILES*'].mean(),
              'Max': uber_df.groupby(['PURPOSE*'])['MILES*'].max()}))

# Round trip for every purpose every month?
pd.set_option('display.max_rows', None) # None means display all rows if it consist large set also
pd.set_option('display.max_columns', None) # if less number of row or column is printed the overall performance will get affected
pd.set_option('display.max_colwidth', 200) # if the character size is high we can give max width - if didn't mentioned the max_colwidth then the large character sentence will not print fully instead of that it will print(.........)
pd.set_option('display.float_format','{:.2f}'.format)
pd.set_option('display.precision',3) # float point numbers round to three number decimal places
data = {'Floats': [1.23456,86.34560,12.65432]}
df = pd.DataFrame(data)
pd.options.display.float_format = '{:,.1f}'.format
print(df)


pd.reset_option('display.expand_frame_repr')
data = {f'Column_{i}': list(range(5)) for i in range(15)}
print(pd.DataFrame(data))

pd.reset_option('display.expand_frame_repr')
pd.set_option('display.expand_frame_repr', False) # prints the data in single line if space is not enough it an have an scroller options to view it completely
data = {f'Columns_{i}': list(range(500)) for i in range(10)}
df = pd.DataFrame(data)
print(df)
# pd.set_option('display.large_repr', 'info') # summary of text data
# print(df)
pd.reset_option('display.large_repr')
print(uber_df.groupby(['MONTH','PURPOSE*'])['ROUND_TRIP'].count())

""" Questions """
# Are there more rides on weekdays or weekends ?
uber_df['WEEKDAY'] = uber_df['START_DATE*'].dt.day_name() # converting date into day
plt.figure(figsize = (10,6))
sns.countplot(data = uber_df, x = 'WEEKDAY', order = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], palette = 'Set3')
plt.title('Number of Rides by Day of the Week')
plt.xlabel('Weekday')
plt.ylabel('Count')
plt.show()

# How many rides were round trips ?
round_trip_counts = uber_df['ROUND_TRIP'].value_counts()
print("How many rides were round trips: \n", round_trip_counts)

plt.figure(figsize = (10,6))
round_trip_counts.plot(kind = 'pie',autopct = '%1.1f%%', startangle = 90, colors = ['#ff9999','#66b3ff'])
plt.title('Proposition of Round Trips')
plt.ylabel('')
plt.show()

# What is the total miles traveled in each category (CATEGORY*) ?
total_miles_by_category = uber_df.groupby(['CATEGORY*'])['MILES*'].sum()
print("Total Miles by Category: \n",total_miles_by_category)
plt.figure(figsize = (10,6))
total_miles_by_category.plot(kind = 'bar',color = 'lightgreen')
plt.title('Total miles by category')
plt.xlabel('Category')
plt.ylabel('Total Miles')
plt.show()

# How does the ride count change across different months (MONTH) ?
plt.figure(figsize = (10,6))
sns.countplot(data = uber_df, x = 'MONTH', palette = 'Set1')
plt.title('Number of Rides by Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.show()

# Which starting location (START) has the highest number of rides
uber_df['START*'] = uber_df['START*'].replace('Kar?chi','Karachi')
top_start_locations = uber_df['START*'].value_counts().head(10)
print(top_start_locations)
plt.figure(figsize = (10,6))
ax = top_start_locations.plot(kind = 'bar',color = 'orange')
plt.title('Top 10 Starting Locations Number of Rides')
plt.xticks(rotation = 30)
plt.xlabel('Starting Location')
plt.ylabel('Count')

for p in ax.patches:
    ax.annotate(f'{p.get_height()}',(p.get_x()+ p.get_width()/2,p.get_height()), ha = 'center', va = 'bottom')
plt.show()

# What are the busiest time of day for rides ?
sorted_time_counts = uber_df['hour'].value_counts().sort_values(ascending = False)
plt.figure(figsize = (10,6))
ax = sns.countplot(data = uber_df, x = 'hour', palette = 'viridis', order = sorted_time_counts.index)
plt.title('Rides by Time of day')
plt.xlabel('Time of Day (Hours)')
plt.ylabel('Count')
for p in ax.patches:
    ax.annotate(f'{p.get_height()}',(p.get_x()+ p.get_width()/2,p.get_height()), ha = 'center', va = 'bottom')
plt.show()

# How many unique purpose (PURPOSE*) are there ?
uber_df.columns = (uber_df.columns.str.replace('*','',regex = False).str.replace(' ','').str.lower().str.strip())
print("How many unique purpose: ",uber_df['purpose'].nunique())

# What are the top 5 most common purpose for rides ?
print("What are the top 5 most common purpose for rides: ",uber_df['purpose'].value_counts().head(10))

# What is the longest and shortest ride durations for each (category) (business vs personal)
uber_df['ride_durations'] = (uber_df['end_date'] - uber_df['start_date']).dt.total_seconds()/60
durations_by_category = uber_df.groupby('category')['ride_durations'].agg(['min','max'])
print("What is the longest and shortest ride durations for each (category) (business vs personal): ",durations_by_category)

# What is the total number of miles traveled per month and which month had the most miles traveled ?
miles_by_month = uber_df.groupby('month')['miles'].sum()
most_miles_month = miles_by_month.idxmax()
print("total number of miles traveled per month and which month had the most miles traveled: ",most_miles_month,miles_by_month)

# What is the average number of rides per day for each day of the week ?
uber_df['weekday'] = uber_df['start_date'].dt.day_name()
rides_by_weekday = uber_df.groupby('weekday').size()
avg_rides_by_weekday = rides_by_weekday/uber_df['weekday'].nunique()
print("average number of rides per day for each week: ",avg_rides_by_weekday)

# Which start locations have the most round_trip rides, and how many ?
total_round_trip_locations = uber_df[uber_df['round_trip'] == 'Yes'].groupby('start').size().sort_values(ascending = False).head(5)
print("Total round trip locations: ", total_round_trip_locations)

# What is the average ride distance(miles) for rides that happen during differenct times of the day (day-night) ?
avg_day_night = uber_df.groupby('day-night')['miles'].mean()
print("Average ride distance (miles) during (day-night): ",avg_day_night)

# How many rides start and stop in the same location (start == stop) and how many miles do these rides cover on average ?
same_location_rides = uber_df[uber_df['start'] == uber_df['stop']]
num_same_locations_rides = same_location_rides.shape[0]
avg_miles_same_locations = same_location_rides['miles'].mean()
print("How many rides start and stop in the same location and how many miles do these rides cover on average: ",num_same_locations_rides,avg_miles_same_locations)

# Which purpose has the highest average ride durations and what is the average durations for that purpose ?
uber_df.groupby('purpose')['ride_durations'].mean()
valid_uber_df = uber_df.dropna(subset = ['purpose','ride_durations'])
avg_durations_by_purpose = valid_uber_df.groupby('purpose')['ride_durations'].mean()
print("what is the average durations for that purpose: ",avg_durations_by_purpose)
uber_df['ride_durations'].fillna(uber_df['ride_durations'].median(),inplace = True)
avg_durations_by_purpose = uber_df.groupby('purpose')['ride_durations'].mean()
print("what is the average durations for that purpose(fillna): ",avg_durations_by_purpose)


# What is the most common combination of start and stop locations and how many times does this combinations appear in the dataset ?
print(uber_df.groupby(['start','stop']).size().sort_values(ascending = False).head(2))

# What is the average time difference between the start of the first ride and the start of the next ride for each unique day ?
uber_df = uber_df.sort_values('start_date')
uber_df['next_ride'] = uber_df.groupby('date')['start_date'].shift(-1)
uber_df['time_diff'] = (uber_df['next_ride'] - uber_df['start_date']).dt.total_seconds() / 60
avg_time_diff = uber_df.groupby('date')['time_diff'].mean().dropna()
print(avg_time_diff)
