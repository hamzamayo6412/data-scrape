# Data Scraper Flask App

This app shows product data from an online store. It stores the data in MongoDB and displays it on a webpage.

## What the App Does

- Gets product data from an API
- Saves the data to a MongoDB database
- Shows the products on a webpage
- Lets you browse through pages of products

## How to Use

1. Start the app:
```bash
python app.py
```

2. Open your browser and go to:
```
http://localhost:5000
```

3. To get new product data, visit:
```
http://localhost:5000/fetch-and-insert
```

## Features

- Shows 10 products per page
- Displays product title, brand, price, and image
- Links to the original product page
- Shows product categories
- Easy page navigation

## Requirements

- Python 3
- Flask
- pymongo
- requests
- pandas

## Setup

1. Install Python packages:
```bash
pip install flask pymongo requests pandas
```

2. Make sure MongoDB is running
3. Start the app with `python app.py`

## References
1. https://www.youtube.com/watch?v=m7UQyy0Q5Uk&list=PLu0W_9lII9agAiWp6Y41ueUKx1VcTRxmf&index=2
2. https://www.youtube.com/watch?v=jNiSALNBQv0&list=PLu0W_9lII9agAiWp6Y41ueUKx1VcTRxmf&index=3
3. https://www.youtube.com/watch?v=zU2l4HKT0nc
4. https://www.youtube.com/watch?v=JqS6BcgeUMw&list=PLu0W_9lII9agAiWp6Y41ueUKx1VcTRxmf&index=19
5. https://medium.com/featurepreneur/mongodb-crud-with-flask-e5700ad7996e
6. https://medium.com/@hello_9187/unit-testing-a-flask-api-910b19c38ee2#:~:text=The%20first%20step%20is%20to,others%20to%20the%20function%20level.