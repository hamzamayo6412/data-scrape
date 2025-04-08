from flask import Flask, render_template
from pymongo import MongoClient
import requests
import json
import pandas as pd

app = Flask(__name__)

# Created Mongodb on mongo atlas and connnected in my app
client = MongoClient("mongodb+srv://hamzamayo6412:pXe8HIv6Lx5QhoqI@cluster0.bc8avdt.mongodb.net/", tls=True, tlsAllowInvalidCertificates=True)
db = client['Econ_store']  # Your database name
collection = db['products']  # Your collection name
# Step 1: Fetch and Insert Data from API to MongoDB (for the first time)
def fetch_and_insert_data():
    url = 'https://aix.salesfire.co.uk/api/v2/recommend?aid=e62ed6db-c28d-4934-a573-60cf200aa837&l=12&w=null&filters%5Bfilter_out_of_stock%5D=true&context=product&uid=0d403cc4-7f17-42f1-9b76-3ee38a4c355f&q=Technology&s%5B0%5D=c&shuffle=0'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://cdn.salesfire.co.uk',
        'referer': 'https://cdn.salesfire.co.uk/',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }

    resp = requests.get(url, headers=headers)
    j = json.loads(resp.content)
    res = j['products']
    
    # Insert the data into MongoDB
    collection.insert_many(res)

# Define the route
@app.route('/fetch-and-insert', methods=['GET'])
def fetch_and_insert_route():
    try:
        fetch_and_insert_data()
        return ({'message': 'Data fetched and inserted successfully'}), 200
    except Exception as e:
        return ({'error': str(e)}), 500

@app.route('/')
def index():
    products = collection.find()

    df_from_mongo = pd.DataFrame(list(products))

    return render_template('index.html', tables=[df_from_mongo.to_html(classes='data', header=True)], titles=['na', 'Products'])

if __name__ == '__main__':
    app.run(debug=True)
