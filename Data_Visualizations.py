"""
Basic Plotting: Introduction to matplotlib
In this section, we will:
-> Create basic plots using matplotlib.pyplot
-> Put axis labels and titles
-> Create multiple plots (subplots) in the same figure
-> Change the scales of x and y axes
-> Create common types of plots: Histogram, Boxplots, Scatter plots, etc
-> Working with images
matplotlib is a python library. It contains the pyplot module, which is basically a collection of functions such as plot, title, show() etc. pyplot is one of the most commonly used module for creating a variety of plots such as line plots, bar plots, histogram etc.

lets start with the basics

"""
"""
# Basic Plotting, Axes Labels and Titles

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import lineStyles
from matplotlib.ticker import PercentFormatter
from openpyxl.compat import product
from plotly.matplotlylib import renderer

x = [1,2,3,4,5]
y = [2,4,6,8,10]
plt.plot(x,y)
plt.title('Simple Line Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.show()

months = ['January','February','March','April','May','June']
stock_prices = [150,160,170,165,175,185]

# create a line plot
plt.figure(figsize=(8,5))
plt.plot(months,stock_prices, marker = 'o', linestyle = '-', color = 'b')
# add title and labels
plt.title('Stock Prices over Several Months')
plt.xlabel('Months')
plt.ylabel('Stock Price ($)')
plt.grid(True)
plt.show()


x = np.linspace(0,10,20)
y = x*2
plt.plot(x,y,'b+')
plt.xlabel('Current')
plt.ylabel('Voltage')
plt.title('Ohm\'s Law')
plt.show()

hours_studied = [1,2,3,4,5,6,7,8]
exam_scores = [50,55,60,65,70,75,80,85]
# create a scatter plot:
plt.figure(figsize=(8,5))
plt.scatter(hours_studied, exam_scores, color = 'r', marker = 'o')
# add title and labels:
plt.title('Correlations between hours studied and exam scores')
plt.xlabel('Hours studied')
plt.ylabel('Exam scores')
plt.grid(True)
plt.show()


# Advanced scatter plot
hours_studied = [1,2,3,4,5,6,7,8]
exam_scores = [50,55,60,65,70,75,80,85]
study_efficieny = [2,4,5,3,4,6,8,9]

# convert list to numpy arrays for trendline calculations:
x = np.array(hours_studied)
y = np.array(exam_scores)
# Create a figure and axis:
fig, ax = plt.subplots(figsize = (10,6))
# Scatter plot:
scatter = ax.scatter(x,y,c = study_efficieny, s = np.array(study_efficieny)*100, cmap = 'coolwarm', alpha = 0.6, edgecolor = 'k')
# c = study_efficieny - color of the points varies
# s = np.array(study_efficieny)*100 -  size of the points will increase based on the value
# alpha means transparency color
# Add a color bar to show what the color represents: (reprents the efficiency from low to high)
cbar = plt.colorbar(scatter)
cbar.set_label('Study Efficiency')
# Add annotations for specific points:
for i in range(len(x)):
    ax.annotate(f'{y[i]}',(x[i],y[i]),textcoords = "offset points",xytext = (5,-10),ha = 'center')
# add title and labels:
ax.set_title('Correlation between hours studied and exam scores with efficiency', fontsize = 14)
ax.set_xlabel('Hours Studied', fontsize = 12)
ax.set_ylabel('Exam scores', fontsize = 12)
# add grid for better readability:
ax.grid(True)
# add a trendline:
z = np.polyfit(x,y,1)
p = np.poly1d(z)
plt.plot(x,p(x),'r--',label = 'Trendline')
# ass a legend:
ax.legend()
plt.show()



# Plotting multiple lines on the same plot
# it can be used during statistic analysis
x = np.linspace(0,5,10)
y = np.linspace(3,6,10)
# the linspace is used for curve
# plot three curves: y,y**2 and y**3 with different line types
plt.plot(x,y,'r-',x,y**2,'b+',x,y**3,'g^')
plt.title('Multiple different line type ')
plt.xlabel('X values')
plt.ylabel('Y values')
# adding a legend:
plt.legend(['y','y^2','y^3'])
# adding a grid
plt.grid(True)
plt.show()

# Figures and Subplots
# To create multiple plots in the same figure, you can use the method plt.subplot(nrows,ncols,nsubplot).

x = np.linspace(1,10,100)
y = np.log(x)
# initiate a new figure explicitly
plt.figure(1)

# create a subplot with 1 row, 2 columns
plt.subplot(121) # plt.subplot(1,2,1)

# create the first subplot in figure 1
plt.title('y = log(x)')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.grid(True)
plt.plot(x,y,'r--')
# create the first subplot in figure 2
plt.subplot(122)
plt.title('y = log(x)**2')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.grid(True)
plt.plot(x,y**2)

plt.tight_layout() # give space from multiple subplots etc
plt.show()

# Example: Create a figure having 4 subplots
x = np.linspace(1,10,100)
# optional command, since matplotlib creates a figure by default anyway
plt.figure(1)
# subplot 1
plt.subplot(2,2,1)
plt.title("Linear")
plt.plot(x,x)

# subplot 2
plt.subplot(2,2,2)
plt.title("Cubic")
plt.plot(x,x**3)

for i in range(1,3):
    plt.subplot(2,2,i)
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.grid(True)
plt.tight_layout()

# subplot 3
plt.figure(2)
plt.subplot(2,2,1)
plt.title("Log")
plt.plot(x,np.log(x))

# subplot 4
plt.subplot(2,2,2)
plt.title("Exponential")
plt.plot(x,x**2)

# Adding labels and grid to each subplot:
for i in range(1,3):
    plt.subplot(2,2,i)
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.grid(True)
plt.tight_layout()
plt.show()


# Types of Commonly used plots
# Lets now use the retail stores sales data to create some commonly use plots such as:
# Area chart, Boxplots, Histogram, Scatter plots and Bar plots
months = np.arange(1,13)
organic_traffic = np.array([500,700,800,1000,1200,1400,1500,1600,1750,1800,1900,2000])
paid_traffic = np.array([200,300,400,500,600,650,700,750,800,900,1000,1100])
referral_traffic = np.array([100,150,200,250,300,350,400,450,500,600,700,800])
# Calculate cumulative traffic
total_traffic = organic_traffic + paid_traffic + referral_traffic
fig, ax = plt.subplots(figsize = (10,6))
ax.fill_between(months,0,organic_traffic,label = 'Organic Traffic', color = 'blue', alpha = 0.5)
ax.fill_between(months, organic_traffic,organic_traffic + paid_traffic, label = 'Paid Traffic', color = 'green', alpha = 0.5)
ax.fill_between(months, organic_traffic + paid_traffic, total_traffic,label = 'Referral Traffic', color = 'red', alpha = 0.5)
# Add Labels, title, grid:
ax.set_title('Buildup of Website Traffic from various sources (Jan-Dec)', fontsize = 16)
ax.set_xlabel('Months', fontsize = 12)
ax.set_ylabel('Traffic Volume', fontsize = 12)
ax.grid(True, which = 'both', linestyle = '--',linewidth = 0.5)

# adding legend:
ax.legend(loc = 'upper left', fontsize = 12)
# Annotate the max traffic point:
max_traffic = total_traffic.max()
max_month = months[total_traffic.argmax()]
ax.annotate(f'Max Traffic: {max_traffic}', xy = (max_month,max_traffic),xytext = (max_month + 1,max_traffic + 500),arrowprops = dict(facecolor = 'black',arrowstyle = '->',), fontsize = 10)
# Adding trendline on top of the area chart:
ax.plot(months,total_traffic, color = 'black', linestyle = '--', linewidth = 2, label = 'Total Trendline')
ax.legend()
plt.tight_layout()
plt.show()


# Bar Chart
# Basic Vertical
product_lines = ['Product A','Product B','Product C','Product D']
revenue = [50000,65000,80000,70000]

# sorted data:
sorted_data = sorted(zip(revenue, product_lines), reverse = True)
revenue_sorted, product_lines_sorted = zip(*sorted_data)
# create a bar chart:
plt.figure(figsize=(8,6))
bars = plt.bar(product_lines_sorted,revenue_sorted,color = 'skyblue')
# Add titles, labels:
plt.title('Annual Revenue by Product Lines',fontsize = 16)
plt.xlabel('Product Lines',fontsize = 12)
plt.ylabel('Revenue',fontsize = 12)
# Annotate each bar with the revenue value:
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, height, f'${height:.2f}', ha='center', va='bottom', fontsize=12)
plt.show()

# Grouped Bar Chart
product_lines = ['Product A', 'Product B','Product C']
regions = ['North','South','East','West']

# Sales data for each product
sales_north = [15000,20000,18000]
sales_south = [25000,30000,38000]
sales_east = [45000,45000,48000]
sales_west = [55000,58000,60000]

# combine sales data for easy processing:
sales_data = np.array([sales_north,sales_south,sales_east,sales_west])
fig, ax = plt.subplots(figsize = (10,6))
# create an index for the x locations:
index = np.arange(len(product_lines))
# define the bar width and positions for the groups:
bar_width = 0.2

# store the bar containers to access individual bars later:
all_bars = []

# Plot each group of bars side by side:
for i in range(len(regions)):
    bars = ax.bar(index+i * bar_width, sales_data[i], bar_width, label = regions[i], color = 'grey')
    all_bars.append(bars)

# Identify the highest bar for each product line and change its color to green:
for j in range(len(product_lines)):
    product_sales = sales_data[:,j]
    # Determine the index of the maximum sales volume for the product line:
    max_sales_index = np.argmax(product_sales)
    # Set the corresponding bars color to green:
    all_bars[max_sales_index][j].set_color('green')

# Add a black seperator line between groups of bars:
for j in range(len(product_lines) - 1):
    ax.axvline(x = (index[j] + 0.5),color = 'black', linewidth = 1.5)
# Annotate each bar with the sales value on the top:
for bars in all_bars:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,f'{height:,}',ha = 'center',va = 'bottom', fontsize = 10)


ax.set_title('Sales by region and product lines', fontsize = 16)
ax.set_xlabel('Product Line', fontsize = 12)
ax.set_ylabel('Sales (in USD)', fontsize = 12)
ax.set_xticks(index+bar_width*0.5)
ax.set_xticklabels(product_lines)
ax.legend()
plt.tight_layout()
plt.show()
# # plotting:
# ax.bar(index,sales_north,bar_width,label = 'North',color = 'b')
# ax.bar(index,sales_south,bar_width,label = 'South',color = 'g')
# ax.bar(index+ 2 * bar_width,sales_east,bar_width,label = 'East',color = 'r')
# ax.bar(index+ 3 * bar_width,sales_west,bar_width,label = 'West',color = 'orange')
# plt.show()



# Stacked Bar Chart
companies = ['Company A','Company B','Company C']
years = [2019,2020,2021]
# Market share for each company over the years:
share_2019 = [25,40,35]
share_2020 = [30,35,35]
share_2021 = [40,30,30]

# create a stacked bar chart:
fig, ax = plt.subplots(figsize = (8,6))
# plot the stacks:

ax.bar(years, share_2019, label = 'Company A',color = 'skyblue')
ax.bar(years, share_2020, label = 'Company B',bottom = share_2019,color = 'lightgreen')
ax.bar(years, share_2021, bottom = np.array(share_2019) + np.array(share_2020), label = 'Company C',color = 'red')

# add title and labels:
ax.set_title('Market Share Distribution Over Years', fontsize = 16)
ax.set_xlabel('Years', fontsize = 12)
ax.set_ylabel('Market Share (%)', fontsize = 12)
# Add a grid for easier comparision of market shares
ax.grid(axis = 'y', linestyle = '--',alpha = 0.7)
# calculate the total market share for each year
total_share = [ sum(x) for x in zip(share_2019,share_2020,share_2021)]
# Add a line plot to show the total market share over the years:
ax.plot(years,total_share, color = 'black', marker = 'o', linewidth = 2, label = 'Total Market Share')
# Add text labels to the line plot:
for i, total in enumerate(total_share):
    ax.text(i,total + 2, str(total) + '%', ha = 'center', color = 'black', fontsize = 10)
# Annotating the barchart with market share values for each company:
for i in range(len(years)):
    ax.text(i,share_2019[i]/2,str(share_2019) + '%', ha = 'center', color = 'black', fontsize = 10)
    ax.text(i,share_2019[i] + share_2020[i]/2, str(share_2020[i]) + '%', ha = 'center', color = 'black', fontsize = 10)
    ax.text(i,share_2019[i] + share_2020[i] + share_2021[i]/2, str(share_2021[i]) + '%', ha = 'center', color = 'black', fontsize = 10)
# formatting the y-axis to display percentage values:
ax.yaxis.set_major_formatter(PercentFormatter())

ax.legend(fontsize = 12)
# add annotation with insights about the trends:
ax.text(1,110,'Note: Company A gaineda significant market share un 2021', fontsize = 12, color = 'red')
plt.tight_layout()
plt.show()


departments = ['HR','Engineering','Sales','Marketing','Finance']
employee_count = [20,100,50,30,40]
# create a horizontal barchart:
plt.figure(figsize = (8,6))
plt.barh(departments,employee_count, color = 'purple')
# Add titles and labels:
plt.title("Number of employees by department", fontsize = 16)
plt.xlabel("Number of employees", fontsize = 12)
plt.ylabel("Departments", fontsize = 12)
plt.show()

# Sample data: Number of employees in different departments
departments = ['HR','Engineering','Sales','Marketing','Finance']
employee_count = [20,100,50,30,40]

# sort the department:
sorted_indices = np.argsort(employee_count)
departments = np.array(departments)[sorted_indices]
employee_count = np.array(employee_count)[sorted_indices]
# create a h bar chart:
plt.figure(figsize = (10,7))
# generate gradient colors based on employee count:
colors = plt.cm.viridis(np.linspace(0.2,0.8,len(departments)))
# Horizontal bars
bars = plt.barh(departments,employee_count, color = colors, edgecolor = 'black')
# Add title and labels:
plt.title("Number of employees by Department", fontsize = 18)
plt.xlabel("Number of employees", fontsize = 14)
plt.ylabel("Departments", fontsize = 14)
# add gridlines for better readability:
plt.grid(axis = 'x', linestyle = '--', alpha = 0.7)
# Add annotations to the bars:
for bar in bars:
    width = bar.get_width()
    plt.text(width + 3, bar.get_y() + bar.get_height()/2,f'{width}',va = 'center', fontsize = 12, color = 'black')
# Display the percentage of total employees on each bar:
total_employees = sum(employee_count)
for i, count in enumerate(employee_count):
    pct = count / total_employees * 100
    plt.text(count + 10, i,f'{pct: .1f}%', va = 'center', fontsize = 10, color = 'blue')
# adjust the x-axis limits to focus on the data range:
plt.xlim(0,max(employee_count)+20)
# adjust font sizes for better readability:
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.tight_layout()
plt.show()

# Sample data: Simulating website traffic over 12 months
months = np.arange(1,13)
organic_traffic = np.array([500,700,800,1000,1200,1400,1500,1600,1750,1800,1900,2000])
paid_traffic = np.array([200,300,400,500,600,650,700,750,800,900,1000,1100])
referral_traffic = np.array([100,150,200,250,300,350,400,450,500,600,700,800])

# create a stacked bar chart:
fig,ax = plt.subplots(figsize = (10,6))
# plot each stack:
ax.bar(months, organic_traffic, label = 'Organic traffic', color = 'green')
ax.bar(months, paid_traffic, bottom = organic_traffic, label = 'Paid Traffic', color = 'blue')
ax.bar(months, referral_traffic, bottom = np.array(organic_traffic) + np.array(paid_traffic) , label = 'Referral Traffic', color = 'orange')

# Add title and labels:
ax.set_title('Website Traffic by Source', fontsize = 16)
ax.set_xlabel('Months', fontsize = 12)
ax.set_ylabel('Number of Visitors', fontsize = 12)
# Legend:
ax.legend()
plt.tight_layout()
plt.show()



months = ['Jan','Feb','Mar','Apr','May']
organic_traffic = [300,400,500,600,700]
paid_traffic = [100,200,250,300,350]
referral_traffic = [50,100,150,200,250]
# calculate totals for percentage annotations:
total_traffic = np.array(organic_traffic) + np.array(paid_traffic) + np.array(referral_traffic)
# stacked barchart:
fig, ax = plt.subplots(figsize = (12,8))
# plot each stack:
organic_bars = ax.bar(months,organic_traffic, label = 'Organic traffic', color = '#2ca02c', edgecolor = 'black')
paid_bars = ax.bar(months, paid_traffic, bottom = organic_traffic,label = 'Paid traffic', color = '#1f77b4',edgecolor = 'black')
referral_bars = ax.bar(months, referral_traffic, bottom = np.array(organic_traffic) + np.array(paid_traffic) , label = 'Referral traffic', color = '#ff7f0e',edgecolor = 'black')

ax.set_title('Monthly Website Traffic by Source', fontsize = 18,fontweight = 'bold')
ax.set_xlabel('Months', fontsize = 14)
ax.set_ylabel('Number of Visitors', fontsize = 14)
ax.grid(True,which = 'both',axis = 'y',linestyle = '--',linewidth = 0.7,alpha = 0.7)
# add a legend outside the plot:
ax.legend(loc = 'upper left',bbox_to_anchor = (1,1) ,fontsize = 12)
# add annotations for each traffic source:
for i, (o,p,r,total) in enumerate(zip(organic_traffic,paid_traffic,referral_traffic,total_traffic)):
    ax.text(i,o/2,f'{o}\n({o / total: .1%})', ha = 'center',va = 'center' ,color = 'white', fontsize = 10)
    # paid traffic:
    ax.text(i,o+p/2,f'{p}\n({p/total: .1%})',ha = 'center',va = 'center' ,color = 'white', fontsize = 10)
    # Referral traffic:
    ax.text(i,o+p+r/2,f'{r}\n({r/total: .1%})', ha = 'center', va = 'center',fontsize = 10, color = 'white')

# Highlight the month with the highest total traffic:
max_traffic_month = months[np.argmax(total_traffic)]
ax.text(np.argmax(total_traffic),total_traffic.max() + 50,f'Max Traffic in {max_traffic_month}',ha = 'center',fontsize = 10, color = 'black', weight = 'bold', bbox = dict(facecolor = 'lightgrey',edgecolor = 'black',boxstyle = 'round', pad = 0.3))
plt.tight_layout(rect = [0,0,0.85,1])
plt.show()
"""

