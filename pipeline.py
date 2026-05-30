import pandas as pd
import numpy as np

# 1. Φόρτωση των δύο συνόλων δεδομένων
df_mobility = pd.read_csv('urban_mobility_kozani_2025.csv')
df_events = pd.read_csv('local_events_kozani_2025.csv')

# 2. Διαχείριση ελλειπουσών τιμών (Cleaning)
# Στα δεδομένα κινητικότητας συμπληρώνουμε τα κενά με τη διάμεσο της κάθε στήλης
for col in ['BusPassengers', 'BikeTrips', 'ParkingOccupancy', 'TrafficCount']:
    df_mobility[col] = df_mobility[col].fillna(df_mobility[col].median())

# Στα δεδομένα εκδηλώσεων συμπληρώνουμε τα κατηγορικά κενά και τα αριθμητικά με 0
df_events['EventType'] = df_events['EventType'].fillna('No Event')
df_events['Zone'] = df_events['Zone'].fillna('No Event')
df_events['Attendance'] = df_events['Attendance'].fillna(0.0)
df_events['VenueCapacity'] = df_events['VenueCapacity'].fillna(0.0)

# 3. Συγχώνευση των DataFrames με βάση την Ημερομηνία (Data Fusion)
df_merged = pd.merge(df_mobility, df_events, on='Date', suffixes=('_mobility', '_event'))

# Μετονομασία στηλών για μεγαλύτερη σαφήνεια και αποφυγή διπλότυπων ονομάτων
df_merged.rename(columns={
    'City_mobility': 'City',
    'Zone_mobility': 'MobilityZone',
    'Zone_event': 'EventZone'
}, inplace=True)
df_merged.drop(columns=['City_event'], inplace=True, errors='ignore')

# 4. Υπολογισμός νέας αναλυτικής μετρικής με χρήση NumPy (Vectorized Operation)
# Βαθμολογία Προτίμησης Μέσων Μαζικής Μεταφοράς / Μικροκινητικότητας έναντι ΙΧ
bus_arr = df_merged['BusPassengers'].to_numpy()
bike_arr = df_merged['BikeTrips'].to_numpy()
traffic_arr = df_merged['TrafficCount'].to_numpy()

# Υπολογισμός: (Επιβάτες Λεωφορείων + Διαδρομές Ποδηλάτων) / (Όγκος Κυκλοφορίας + 1) * 100
df_merged['PT_Preference_Score'] = np.round((bus_arr + bike_arr) / (traffic_arr + 1) * 100, 2)

# 5. Αποθήκευση του τελικού ενιαίου αρχείου
df_merged.to_csv('merged_urban_data.csv', index=False)
print("Η συγχώνευση, ο καθαρισμός και ο υπολογισμός της μετρικής ολοκληρώθηκαν!")