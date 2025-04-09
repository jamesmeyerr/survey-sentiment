import { format } from 'date-fns';

// Convert sentiment score (0-1) to text representation
export const getSentimentText = (score) => {
  if (score >= 0.8) return 'Very Positive';
  if (score >= 0.6) return 'Positive';
  if (score >= 0.4) return 'Neutral';
  if (score >= 0.2) return 'Negative';
  return 'Very Negative';
};

// Get CSS class for sentiment score
export const getSentimentClass = (score) => {
  if (score >= 0.8) return 'sentiment-very-positive';
  if (score >= 0.6) return 'sentiment-positive';
  if (score >= 0.4) return 'sentiment-neutral';
  if (score >= 0.2) return 'sentiment-negative';
  return 'sentiment-very-negative';
};

// Get color for sentiment score (for charts)
export const getSentimentColor = (score) => {
  if (score >= 0.8) return '#2e7d32'; // Dark green
  if (score >= 0.6) return '#4caf50'; // Green
  if (score >= 0.4) return '#ff9800'; // Orange
  if (score >= 0.2) return '#f44336'; // Red
  return '#b71c1c'; // Dark red
};

// Compare rating vs sentiment and get text
export const compareRatingAndSentiment = (rating, sentiment) => {
  // Convert both to same scale (0-1)
  const normalizedRating = rating / 10;
  
  const difference = normalizedRating - sentiment;
  
  if (Math.abs(difference) < 0.15) {
    return {
      text: 'Rating matches sentiment',
      class: ''
    };
  } else if (difference > 0) {
    return {
      text: `Rating higher than sentiment by ${Math.round(difference * 10)} points`,
      class: 'rating-higher'
    };
  } else {
    return {
      text: `Sentiment higher than rating by ${Math.round(Math.abs(difference) * 10)} points`,
      class: 'sentiment-higher'
    };
  }
};

// Format date to display format
export const formatDate = (dateString) => {
  try {
    return format(new Date(dateString), 'MMM d, yyyy');
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString;
  }
};

// Category definitions with colors and icons
export const categories = {
  food: {
    label: 'Food & Beverages',
    color: '#FF6B6B',
    icon: 'restaurant'
  },
  service: {
    label: 'Staff & Service',
    color: '#4ECDC4',
    icon: 'people'
  },
  facilities: {
    label: 'Facilities & Venue',
    color: '#FFD166',
    icon: 'location_city'
  },
  racing: {
    label: 'Racing Experience',
    color: '#6A0572',
    icon: 'sports_score'
  },
  value: {
    label: 'Value for Money',
    color: '#1A936F',
    icon: 'attach_money'
  },
  atmosphere: {
    label: 'Atmosphere & Ambiance',
    color: '#3D5A80',
    icon: 'emoji_emotions'
  }
};

// Calculate average score from array of objects
export const calculateAverage = (array, key) => {
  if (!array || array.length === 0) return 0;
  const sum = array.reduce((acc, item) => acc + (item[key] || 0), 0);
  return sum / array.length;
};