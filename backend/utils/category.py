"""
Utility functions for categorization of text
"""

def get_category_colors():
    """
    Returns a consistent color mapping for categories
    Used for visualization consistency
    """
    return {
        "food": "#FF6B6B",         # Red
        "service": "#4ECDC4",      # Teal
        "facilities": "#FFD166",   # Yellow
        "racing": "#6A0572",       # Purple
        "value": "#1A936F",        # Green
        "atmosphere": "#3D5A80",   # Blue
    }

def get_category_icons():
    """
    Returns icon names for each category (for use with material-ui icons)
    """
    return {
        "food": "restaurant",
        "service": "people",
        "facilities": "location_city",
        "racing": "sports_score",
        "value": "attach_money",
        "atmosphere": "emoji_emotions",
    }

def get_category_display_names():
    """
    Returns user-friendly display names for categories
    """
    return {
        "food": "Food & Beverages",
        "service": "Staff & Service",
        "facilities": "Facilities & Venue",
        "racing": "Racing Experience",
        "value": "Value for Money",
        "atmosphere": "Atmosphere & Ambiance",
    }

def sentiment_to_text(score):
    """
    Converts a sentiment score (0-1) to descriptive text
    """
    if score >= 0.8:
        return "Very Positive"
    elif score >= 0.6:
        return "Positive"
    elif score >= 0.4:
        return "Neutral"
    elif score >= 0.2:
        return "Negative"
    else:
        return "Very Negative"