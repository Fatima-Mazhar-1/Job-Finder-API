import React, { useState } from 'react';

const initialFormData = {
  position: '',
  experience: '',
  salary: '',
  jobNature: '',
  location: '',
  skills: ''
};

const SearchForm = ({ onSearch, isLoading }) => {
  const [formData, setFormData] = useState(initialFormData);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(formData);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Find Your Dream Job</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label htmlFor="position" className="input-label">Job Title/Position*</label>
            <input
              type="text"
              id="position"
              name="position"
              placeholder="e.g., Frontend Engineer"
              className="input-field"
              value={formData.position}
              onChange={handleChange}
              required
            />
          </div>
          
          <div>
            <label htmlFor="experience" className="input-label">Experience*</label>
            <input
              type="text"
              id="experience"
              name="experience"
              placeholder="e.g., 2 years"
              className="input-field"
              value={formData.experience}
              onChange={handleChange}
              required
            />
          </div>
          
          <div>
            <label htmlFor="salary" className="input-label">Expected Salary</label>
            <input
              type="text"
              id="salary"
              name="salary"
              placeholder="e.g., 80,000 PKR to 150,000 PKR"
              className="input-field"
              value={formData.salary}
              onChange={handleChange}
            />
          </div>
          
          <div>
            <label htmlFor="jobNature" className="input-label">Job Nature</label>
            <select
              id="jobNature"
              name="jobNature"
              className="input-field"
              value={formData.jobNature}
              onChange={handleChange}
            >
              <option value="">Select Job Nature</option>
              <option value="remote">Remote</option>
              <option value="onsite">Onsite</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </div>
          
          <div>
            <label htmlFor="location" className="input-label">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              placeholder="e.g., Lahore, Pakistan"
              className="input-field"
              value={formData.location}
              onChange={handleChange}
            />
          </div>
          
          <div>
            <label htmlFor="skills" className="input-label">Skills*</label>
            <input
              type="text"
              id="skills"
              name="skills"
              placeholder="e.g., React, TypeScript, Node.js"
              className="input-field"
              value={formData.skills}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        
        <button 
          type="submit" 
          className="btn-primary w-full"
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Searching...
            </span>
          ) : (
            'Find Jobs'
          )}
        </button>
      </form>
    </div>
  );
};

export default SearchForm; 