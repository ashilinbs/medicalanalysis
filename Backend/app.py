import os
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
import zipfile
import time  

matplotlib.use('Agg') 

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://ashilinbs22cse:Ashmi@cluster0.xxxj1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['blood_donation_db']
collection = db['blood_donation']

GRAPH_FOLDER = "graphs"  
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# Add the configuration to serve static files
app.config['UPLOAD_FOLDER'] = 'graphs'
app.add_url_rule('/static/graphs/<filename>', 'static_graphs', 
                 lambda filename: send_from_directory(app.config['UPLOAD_FOLDER'], filename), methods=['GET'])

@app.route('/add-donation', methods=['POST'])
def add_donation():
    data = request.json
    state = data.get("State/UT")

    existing_record = collection.find_one({"State/UT": state})
    if existing_record:
        collection.update_one({"State/UT": state}, {"$set": data})
        return jsonify({"message": "Data updated successfully"}), 200
    else:
        collection.insert_one(data)
        return jsonify({"message": "Data added successfully"}), 201

@app.route('/get-all-blood-donation-graphs', methods=['GET'])
def get_all_blood_donation_graphs():
    data = list(collection.find({}, {"_id": 0, "State/UT": 1, "Total Blood Donations": 1}))

    if not data:
        return jsonify({"message": "No data available"}), 404

    df = pd.DataFrame(data)
    graph_urls = []

    bar_chart_path = os.path.join(GRAPH_FOLDER, "bar_chart.png")
    plt.figure(figsize=(12, 6))
    plt.bar(df['State/UT'], df['Total Blood Donations'], color='blue')
    plt.xticks(rotation=90)
    plt.xlabel('State/UT')
    plt.ylabel('Total Blood Donations')
    plt.title('Blood Donations by State/UT (Bar Chart)')
    plt.tight_layout()
    plt.savefig(bar_chart_path)
    plt.close()
    graph_urls.append(f"http://localhost:5000/static/graphs/bar_chart.png?{int(time.time())}")  # Append timestamp for cache busting

    line_chart_path = os.path.join(GRAPH_FOLDER, "line_chart.png")
    plt.figure(figsize=(12, 6))
    plt.plot(df['State/UT'], df['Total Blood Donations'], marker='o', color='green')
    plt.xticks(rotation=90)
    plt.xlabel('State/UT')
    plt.ylabel('Total Blood Donations')
    plt.title('Blood Donations by State/UT (Line Chart)')
    plt.tight_layout()
    plt.savefig(line_chart_path)
    plt.close()
    graph_urls.append(f"http://localhost:5000/static/graphs/line_chart.png?{int(time.time())}")  # Append timestamp for cache busting

   
    histogram_path = os.path.join(GRAPH_FOLDER, "histogram.png")
    plt.figure(figsize=(12, 6))
    plt.hist(df['Total Blood Donations'], bins=10, color='purple', edgecolor='black')
    plt.xlabel('Total Blood Donations')
    plt.ylabel('Frequency')
    plt.title('Blood Donations Frequency Distribution (Histogram)')
    plt.tight_layout()
    plt.savefig(histogram_path)
    plt.close()
    graph_urls.append(f"http://localhost:5000/static/graphs/histogram.png?{int(time.time())}")  # Append timestamp for cache busting

   
    circular_chart_path = os.path.join(GRAPH_FOLDER, "circular_chart.png")
    plt.figure(figsize=(8, 8))
    
    
    angles = [n / float(len(df)) * 2 * 3.1416 for n in range(len(df))]
    radii = df['Total Blood Donations']
    plt.subplot(111, polar=True)
    plt.bar(angles, radii, width=0.3, color='orange', edgecolor='black')

    plt.title('Blood Donations by State/UT (Circular Visualization)', fontsize=16)
    plt.tight_layout()
    plt.savefig(circular_chart_path)
    plt.close()
    graph_urls.append(f"http://localhost:5000/static/graphs/circular_chart.png?{int(time.time())}")  # Append timestamp for cache busting

    return jsonify({"graphs": graph_urls}), 200

@app.route('/download-graphs', methods=['GET'])
def download_graphs():
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename in os.listdir(GRAPH_FOLDER):
            file_path = os.path.join(GRAPH_FOLDER, filename)
            zip_file.write(file_path, arcname=filename)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='graphs.zip')

if __name__ == '__main__':
    app.run(debug=True)
