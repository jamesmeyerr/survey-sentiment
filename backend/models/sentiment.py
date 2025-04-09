import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Create model directory if it doesn't exist
os.makedirs(os.path.dirname(__file__), exist_ok=True)

class VaderSentimentModel:
    """Simple sentiment analysis model using NLTK's VADER"""
    
    def __init__(self):
        # Download necessary NLTK data (only runs once)
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        self.analyzer = SentimentIntensityAnalyzer()
    
    def predict(self, text):
        """
        Analyze sentiment of text
        Returns a score between 0 (negative) and 1 (positive)
        """
        if not text:
            return 0.5  # Neutral for empty text
        
        scores = self.analyzer.polarity_scores(text)
        
        # Convert from VADER's -1 to 1 scale to 0 to 1 scale
        normalized_score = (scores['compound'] + 1) / 2
        
        return normalized_score


class TransformerSentimentModel:
    """More sophisticated sentiment analysis using pre-trained transformers"""
    
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the model with a pre-trained transformer
        Only loads these libraries if this model is actually used
        """
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.softmax = torch.nn.Softmax(dim=1)
            self.ready = True
        except Exception as e:
            print(f"Error loading transformer model: {e}")
            print("Falling back to VADER")
            self.ready = False
            self.fallback = VaderSentimentModel()
    
    def predict(self, text):
        """
        Analyze sentiment using the transformer model
        Returns a score between 0 (negative) and 1 (positive)
        """
        if not self.ready:
            return self.fallback.predict(text)
        
        if not text:
            return 0.5  # Neutral for empty text
        
        try:
            import torch
            
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probabilities = self.softmax(outputs.logits)
            # Most models output [negative, positive] probabilities
            # So we can just take the second value as the positive score
            positive_score = probabilities[0][1].item()
            
            return positive_score
        except Exception as e:
            print(f"Error in transformer inference: {e}")
            # Fall back to VADER if something goes wrong
            return self.fallback.predict(text)