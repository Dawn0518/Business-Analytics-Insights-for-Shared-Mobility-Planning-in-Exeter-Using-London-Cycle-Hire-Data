import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


lch_data = pd.read_csv("/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/merged.csv")
#lch_data.info()
#lch_data.shape

# descriptive analysis 1 - daily demand
lch_data['Start date'] = pd.to_datetime(lch_data['Start date'])
lch_data.sort_values(by= 'Start date', ascending= True, inplace= True)
#print(lch_data)
lch_data['Weekday'] = lch_data['Start date'].dt.day_name()
#print(lch_data)
lch_data['Date type'] = lch_data['Weekday'].apply(
    lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday'
)
#print(lch_data)

rentals_counts_by_weekday = lch_data.groupby('Weekday').size()
#print(rentals_counts_by_weekday)

#print(lch_data.head())
weekday_order = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]
rentals_counts_by_weekday = rentals_counts_by_weekday.reindex(weekday_order)

rentals_counts_by_datetype = lch_data.groupby('Date type').size()
#print(rentals_counts_by_datetype)

lch_data['Date'] = lch_data['Start date'].dt.date
daily_demand = (
    lch_data
      .groupby(['Date', 'Date type'])   
      .size()                          
      .reset_index(name='Demand')      
)
print(daily_demand)

daily_demand_stats = daily_demand.groupby('Date type')['Demand'].agg(['mean', 'median', 'std'])
print(daily_demand_stats)
daily_demand_stats.to_excel('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/daily_demand_stats.xlsx')

plt.figure()
plt.bar(rentals_counts_by_weekday.index, rentals_counts_by_weekday.values)
plt.xlabel('Weekday')
plt.ylabel('Number of Rentals')
#plt.title('Weekly Demand by Weekday')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/weekly_demand_by_weekday.png')
plt.show()


# descriptive analysis 2 - trip duration
lch_data['Duration (mins)'] = lch_data['Total duration (ms)']/1000/60
duration_stats = lch_data['Duration (mins)'].agg(['mean', 'median', 'std'])
print(duration_stats)
duration_stats_excel = duration_stats.reset_index()
duration_stats_excel.columns = ['Metric', 'Value']
duration_stats_excel.to_excel('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/duration_stats.xlsx')

count_under_20 = (lch_data['Duration (mins)'] < 20).sum()
count_20_or_more = (lch_data['Duration (mins)'] >= 20).sum()

total_trips = count_under_20 + count_20_or_more

duration_category_table = pd.DataFrame({
    'Duration Category': ['< 20 minutes', '≥ 20 minutes'],
    'Number of Trips': [count_under_20, count_20_or_more],
    'Percentage (%)': [
        count_under_20 / total_trips * 100,
        count_20_or_more / total_trips * 100
    ]
})

print(duration_category_table)
duration_category_table.to_excel('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/duration_category.xlsx')


plt.figure()
plt.bar(['< 20 min', '≥ 20 min'],
        [count_under_20, count_20_or_more])
plt.xlabel('Trip Duration Category')
plt.ylabel('Number of Trips')
#plt.title('Trips Under 20 Minutes vs 20 Minutes and Over')
plt.tight_layout()

plt.savefig('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/trip_duration.png')
plt.show()


# descriptive analysis 3 - bike type usage 

bike_usage_counts = lch_data['Bike model'].value_counts()
print(bike_usage_counts)

classic_bike_counts = (lch_data['Bike model'] == 'CLASSIC').sum()
ebike_counts = (lch_data['Bike model'] == 'PBSC_EBIKE').sum()

total_bike_counts = classic_bike_counts + ebike_counts

bike_category_table = pd.DataFrame({
    'Bike Category': ['CLASSIC', 'PBSC_EBIKE'],
    'Number of Bikes': [classic_bike_counts, ebike_counts],
    'Percentage (%)': [
        classic_bike_counts / total_bike_counts * 100,
        ebike_counts / total_bike_counts * 100
    ]
})

print(bike_category_table)
bike_category_table.to_excel('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/bike_usage_counts.xlsx')

labels = ['E-bike', 'Classic Bike']
sizes = [ebike_counts, classic_bike_counts]

plt.figure()
plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    labeldistance=0.4,
    pctdistance=0.6
)

plt.tight_layout()

plt.savefig('/Users/huangshuya/Desktop/BA/Topics in Business Analytics/Report/Clean Data/bike_type_usage.png')
plt.show()

