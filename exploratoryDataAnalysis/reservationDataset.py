import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

os.makedirs("figures", exist_ok=True)
trips = pd.read_csv('../backend/data/train_set.csv')

# Feature Engineering
trips["checkin"] = pd.to_datetime(trips["checkin"])
trips["checkout"] = pd.to_datetime(trips["checkout"])
trips["stay_duration"] = (trips["checkout"] - trips["checkin"]).dt.days
trips['checkin_month'] = trips['checkin'].dt.month
trips['is_cross_border'] = (trips['booker_country'] != trips['hotel_country']).astype(int)  # !!!



def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'


trips['season'] = trips['checkin_month'].apply(get_season)


# Stay Duration Distribution
plt.figure(figsize=(8, 5))
sns.histplot(trips["stay_duration"], bins=30)
plt.title("Stay Duration Distribution")
plt.xlabel("Days")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("figures/stay_duration_distribution.png")
plt.close()

# Number of Bookings per Trip
bookings_per_trip = trips.groupby("utrip_id").size()
plt.figure(figsize=(8, 5))
sns.histplot(bookings_per_trip, bins=100)
plt.title("Number of Bookings per Trip")
plt.xlabel("Bookings per Trip")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("figures/bookings_per_trip.png")
plt.close()

# Monthly Check-In Distribution
trips["checkin_month"] = trips["checkin"].dt.month
plt.figure(figsize=(8, 5))
sns.countplot(x="checkin_month", data=trips, palette="viridis")
plt.title("Monthly Check-in Distribution")
plt.xlabel("Month")
plt.ylabel("Number of Check-ins")
plt.tight_layout()
plt.savefig("figures/monthly_checkins.png")
plt.close()

# Unique Cities per Trip
num_cities_per_trip = trips.groupby('utrip_id')['city_id'].nunique().rename('num_cities_in_trip')
trips = trips.merge(num_cities_per_trip, on='utrip_id')

# Trip Duration
trip_start = trips.groupby('utrip_id')['checkin'].min()
trip_end = trips.groupby('utrip_id')['checkout'].max()
trip_length_days = (trip_end - trip_start).dt.days.rename('trip_length_days')
trips = trips.merge(trip_length_days, on='utrip_id')


def plot_box(column, by, title, xlabel, ylabel, filename):
    plt.figure(figsize=(8, 6))
    trips.boxplot(column=column, by=by)
    plt.title(title)
    plt.suptitle('')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(os.path.join("figures", filename))
    plt.close()


plot_box('trip_length_days', 'season', 'Trip Length by Season', 'Season', 'Trip Length (days)',
         'trip_length_by_season.png')

plot_box('num_cities_in_trip', 'season', 'Number of Cities per Trip by Season', 'Season', 'Number of Cities',
         'num_cities_by_season.png')

plot_box('trip_length_days', 'device_class', 'Trip Length by Device Type', 'Device Type', 'Trip Length (days)',
         'trip_length_by_device.png')

plot_box('num_cities_in_trip', 'device_class', 'Number of Cities per Trip by Device Type', 'Device Type',
         'Number of Cities', 'num_cities_by_device.png')

plot_box('trip_length_days', 'is_cross_border', 'Trip Length by Cross-Border Status', 'Is Cross-Border (0=No, 1=Yes)',
         'Trip Length (days)', 'trip_length_by_crossborder.png')

plot_box('num_cities_in_trip', 'is_cross_border', 'Number of Cities per Trip by Cross-Border Status',
         'Is Cross-Border (0=No, 1=Yes)', 'Number of Cities', 'num_cities_by_crossborder.png')

trips.to_csv("figures/cleaned_booking_multi_trip_dataset.csv", index=False)