# Plotly
# Plotly is a comprehensive graphing library that helps create interactive visualizations and dashboards. It is widely used for data science and analytics due to its interactivity and easy of use.
# Originated from the need to create advanced,interactive plots beyond static images.
# import plotly.express as px
# df = px.data.gapminder()
# df_canada = df[df.country == 'Canada']
# px.line(df_canada, x = 'year', y = 'lifeExp', title = 'Life Expectancy in Canada', markers = True, labels = {'year': 'Year','lifeExp': 'Life Expectancy (Years)'})
# fig.show()

# this code is showing errors
# import plotly.graph_objects as go
# fig = go.Figure()
# fig.add_trace(go.Scatter(x = [1,2,3], y = [4,5,6], mode = 'lines+markers',marker = dict(size = 10,color = 'red', symbol = 'circle'),line = dict(width = 2, dash = 'dash'),name = 'Sample Data'))
# fig.update_layout(title = dict(text = 'Scatter plot with Lines and Markers', font = dict(size = 24), x = 0.5, xanchor = 'center'),xaxis = dict(title = 'X-Axis', showgrid = True, gridcolor = 'Lightgrey', zeroline = True,zerolinecolor = 'Grey', tickmode = 'linear',tick0 = 0,dtick = 1),yaxis = dict(title = 'Y-Axis', showgrid = True, gridcolor = 'LightGrey', zeroline = True, zerolinecolor = 'Grey'),plot_bgcolor = 'rgba(0,0,0,0)', hovermode = 'x', legend = dict(x = 0.02, y = 0.98, bgcolor = 'rgba(255,255,255,0.5)', bordercolor = 'Black', borderwidth = 1))
#
# fig.show()



