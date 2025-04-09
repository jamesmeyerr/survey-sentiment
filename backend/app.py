from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from services.analyzer import SentimentAnalyzer, CategoryExtractor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
sentiment_analyzer = SentimentAnalyzer()
category_extractor = CategoryExtractor()

# Load sample data
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'surveys.json')

def load_data():
    """Load survey data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save survey data to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Routes
@app.route('/api/surveys', methods=['GET'])
def get_surveys():
    """Get all surveys with sentiment analysis"""
    surveys = load_data()
    
    # Add sentiment analysis if not already present
    for survey in surveys:
        if 'sentiment_score' not in survey:
            survey['sentiment_score'] = sentiment_analyzer.analyze(survey['comment'])
        
        if 'categories' not in survey:
            survey['categories'] = category_extractor.extract_categories(survey['comment'])
    
    save_data(surveys)
    return jsonify(surveys)

@app.route('/api/surveys', methods=['POST'])
def add_survey():
    """Add a new survey"""
    data = request.json
    surveys = load_data()
    
    # Generate new ID
    new_id = max([s['id'] for s in surveys], default=0) + 1
    
    new_survey = {
        'id': new_id,
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'overall_rating': data['overall_rating'],
        'comment': data['comment'],
        'member_id': data.get('member_id', f'M{1000 + new_id}'),
        'sentiment_score': sentiment_analyzer.analyze(data['comment']),
        'categories': category_extractor.extract_categories(data['comment'])
    }
    
    surveys.append(new_survey)
    save_data(surveys)
    
    return jsonify(new_survey), 201

@app.route('/api/surveys/<int:survey_id>', methods=['GET'])
def get_survey(survey_id):
    """Get a specific survey by ID"""
    surveys = load_data()
    survey = next((s for s in surveys if s['id'] == survey_id), None)
    
    if survey:
        return jsonify(survey)
    return jsonify({'error': 'Survey not found'}), 404

@app.route('/api/analytics/sentiment-over-time', methods=['GET'])
def sentiment_over_time():
    """Get sentiment trends over time"""
    surveys = load_data()
    
    # Ensure all surveys have sentiment scores
    for survey in surveys:
        if 'sentiment_score' not in survey:
            survey['sentiment_score'] = sentiment_analyzer.analyze(survey['comment'])
    
    # Group by date
    result = {}
    for survey in surveys:
        date = survey['date']
        if date not in result:
            result[date] = {
                'date': date,
                'avg_sentiment': 0,
                'avg_rating': 0,
                'count': 0
            }
        
        result[date]['avg_sentiment'] += survey['sentiment_score']
        result[date]['avg_rating'] += survey['overall_rating']
        result[date]['count'] += 1
    
    # Calculate averages
    for date in result:
        result[date]['avg_sentiment'] /= result[date]['count']
        result[date]['avg_rating'] /= result[date]['count']
    
    return jsonify(list(result.values()))

@app.route('/api/analytics/category-sentiment', methods=['GET'])
def category_sentiment():
    """Get sentiment breakdown by category"""
    surveys = load_data()
    
    # Ensure all surveys have categories and sentiment scores
    for survey in surveys:
        if 'sentiment_score' not in survey:
            survey['sentiment_score'] = sentiment_analyzer.analyze(survey['comment'])
        if 'categories' not in survey:
            survey['categories'] = category_extractor.extract_categories(survey['comment'])
    
    # Extract category-specific sentiment
    categories = {}
    for survey in surveys:
        for category, text in survey['categories'].items():
            if category not in categories:
                categories[category] = {
                    'category': category,
                    'avg_sentiment': 0,
                    'count': 0,
                    'example_comments': []
                }
            
            # Calculate sentiment for this category text specifically
            category_sentiment = sentiment_analyzer.analyze(text)
            categories[category]['avg_sentiment'] += category_sentiment
            categories[category]['count'] += 1
            
            # Store a few example comments
            if len(categories[category]['example_comments']) < 3:
                categories[category]['example_comments'].append({
                    'text': text,
                    'sentiment': category_sentiment
                })
    
    # Calculate averages
    for category in categories:
        categories[category]['avg_sentiment'] /= categories[category]['count']
    
    return jsonify(list(categories.values()))

# Initialize with sample data
if __name__ == '__main__':
    # Check if data file exists, if not, create it with sample data
    if not os.path.exists(DATA_FILE):
        sample_data_path = os.path.join(os.path.dirname(__file__), '..', 'dummy-survey-data.json')
        if os.path.exists(sample_data_path):
            with open(sample_data_path, 'r') as f:
                sample_data = json.load(f)
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, 'w') as f:
                json.dump(sample_data, f, indent=2)
        else:
            print("Warning: Sample data file not found.")
    
    app.run(debug=True, port=5000)