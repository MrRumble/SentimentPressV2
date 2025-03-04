import React, { useState } from 'react';
import { IoSearchCircle } from "react-icons/io5";
import { FaChevronDown } from "react-icons/fa";

const SearchBar = ({ onSearch, searchTerm, errorMessage }) => {
  const [query, setQuery] = useState(searchTerm || '');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const predefinedTerms = [
    "Trump", "Politics", "Business", "Science", "Sports",
    "Entertainment", "Education", "Environment", "UK", 
    "Finance", "Music", "Movies",
    'Technology', "Stock Market", "Weather", "Crime", "Starmer",
    "War", "AI", "Rugby", 'Gaza', 'Israel', 'Russia', 'Ukraine'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
      setIsDropdownOpen(false);
    }
  };

  const handleChange = (e) => {
    setQuery(e.target.value);
    setIsDropdownOpen(false);
  };

  const handleTermSelect = (term) => {
    setQuery(term);
    setIsDropdownOpen(false);
    onSearch(term);
  };

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      <form onSubmit={handleSubmit}>
        <div style={{ 
          marginBottom: '10px', 
          display: 'flex', 
          alignItems: 'center', 
          position: 'relative' 
        }}>
          <input
            type="text"
            value={query}
            onChange={handleChange}
            placeholder="Enter your query, or select the dropdown for our top picks.."
            style={{
              width: '100%',
              padding: '10px',
              fontSize: '16px',
              boxSizing: 'border-box',
              paddingRight: '50px',
            }}
          />
          <button
            type="button"
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            style={{
              position: 'absolute',
              right: '60px',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <FaChevronDown style={{ color: '#920089' }} />
          </button>
          <button
            type="submit"
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '16px',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              marginLeft: '4px',
            }}
          >
            <IoSearchCircle style={{ fontSize: '50px', color: '#920089' }} />
          </button>
        </div>
      </form>

      {isDropdownOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          width: '100%',
          maxHeight: '300px',
          overflowY: 'auto',
          backgroundColor: 'white',
          border: '1px solid #ddd',
          borderRadius: '4px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
          zIndex: 10,
        }}>
          {predefinedTerms.map((term, index) => (
            <div
            key={index}
            onClick={() => handleTermSelect(term)}
            style={{
              padding: '10px',
              cursor: 'pointer',
              color: 'black', 
              hover: {
                backgroundColor: '#f0f0f0'
              }
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = '#f0f0f0';
              e.target.style.color = 'black'; 
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'white';
              e.target.style.color = 'black'; 
            }}
          >
            {term}
          </div>
          ))}
        </div>
      )}

      {errorMessage && (
        <div style={{ color: 'red', fontSize: '14px', marginTop: '8px' }}>
          {errorMessage}
        </div>
      )}
    </div>
  );
};

export default SearchBar;