# Line Charts
import plotly.express as px
df = px.data.gapminder()
print(df.head())
countries = ['United States','China','India','Brazil','Germany']
df_filtered = df[df['country'].isin(countries)]
fig = px.line(df_filtered,x = 'year', y = 'lifeExp', color = 'country', title = 'Life Expectancy Ober Time', markers = True)
fig.show()

# # Stock Prices Over Time
# import yfinance as yf
# stock_data = yf.download('AAPL',start = '2019-01-01', end = '2024-01-01')
# stock_data.reset_index(inplace = True)
# print(stock_data.head())
# fig = px.line(stock_data, x = 'Date', y = 'Close', title = 'Apple Inc. (APPL) Stock Price Over Time', markers = True)
# fig.show()

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
dates = pd.date_range(start = '2023-01-01', end = '2023-12-31')
np.random.seed(0)
tmp_nyc = np.random.normal(loc = 60,scale = 15, size = len(dates)) + np.sin(np.linspace(0,6*np.pi,len(dates))) * 15
tmp_la = np.random.normal(loc = 70, scale = 10,size = len(dates)) + np.sin(np.linspace(0,6*np.pi,len(dates))) * 10

# create a dataframe:
df_weather = pd.DataFrame({
    'Date': dates,
    'NYC_Temperature': tmp_nyc,
    'LA_Temperature': tmp_la
})
print(df_weather.head())

