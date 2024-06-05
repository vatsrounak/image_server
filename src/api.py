from flask import Flask, jsonify
from database import session , MenuItem

app = Flask(__name__)

@app.route('/menu_items', methods=['GET'])  
def get_menu_items():
    menu_items = session.query(MenuItem).all()
    return jsonify([{'name': item.name, 'price': item.price} for item in menu_items])

if __name__ == '__main__':
    app.run(debug=True)