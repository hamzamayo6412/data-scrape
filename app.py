from flask import Flask, render_template, request
from pymongo import MongoClient
import requests
import json
import pandas as pd
import datetime

app = Flask(__name__)

client = MongoClient("mongodb+srv://hamzamayo6412:pXe8HIv6Lx5QhoqI@cluster0.bc8avdt.mongodb.net/", tls=True, tlsAllowInvalidCertificates=True)
db = client['Ecom_store']
collection = db['products']
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
    products = j['products']
    
    # Prepare the data for MongoDB
    prepared_products = []
    for product in products:
        # Extract categories and interests
        categories = []
        interests = []
        for interest in product.get('meta', {}).get('interests', []):
            if interest['type'] == 'category':
                categories.append(interest['name'])
            else:
                interests.append(interest['name'])
        
        prepared_product = {
            'product_id': product.get('id', ''),
            'docid': product.get('docid', ''),
            'title': product.get('title', ''),
            'brand': product.get('brand', ''),
            'description': product.get('description', ''),
            'price': {
                'min': product.get('price', {}).get('min', ''),
                'max': product.get('price', {}).get('max', ''),
                'currency': product.get('price', {}).get('currency', ''),
                'original_min': product.get('price', {}).get('original_min', ''),
                'original_max': product.get('price', {}).get('original_max', ''),
                'savings': product.get('price', {}).get('savings', 0),
                'unit': product.get('price', {}).get('unit', '')
            },
            'images': {
                'main': product.get('image_url', ''),
                'all': product.get('images', {})
            },
            'links': {
                'main': product.get('link', ''),
                'all': product.get('links', {})
            },
            'meta': {
                'categories': categories,
                'interests': interests,
                'origin': product.get('origin', ''),
                'score': product.get('score', 0)
            },
            'in_stock': product.get('in_stock', False),
            'image_ts': product.get('image_ts', ''),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        prepared_products.append(prepared_product)

    if prepared_products:
        collection.insert_many(prepared_products)
    
    return j

# Define the route
@app.route('/fetch-and-insert', methods=['GET'])
def fetch_and_insert_route():
    try:
        api_response = fetch_and_insert_data()
        return ({'message': 'Data fetched and inserted successfully', 'api_response': api_response}), 200
    except Exception as e:
        return ({'error': str(e)}), 500

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    per_page = 10

    skip = (page - 1) * per_page

    total_products = collection.count_documents({})

    products = list(collection.find().skip(skip).limit(per_page))

    display_data = []
    for product in products:
        display_data.append({
            'Title': product.get('title', ''),
            'Brand': product.get('brand', ''),
            'Price': f"{product.get('price', {}).get('currency', '')} {product.get('price', {}).get('min', '')}",
            'Categories': ', '.join(product.get('meta', {}).get('categories', [])),
            'Image': f"<img src='{product.get('images', {}).get('main', '')}' width='100' />",
            'Link': f"<a href='{product.get('links', {}).get('main', '')}' target='_blank'>View Product</a>"
        })

    df = pd.DataFrame(display_data)
    html_table = df.to_html(classes='data', header=True, escape=False, index=False)
    html_table = html_table.replace('\n', '').strip()

    total_pages = (total_products + per_page - 1) // per_page
    
    return render_template(
        'index.html',
        tables=html_table,
        titles=['Products'],
        current_page=page,
        total_pages=total_pages,
        total_products=total_products
    )

if __name__ == '__main__':
    app.run(debug=True)
