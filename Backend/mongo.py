from pymongo import MongoClient
import pandas as pd

# Replace with your connection string from MongoDB Atlas
connection_string = "mongodb+srv://ashilinbs22cse:Ashmi@cluster0.xxxj1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 "
client = MongoClient(connection_string)

# Create or connect to a database and collection
db = client['blood_donation_db']  # Database name
collection = db['blood_donation']  # Collection name

# Load data from CSV
csv_file = 'blood_dona.csv'  # Replace with your CSV file path
data = pd.read_csv(csv_file)

# Convert data to dictionary format and insert into MongoDB
records = data.to_dict(orient='records')
collection.insert_many(records)
print("Data has been successfully inserted into MongoDB Atlas.")