fig = go.Figure()
fig.add_trace(go.Scatter(x = df_weather['Date'], y = df_weather['NYC_Temperature'],mode = 'lines+markers',name = 'NYC_Temperature',line = dict(color = 'royalblue', width = 2, dash = 'solid'), marker = dict(size = 4, color = 'royalblue')))
fig.add_trace(go.Scatter(x = df_weather['Date'], y = df_weather['LA_Temperature'], mode = 'lines+markers',name = 'LA Temperature', line = dict(color = 'orange', width = 2,dash = 'dot'),marker = dict(size = 4, color = 'orange')))
fig.update_layout(title = 'Average Daily Temperature Over Time (NYC vs. LA)', xaxis_title = "Date",yaxis_title = "Temperature (F)", xaxis = dict(rangeselector = dict(buttons = list([dict(count = 1, label = '1m',step = 'month',stepmode = 'backward'),dict(count = 3,label = '3m', step = 'month', stepmode = 'backward'),dict(count = 6, label = '6m',step = 'month', stepmode = 'backward'),dict(step = 'all')])), rangeslider = dict(visible = True), type = "date"))
fig.update_traces(hovertemplate = 'Date: %{x}<br>Temperature: %{y}F')
fig.add_vrect(x0 = '2023-06-01',x1 = '2023-09-01',fillcolor = 'green', opacity = 0.2, layer = 'below', line_width = 0, annotation_text = "Summer", annotation_position = "top left")
fig.show()


