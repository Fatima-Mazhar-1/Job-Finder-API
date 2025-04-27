import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Header from './components/Header';
import SearchForm from './components/SearchForm';
import JobResults from './components/JobResults';
import Footer from './components/Footer';
import { searchJobs } from './services/jobService';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState(null);

  const handleSearch = async (searchCriteria) => {
    setIsLoading(true);
    setSearchResults(null);
    
    try {
      const results = await searchJobs(searchCriteria);
      setSearchResults(results);
      
      if (results.relevant_jobs.length === 0) {
        toast.info('No jobs found matching your criteria. Try adjusting your search parameters.');
      } else {
        toast.success(`Found ${results.relevant_jobs.length} relevant job opportunities!`);
      }
    } catch (error) {
      console.error('Error searching for jobs:', error);
      toast.error('An error occurred while searching for jobs. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <ToastContainer position="top-right" />
      <Header />
      
      <main className="container mx-auto px-4 flex-grow py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-800">Find Your Dream Job</h1>
            <p className="text-lg text-gray-600 mt-2">
              Discover relevant job opportunities across LinkedIn, Indeed, and Glassdoor
            </p>
          </div>
          
          <SearchForm onSearch={handleSearch} isLoading={isLoading} />
          
          {searchResults && (
            <JobResults 
              jobs={searchResults.relevant_jobs} 
              isLoading={isLoading} 
            />
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App; 