import re
import os
import nltk
from models.sentiment import VaderSentimentModel, TransformerSentimentModel

# Create directories if they don't exist
os.makedirs(os.path.dirname(__file__), exist_ok=True)

class SentimentAnalyzer:
    """Service that analyzes the sentiment of survey comments"""
    
    def __init__(self, use_transformer=False):
        """Initialize with the specified model type"""
        # For the prototype, we'll use the simpler VADER model by default
        # Later we can switch to the more sophisticated transformer model
        if use_transformer:
            self.model = TransformerSentimentModel()
        else:
            self.model = VaderSentimentModel()
    
    def analyze(self, text):
        """
        Analyze the sentiment of the given text
        Returns a score between 0 (negative) and 1 (positive)
        """
        return self.model.predict(text)
    
    def analyze_categories(self, categories):
        """
        Analyze sentiment for specific categories extracted from text
        Returns a dictionary of category -> sentiment score
        """
        result = {}
        for category, text in categories.items():
            result[category] = self.analyze(text)
        return result


class CategoryExtractor:
    """Service that extracts categories from survey comments"""
    
    def __init__(self):
        """Initialize with necessary NLTK components"""
        # Download necessary NLTK data
        try:
            nltk.data.find('punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Define common categories and their related keywords
        self.categories = {
            "food": ["food", "meal", "menu", "eat", "dining", "breakfast", "lunch", "dinner", 
                    "snack", "cuisine", "dish", "taste", "flavor", "delicious", "catering",
                    "restaurant", "cafe", "buffet", "cold", "hot", "drinks", "beverage"],
            
            "service": ["service", "staff", "waiter", "waitress", "attendant", "employee",
                       "customer service", "help", "assistance", "attentive", "friendly",
                       "professional", "responsive", "helpful", "attitude", "server"],
            
            "facilities": ["facility", "facilities", "bathroom", "toilet", "restroom", "venue",
                          "location", "building", "infrastructure", "clean", "maintenance",
                          "seating", "seat", "chair", "table", "area", "space", "room", 
                          "parking", "entrance", "exit", "accessibility"],
            
            "racing": ["race", "racing", "horse", "jockey", "bet", "betting", "track",
                      "viewing", "view", "binoculars", "odds", "winner", "finish",
                      "program", "card", "race card", "thoroughbred", "competition"],
            
            "value": ["price", "cost", "expensive", "cheap", "affordable", "value",
                     "money", "worth", "overpriced", "reasonable", "budget", "payment",
                     "fee", "admission", "ticket", "spend", "dollar", "pound", "cash"],
            
            "atmosphere": ["atmosphere", "crowd", "ambiance", "environment", "mood",
                         "vibe", "energy", "exciting", "boring", "fun", "enjoyable",
                         "lively", "quiet", "noisy", "pleasant", "experience", "feel"],
        }
    
    def extract_categories(self, text):
        """
        Extract text segments related to specific categories
        Returns a dictionary of category -> relevant text portions
        """
        if not text:
            return {}
        
        # Convert to lowercase for easier matching
        text_lower = text.lower()
        
        # Split into sentences for better context
        sentences = nltk.sent_tokenize(text)
        
        result = {}
        
        # Check each category
        for category, keywords in self.categories.items():
            # Find sentences containing keywords for this category
            category_sentences = []
            for sentence in sentences:
                sentence_lower = sentence.lower()
                # If any keyword appears in the sentence
                if any(re.search(r'\b' + re.escape(kw) + r'\b', sentence_lower) for kw in keywords):
                    category_sentences.append(sentence)
            
            # If we found relevant sentences, join them and store
            if category_sentences:
                result[category] = " ".join(category_sentences)
        
        return result