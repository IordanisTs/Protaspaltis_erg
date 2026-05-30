import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ρύθμιση για σωστή εμφάνιση ελληνικών χαρακτήρων στα γραφήματα
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Φόρτωση των συγχωνευμένων δεδομένων
df = pd.read_csv('merged_urban_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Ορισμός κοινού αισθητικού θέματος
sns.set_theme(style="whitegrid")

# ==========================================
# ΓΡΑΦΗΜΑ 1: Ιστόγραμμα με καμπύλη πυκνότητας (KDE)
# ==========================================
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='TrafficCount', kde=True, color='#2b5c8f', bins=30)
plt.title('Κατανομή του Ημερήσιου Όγκου Κυκλοφορίας στην Κοζάνη (2025)', fontsize=14, pad=15)
plt.xlabel('Όγκος Κυκλοφορίας (Αριθμός Οχημάτων)', fontsize=12)
plt.ylabel('Συχνότητα (Ημέρες)', fontsize=12)
plt.tight_layout()
plt.savefig('1_traffic_distribution.png', dpi=300)
plt.close()

# ==========================================
# ΓΡΑΦΗΜΑ 2: Γράφημα Τάσης (Time-series)
# ==========================================
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='BikeTrips', color='#107d10', linewidth=1.5)
plt.title('Διακύμανση Χρήσης Κοινόχρηστων Ποδηλάτων κατά τη Διάρκεια του Έτους', fontsize=14, pad=15)
plt.xlabel('Ημερομηνία', fontsize=12)
plt.ylabel('Ημερήσιες Διαδρομές με Ποδήλατα', fontsize=12)
plt.tight_layout()
plt.savefig('2_bike_trips_trend.png', dpi=300)
plt.close()

# ==========================================
# ΓΡΑΦΗΜΑ 3: Συγκεντρωτικό Ραβδόγραμμα (Bar Chart)
# ==========================================
# Υπολογισμός της μέσης πληρότητας ανά είδος εκδήλωσης
df_grouped = df.groupby('EventType')['ParkingOccupancy'].mean().reset_index()
# Ταξινόμηση για καλύτερη οπτική ανάγνωση
df_grouped = df_grouped.sort_values(by='ParkingOccupancy', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_grouped, x='ParkingOccupancy', y='EventType', palette='Blues_r', hue='EventType', legend=False)
plt.title('Μέση Πληρότητα Χώρων Στάθμευσης ανά Είδος Εκδήλωσης', fontsize=14, pad=15)
plt.xlabel('Μέση Πληρότητα Χώρων Στάθμευσης (%)', fontsize=12)
plt.ylabel('Είδος Εκδήλωσης', fontsize=12)
plt.tight_layout()
plt.savefig('3_parking_by_event_type.png', dpi=300)
print("Τα 3 στατικά γραφήματα δημιουργήθηκαν και αποθηκεύτηκαν επιτυχώς!")