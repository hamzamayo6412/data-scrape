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
    mock_mongo.insert_one({
        'title': 'Product X',
        'brand': 'Brand Y',
        'price': {'currency': 'USD', 'min': '99'},
        'meta': {'categories': ['Tech']},
        'images': {'main': 'http://image.com'},
        'links': {'main': 'http://link.com'}
    })

    response = client.get('/')
    assert response.status_code == 200
    assert b'Product X' in response.data
    assert b'Brand Y' in response.data
    assert b'USD 99' in response.data
def test_external_api_call_real():
    import requests
    url = 'https://aix.salesfire.co.uk/api/v2/recommend?aid=e62ed6db-c28d-4934-a573-60cf200aa837&l=12&w=null&filters%5Bfilter_out_of_stock%5D=true&context=product&uid=0d403cc4-7f17-42f1-9b76-3ee38a4c355f&q=Technology&s%5B0%5D=c&shuffle=0'
    
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    print(f"✅ Real API test passed. Fetched {len(data['products'])} products.")
