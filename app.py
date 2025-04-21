from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import os
from sqlalchemy import or_

app = Flask(__name__)
# Update database configuration for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u56ee1q8tsvtot:paa1bc57419b22a4a7c2ea5dce8764cb92f860f3d58722601f2c998ec363714d1@cf980tnnkgv1bp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddffi5bp87g491'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stars = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    is_open = db.Column(db.Integer)
    attributes = db.Column(db.Text)  # Store as JSON string
    categories = db.Column(db.Text)  # Store as JSON string
    hours = db.Column(db.Text)  # Store as JSON string

    def __repr__(self):
        return f'<Business {self.name}>'

    def to_dict(self):
        return {
            'business_id': self.business_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'stars': self.stars,
            'review_count': self.review_count,
            'is_open': self.is_open,
            'attributes': json.loads(self.attributes) if self.attributes else None,
            'categories': json.loads(self.categories) if self.categories else None,
            'hours': json.loads(self.hours) if self.hours else None
        }

@app.route('/api/search', methods=['POST'])
def search_businesses():
    try:
        search_data = request.get_json()
        
        if not search_data or 'state' not in search_data:
            return jsonify({'error': 'State is required in the request body'}), 400
            
        state = search_data['state'].upper()
        categories = search_data.get('categories', []) 
        
        # Convert to list of lowercase categories and remove any whitespace
        processed_categories = []
        if categories:
            for category in categories:
                processed_category = category.strip().lower()
                processed_categories.append(processed_category)
        
        # Start with base query
        query = Business.query.filter(Business.state == state)
        
        # If categories are provided, add category filter
        if processed_categories:
            # Create a list of conditions for each category
            category_conditions = []
            for category in processed_categories:
                category_conditions.append(Business.categories.ilike(f'%{category}%'))
            
            # Combine conditions with OR
            query = query.filter(or_(*category_conditions))
        
        # Execute query and convert results to dictionaries
        results = [business.to_dict() for business in query.all()]
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)








