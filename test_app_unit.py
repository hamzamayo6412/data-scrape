from flask import Flask
from unittest.mock import patch, MagicMock
import json
import pytest
import app

@pytest.fixture
def app_fixture():
    flask_app = Flask(__name__)
    flask_app.config['TESTING'] = True
    
    flask_app.route('/fetch-and-insert', methods=['GET'])(app.fetch_and_insert_route)
    flask_app.route('/')(app.index)
    
    return flask_app

@pytest.fixture
def client(app_fixture):
    return app_fixture.test_client()

@pytest.fixture
def mock_mongo():
    mock_collection = MagicMock()
    
    mock_collection.count_documents.return_value = 1
    
    mock_products = [{
        'title': 'Product X',
        'brand': 'Brand Y',
        'price': {'currency': 'USD', 'min': '99'},
        'meta': {'categories': ['Tech']},
        'images': {'main': 'http://image.com'},
        'links': {'main': 'http://link.com'}
    }]
    
    mock_collection.find.return_value.skip.return_value.limit.return_value = mock_products
    
    with patch.object(app, 'collection', mock_collection):
        yield mock_collection

def test_fetch_and_insert_data_success(client):
    from unittest.mock import patch
    import json

    mock_api_response = {
        "products": [
            {
                "id": "123",
                "docid": "doc123",
                "title": "Test Product",
                "brand": "Test Brand",
                "description": "This is a test product.",
                "price": {
                    "min": 10,
                    "max": 15,
                    "currency": "USD",
                    "original_min": 12,
                    "original_max": 18,
                    "savings": 2,
                    "unit": "unit"
                },
                "image_url": "http://example.com/image.jpg",
                "images": {"all": ["img1", "img2"]},
                "link": "http://example.com/product",
                "links": {"all": ["link1"]},
                "meta": {
                    "interests": [
                        {"type": "category", "name": "Tech"},
                        {"type": "interest", "name": "AI"}
                    ]
                },
                "origin": "web",
                "score": 0.8,
                "in_stock": True,
                "image_ts": "2023-01-01"
            }
        ]
    }

    with patch('app.requests.get') as mock_get:
        mock_get.return_value.content = json.dumps(mock_api_response).encode()
        response = client.get('/fetch-and-insert')
        assert response.status_code == 200
        assert b'Data fetched and inserted successfully' in response.data

def test_index_route(client, mock_mongo):
    mock_mongo.find.return_value.skip.return_value.limit.return_value = [{
        'title': 'Product X',
        'brand': 'Brand Y',
        'price': {'currency': 'USD', 'min': '99'},
        'meta': {'categories': ['Tech']},
        'images': {'main': 'http://image.com'},
        'links': {'main': 'http://link.com'}
    }]
    
    response = client.get('/')
    
    assert response.status_code == 200
    
    assert b'Product' in response.data
    assert b'Brand' in response.data
    assert b'http://image.com' in response.data
    assert b'http://link.com' in response.data

def test_external_api_call_real():
    import requests
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

    response = requests.get(url, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
