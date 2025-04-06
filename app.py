from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Created Mongodb on mongo atlas and connnected in my app
client = MongoClient("mongodb+srv://hamzamayo6412:pXe8HIv6Lx5QhoqI@cluster0.bc8avdt.mongodb.net/", tls=True, tlsAllowInvalidCertificates=True)
db = client['Econ_store']  # Your database name
collection = db['products']  # Your collection name

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
