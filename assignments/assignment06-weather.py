# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.ticker as mtick
import requests
import plotly.express as px
from matplotlib.widgets import Slider

# (I.) Read in the data
# References:
    # https://www.geeksforgeeks.org/how-to-fix-python-pandas-error-tokenizing-data/
url = 'https://cli.fusio.net/cli/climate_data/webdata/hly4935.csv'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(url, skiprows=23,low_memory=False)
    print(df.head())
else:
    print("Failed to retrieve the file. Status code:", response.status_code)

# _______________________________
# (II.) Data cleaning and wrangling

# Convert the date column to a datetime format
# References: https://docs.osmos.io/data-transformations/formulas/date-and-time-formulas/date-format-specifiers
df['date_time'] = pd.to_datetime(df['date'], format='%d-%b-%Y %H:%M')

# _______________________________
# (III.) First set of plots

# Setting plot and axis variables as subplots() which returns a tuple(fig, ax)
fig = plt.figure(figsize=(15, 8))
grid_spec = fig.add_gridspec(3, 2, height_ratios=[3, 1, 0.5])

# Large plot: temperature over time 
ax1 = fig.add_subplot(grid_spec[0, :])
ax1.plot(df['date_time'], df['temp'], color='darkblue')
ax1.set_title('Daily Temperature Over Time', fontsize=16)
ax1.set_xlabel('Date Time', fontsize=8)
ax1.set_ylabel('Temperature (°C)', fontsize=12)
ax1.legend(fontsize=12)
ax1.tick_params(axis='x', labelsize=8) 
ax1.grid()

# Smaller plot 1: daily mean temp
daily_mean_temp = df.groupby(['date_time'])['temp'].mean().reset_index()
ax2 = fig.add_subplot(grid_spec[1, 0])
ax2.plot(daily_mean_temp['date_time'], daily_mean_temp['temp'], color='darkgreen')
ax2.set_title('Daily Mean Temperature', fontsize=13)
ax2.set_xlabel('Date', fontsize=8)
ax2.set_ylabel('Temperature (°C)', fontsize=10)
ax2.legend(fontsize=8)
ax2.tick_params(axis='x', labelsize=8) 
ax2.grid()

# Smaller plot 2: monthly mean temp
monthly_mean_temp = df.groupby(['date_time'])['temp'].mean().reset_index()
ax3 = fig.add_subplot(grid_spec[1, 1])
ax3.plot(monthly_mean_temp['date_time'], monthly_mean_temp['temp'], color='darkred')
ax3.set_title('Monthly Mean Temperature', fontsize=14)
ax3.set_xlabel('Date', fontsize=8)
ax3.set_ylabel('Temperature (°C)', fontsize=10)
ax3.legend(fontsize=8)
ax3.tick_params(axis='x', labelsize=8)
ax3.grid()

# Add slider to control the date
# Reference: https://www.geeksforgeeks.org/python-scroll-through-plots/
slider_ax = fig.add_subplot(grid_spec[2, :])
slider_ax.axis('off')  
slider_widget = plt.axes([0.2, 0.02, 0.6, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(slider_widget, 'Date', 0, len(df['date_time']) - 1, valinit=0, valstep=1)

# update() function to change the graph when the
# slider is in use
def update(val):
    start = int(slider.val)
    end = start + int(len(df['date_time']) * 0.1)  # Show 10% of data at a time
    ax1.set_xlim(df['date_time'].iloc[start], df['date_time'].iloc[min(end, len(df['date_time']) - 1)])
    ax2.set_xlim(df['date_time'].iloc[start], df['date_time'].iloc[min(end, len(df['date_time']) - 1)])
    ax3.set_xlim(df['date_time'].iloc[start], df['date_time'].iloc[min(end, len(df['date_time']) - 1)])
    fig.canvas.draw_idle()

# Update function called using on_changed() function
slider.on_changed(update)

plt.show()

# _______________________________
# (IV.) Second set of plots
