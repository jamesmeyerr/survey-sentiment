import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = {
  // Survey methods
  getAllSurveys: async () => {
    try {
      const response = await axios.get(`${API_URL}/surveys`);
      return response.data;
    } catch (error) {
      console.error('Error fetching surveys:', error);
      throw error;
    }
  },
  
  getSurveyById: async (id) => {
    try {
      const response = await axios.get(`${API_URL}/surveys/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching survey ${id}:`, error);
      throw error;
    }
  },
  
  addSurvey: async (surveyData) => {
    try {
      const response = await axios.post(`${API_URL}/surveys`, surveyData);
      return response.data;
    } catch (error) {
      console.error('Error adding survey:', error);
      throw error;
    }
  },
  
  // Analytics methods
  getSentimentOverTime: async () => {
    try {
      const response = await axios.get(`${API_URL}/analytics/sentiment-over-time`);
      return response.data;
    } catch (error) {
      console.error('Error fetching sentiment over time:', error);
      throw error;
    }
  },
  
  getCategorySentiment: async () => {
    try {
      const response = await axios.get(`${API_URL}/analytics/category-sentiment`);
      return response.data;
    } catch (error) {
      console.error('Error fetching category sentiment:', error);
      throw error;
    }
  }
};

export default api;