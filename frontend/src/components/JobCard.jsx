import React from 'react';
import { FaBuilding, FaMapMarkerAlt, FaBriefcase, FaMoneyBillWave, FaExternalLinkAlt } from 'react-icons/fa';

const JobCard = ({ job }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-primary-500 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start">
        <h3 className="text-xl font-bold text-gray-800">{job.job_title}</h3>
        <span className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-xs font-medium">
          {job.source}
        </span>
      </div>
      
      <div className="mt-4 space-y-2">
        <div className="flex items-center">
          <FaBuilding className="text-gray-500 mr-2" />
          <span className="text-gray-700">{job.company}</span>
        </div>
        
        {job.location && (
          <div className="flex items-center">
            <FaMapMarkerAlt className="text-gray-500 mr-2" />
            <span className="text-gray-700">{job.location}</span>
          </div>
        )}
        
        {job.experience && (
          <div className="flex items-center">
            <FaBriefcase className="text-gray-500 mr-2" />
            <span className="text-gray-700">Experience: {job.experience}</span>
          </div>
        )}
        
        {job.salary && (
          <div className="flex items-center">
            <FaMoneyBillWave className="text-gray-500 mr-2" />
            <span className="text-gray-700">Salary: {job.salary}</span>
          </div>
        )}
        
        {job.jobNature && (
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500 mr-2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z" />
            </svg>
            <span className="text-gray-700">Job Type: {job.jobNature}</span>
          </div>
        )}
      </div>
      
      <div className="mt-6">
        <a 
          href={job.apply_link} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="btn-primary flex items-center justify-center"
        >
          Apply Now
          <FaExternalLinkAlt className="ml-2" />
        </a>
      </div>
    </div>
  );
};

export default JobCard; 