# Bar Chart
df = px.data.iris()
print(df.head())
df_avg = df.groupby('species').agg({'petal_length': 'mean'}).reset_index()
px.bar(df,x = 'species', y = 'petal_length', title = 'Average Petal Length by Species', labels = {'species': 'Iris Species','petal_length': 'Petal Length (cm)'}, color = 'species')
fig.update_layout(yaxis = dict(title = 'Average Petal Length (cm)', tickmode = 'linear'),xaxis_title = 'Iris Species', title_font_size = 20)
fig.show()

np.random.seed(42)
regions = ['North','South','East','West','Central']
total_sales = np.random.randint(5000,15000,size = 5)
sales_std = np.random.randint(500,1500,size = 5)
df_sales = pd.DataFrame({'Region': regions,'Total Sales': total_sales,'Sales STD': sales_std})
df_sales = df_sales.sort_values(by = 'Total Sales', ascending = False)
print(df_sales.head())

fig = px.bar(df_sales, x = 'Region', y = 'Total Sales',title = 'Total Sales by Region', labels = {'Total Sales': 'Total Sales (USD)', 'Region': 'Sales Region'},color = 'Region',text = 'Total Sales', error_y = 'Sales STD', template = 'plotly')
fig.update_layout(yaxis = dict(title = 'Total Sales (USD)', tickmode = 'linear'), xaxis_title = 'Sales Region', title_font_size = 22, uniformtext_minsize = 10, uniformtext_mode = 'hide',showlegend = False)
max_region = df_sales.iloc[0]['Region']
max_sales = df_sales.iloc[0]['Total Sales']

