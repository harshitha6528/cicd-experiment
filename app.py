import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Fallback to local SQLite database if DATABASE_URL is not set
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define an Item table model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Auto-create tables when app starts
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "App and Database connected successfully!"})

@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'POST':
        data = request.get_json() or {}
        item_name = data.get('name', 'Sample Item')
        new_item = Item(name=item_name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item added!", "id": new_item.id, "name": new_item.name}), 201

    items = Item.query.all()
    return jsonify([{"id": item.id, "name": item.name} for item in items])

if __name__ == '__main__':
    app.run()