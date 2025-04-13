import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
data= pd.read_csv("D:/UK+Train+Rides/railway.csv")
#Display Basic info
print(data.info())
print(data.head())

#check for missing values
missing_values = data.isnull().sum()
print(missing_values)

#Handling the missing values



#Drop rows with critical missing values
data.dropna(subset=['Price', 'Departure Station', 'Arrival Destination'], inplace=True)

# Fill missing delay reasons with 'No Delay'
data['Reason for Delay'].fillna('No Delay', inplace=True)

# Fill missing 'Refund Request' with 'No'
data['Refund Request'].fillna('No', inplace=True)

# Fill missing 'Railcard' with 'No Railcard'
data['Railcard'].fillna('No Railcard', inplace=True)

# Fill missing 'Actual Arrival Time' with 'mode of Actual Arrival Time'
data['Actual Arrival Time'].fillna(data["Actual Arrival Time"].mode()[0], inplace=True)

#1. Objective Ticket Sales Trends by Line Plot Graph

data['Date of Purchase'] = pd.to_datetime(data['Date of Purchase'])

sales_over_time = data.groupby('Date of Purchase')['Price'].sum()
plt.figure(figsize=(10, 6))
sales_over_time.plot(kind='line')
plt.title('Total Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales (£)')
plt.grid(True)
plt.show()

#2. Objective Delay Patterns  on Heatmap

data['Departure Hour'] = pd.to_datetime(data['Departure Time'], format='%H:%M:%S').dt.hour

delayed_data = data[data['Journey Status'] == 'Delayed']

heatmap_data = delayed_data.pivot_table(index='Departure Station', columns='Departure Hour', aggfunc='size', fill_value=0)

plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap='Reds', annot=True, fmt='d')
plt.title('Number of Delays by Station and Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Departure Station')
plt.show()

#3. Objective Ticket Pricing Insights on Box plot

plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x='Ticket Type', y='Price',palette='magma')
plt.title('Ticket Prices by Ticket Type')
plt.xlabel('Ticket Type')
plt.ylabel('Price (£)')
plt.grid(True)
plt.show()

#4. Objective Journey Delays on Bar Chart

data['Scheduled Arrival'] = pd.to_datetime(data['Arrival Time'], format='%H:%M:%S')

data['Actual Arrival'] = pd.to_datetime(data['Actual Arrival Time'], format='%H:%M:%S')

data['Delay Minutes'] = (data['Actual Arrival'] - data['Scheduled Arrival']).dt.total_seconds() / 60

data['Route'] = data['Departure Station'] + ' → ' + data['Arrival Destination']

route_delays = data.groupby('Route')['Delay Minutes'].mean().dropna()

plt.figure(figsize=(14, 8))
route_delays.sort_values(ascending=False).plot(kind='bar')
plt.title('Average Delay by Route')
plt.xlabel('Route')
plt.ylabel('Average Delay (minutes)')
plt.grid(True)
plt.show()

#5. Objective Price vs Journey Distance on Scatter Plot

np.random.seed(0)
data['Estimated Distance (km)'] = np.random.randint(50, 500, size=len(data))

plt.figure(figsize=(10, 6))
plt.scatter(data['Estimated Distance (km)'], data['Price'],color='crimson')
plt.title('Ticket Price vs Estimated Journey Distance')
plt.xlabel('Estimated Distance (km)')
plt.ylabel('Price (£)')
plt.grid(True)
plt.show() 