fig.add_annotation(x = max_region,y = max_sales + 500, text = f"Highest sales in {max_region}",showarrow = True, arrowhead = 2, ax = 0, ay = -40, font = dict(color = 'green',size = 12, family = 'Arial'),arrowcolor = 'green')
fig.show()

# Pie Chart - used for market share and budget allocations
df = px.data.iris()
fig = px.pie(df, names = 'species', title = 'Distributions of species in Iris Dataset')
fig.show()


data = {'Company':['Apple','Samsung','Huawei','Xiomi','Oppo'],
        'Market Share': [30,25,20,15,10]}
df_market_share = pd.DataFrame(data)
print(df_market_share.head())
fig = px.pie(df_market_share,names = 'Company', values = 'Market Share', title = 'Smartphone market share (2024)', color_discrete_sequence = px.colors.sequential.RdBu, hole = 0.2)
fig.update_traces(textposition = 'inside',textinfo = 'percent+label',pull = [0.1,0,0,0,0], marker = dict(line = dict(color = '#000000', width = 2)))
fig.update_layout(legend_traceorder = 'reversed', piecolorway = px.colors.sequential.Viridis)
# fig.update_trace(visible = 'legendonly') - it shows only the legends in the plot
# fig.update_traces(rotation = 90)
fig.update_traces(visible = True, selector = dict(type = 'pie'))
fig.show()


# Basic Dashboard using plotly