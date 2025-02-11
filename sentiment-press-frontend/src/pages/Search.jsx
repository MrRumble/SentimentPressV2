import React, { useState } from 'react';
import { IoSearchCircle } from "react-icons/io5";

const SearchBar = ({ onSearch, searchTerm }) => {
  const [query, setQuery] = useState(searchTerm || '');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query); // Pass the query back to the parent when search is triggered
    }
  };

  const handleChange = (e) => {
    setQuery(e.target.value); // Update the local state when the user types
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ marginBottom: '10px', display: 'flex', alignItems: 'center' }}>
        <input
          type="text"
          value={query}
          onChange={handleChange} // Use handleChange to update state
          placeholder="Enter your query"
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            boxSizing: 'border-box',
          }}
        />
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
  );
};

export default SearchBar;
