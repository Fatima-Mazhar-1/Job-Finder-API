import React from 'react';
import JobCard from './JobCard';

const JobResults = ({ jobs, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 mt-8">
        <div className="flex flex-col items-center justify-center">
          <svg className="animate-spin h-12 w-12 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="mt-4 text-lg text-gray-600">Searching for jobs...</p>
        </div>
      </div>
    );
  }

  if (!jobs || jobs.length === 0) {
    return null;
  }

  return (
    <div className="mt-8">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Search Results</h2>
        <p className="text-gray-600">Found {jobs.length} relevant job opportunities for you</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {jobs.map((job, index) => (
          <JobCard key={`${job.source}-${job.company}-${index}`} job={job} />
        ))}
      </div>
    </div>
  );
};

export default JobResults; 