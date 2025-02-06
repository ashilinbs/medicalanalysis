import matplotlib.pyplot as plt
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://ashilinbs22cse:Ashmi@cluster0.xxxj1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 ")
db = client['blood_donation_db']
collection = db['blood_donation']

# Fetch data from MongoDB
data = list(collection.find({}, {'_id': 0}))

# Extract State/UT and Total Blood Donations
states = [record['State/UT'] for record in data]
donations = [record['Total Blood Donations'] for record in data]

# Create a bar graph
plt.figure(figsize=(12, 6))
plt.bar(states, donations, color='purple')
plt.xticks(rotation=90)
plt.xlabel('State/UT')
plt.ylabel('Total Blood Donations')
plt.title('Total Blood Donations by State/UT')
plt.tight_layout()
plt.show()
