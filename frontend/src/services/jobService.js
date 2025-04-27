import axios from 'axios';

const API_URL = '/api';

export const searchJobs = async (searchCriteria) => {
  try {
    const response = await axios.post(`${API_URL}/jobs/search`, searchCriteria);
    return response.data;
  } catch (error) {
    console.error('Error searching jobs:', error);
    throw error;
  }
}; 