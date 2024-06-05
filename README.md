## Project Documentation: Image Server for Restaurant Menus

### Overview
This project involves building an image server to scrape menu images from restaurants in Mumbai, perform OCR (Optical Character Recognition) on these images to extract menu items and their prices, and store the extracted data in a database. A Flask-based API is provided to access the stored data.

### Assumptions
1. **Restaurant Websites**: The websites of the restaurants in Mumbai will have menu images embedded in HTML with identifiable `img` tags containing URLs to the images.
   - **Reason**: This is a common practice on many restaurant websites, making it feasible to locate and download images using web scraping techniques.

2. **Image Format**: The menu images will be in a standard format (e.g., JPEG, PNG) and accessible without login or additional authentication.
   - **Reason**: Simplifies the scraping process and avoids complexities related to image formats and authentication.

3. **OCR Compatibility**: The text on the menu images will be in a clear, readable font and in English, making it suitable for OCR processing using Tesseract.
   - **Reason**: Ensures reliable text extraction as Tesseract works best with clear, printed text.

4. **Database Choice**: SQLite is used for simplicity and ease of setup. This can be easily replaced with a more robust database like MySQL or PostgreSQL if needed.
   - **Reason**: Simplifies the initial development and testing phase. SQLite is lightweight and does not require a separate server setup.

5. **Flask for API**: Flask is chosen to create a RESTful API for accessing the stored data.
   - **Reason**: Flask is lightweight, easy to use, and well-suited for small to medium-sized projects.

### Project Structure

If test cases are included and once the server starts up the project structure should look like this.

```plaintext
image-server-project/
├── data/
│   ├── images/                # Directory to store downloaded images
│   └── processed/             # Directory to store preprocessed images (optional)
├── src/
│   ├── __init__.py
│   ├── scraper.py             # Script for web scraping
│   ├── ocr_processor.py       # Script for OCR processing
│   ├── database.py            # Script for database interactions
│   ├── api.py                 # Flask application script
│   └── config.py              # Configuration settings (e.g., database URI)
├── tests/
│   ├── test_scraper.py        # Tests for web scraping
│   ├── test_ocr_processor.py  # Tests for OCR processing
│   ├── test_database.py       # Tests for database interactions
│   └── test_api.py            # Tests for API endpoints
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

### Virtual environment
Create a virtual environment: 
```bash
python3 -m venv venv
```


### Requirements
Install the required Python libraries using the following command:
```bash
pip install -r requirements.txt
```

### src/scraper.py
Handles downloading menu images from restaurant websites.
```python
import os
import requests
from bs4 import BeautifulSoup

def fetch_image_urls(restaurant_url):
    response = requests.get(restaurant_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = [img['src'] for img in soup.find_all('img') if 'menu' in img['src']]
    return image_urls

def download_images(image_urls, save_dir='data/images'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for url in image_urls:
        image_name = url.split('/')[-1]
        img_data = requests.get(url).content
        with open(os.path.join(save_dir, image_name), 'wb') as handler:
            handler.write(img_data)
```

### src/ocr_processor.py
Handles preprocessing images and extracting text using OCR.
```python
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re

def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    return image

def ocr_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image)
    return text

def parse_text(text):
    items_prices = re.findall(r'(\w+.*?)\s+(\d+)', text)
    return items_prices
```

### src/database.py
Handles database interactions such as storing and retrieving menu items and prices.
```python
from sqlalchemy import create_engine, Column, Integer, String, Float, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'sqlite:///data/menu_items.db'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_all_menu_items():
    return session.query(MenuItem).all()

def store_items(items_prices):
    for item, price in items_prices:
        menu_item = MenuItem(name=item, price=price)
        session.add(menu_item)
    session.commit()
```

### src/api.py
Provides API endpoints to access the stored data.
```python
from flask import Flask, jsonify
from database import get_all_menu_items

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Menu Items API!"

@app.route('/menu_items', methods=['GET'])
def get_menu_items():
    items = get_all_menu_items()
    return jsonify([{'name': item.name, 'price': item.price} for item in items])

if __name__ == '__main__':
    app.run(debug=True)
```

### src/config.py
Configuration settings for the project.
```python
DATABASE_URI = 'sqlite:///data/menu_items.db'
TESSERACT_CMD = '/usr/bin/tesseract'  # Path to the Tesseract executable
```


### Running the Project
1. **Scrape Images**:
   - Run `scraper.py` to fetch and download menu images.
   - Images are saved in `data/images/`.

2. **Process Images with OCR**:
   - Run `ocr_processor.py` to preprocess images, perform OCR, and parse text.
   - Extracted items and prices are stored in the database.

3. **Store Data in Database**:
   - Ensure `database.py` is correctly configured to store parsed items and prices in the database.

4. **Build and Run API**:
   - Run `api.py` to start the API server.
   - Access stored menu items and prices via API endpoints.

### Testing the Project
- The project can be tested on several sample data and unit tests can be written for the project
- Insert sample data into the database for testing.
- Run the tests in the `tests/` directory to ensure everything is working as expected.

### Deployment
- Deploy the API and other components on a server.
- Ensure the database is accessible and configured correctly on the server.

By following this documentation, you will be able to set up, develop, and deploy this project efficiently.