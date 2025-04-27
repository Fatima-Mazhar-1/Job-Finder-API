import React from 'react';
import { FaBriefcase } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="bg-primary-700 text-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <FaBriefcase className="text-2xl mr-2" />
          <h1 className="text-xl md:text-2xl font-bold">Job Finder</h1>
        </div>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <a href="/" className="hover:text-primary-200 transition-colors">
                Home
              </a>
            </li>
            <li>
              <a href="https://github.com/Fatima-Mazhar-1/Job-Finder-API/tree/main" target="_blank" rel="noopener noreferrer" className="hover:text-primary-200 transition-colors">
                GitHub
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header; 