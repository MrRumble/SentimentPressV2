import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoSearchCircle } from "react-icons/io5";
import { FaChevronDown } from "react-icons/fa";
import GlobeComponent from '../components/Globe/Globe';
import About from '../components/About/About';
import Headlines from '../components/LandingComponents/HeadlineComponent';
import TopSearchTerm from '../components/LandingComponents/TopSearchTerm';
import SentimentDisplay from '../components/LandingComponents/TopBottomSentimentToday';
import './Landing.css';

const LandingPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const predefinedTerms = [
    "Trump", "Politics", "Business", "Science", "Sports",
    "Entertainment", "Education", "Environment", "UK", 
    "Finance", "Music", "Movies",
    'Technology', "Stock Market", "Weather", "Crime", "Starmer",
    "War", "AI", "Rugby", 'Gaza', 'Israel', 'Russia', 'Ukraine'
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      navigate(`/home?search=${encodeURIComponent(searchTerm)}`);
      setIsDropdownOpen(false);
    }
  };

  const handleTermSelect = (term) => {
    setSearchTerm(term);
    setIsDropdownOpen(false);
    navigate(`/home?search=${encodeURIComponent(term)}`);
  };

  return (
    <div className="landingpage">
      <div className="left-column-landing">
        <div className="top-row-landing">
          <div className="spinning-globe-landing">
            <GlobeComponent position={[0, 0, 0]} scale={[2, 2, 2]} />
          </div>
          <div className="website-name-landing">Sentiment Press</div>
        </div>

        <div className="middle-row-landing">
    
          <div className="row-1-middle">
            <TopSearchTerm />
          </div>
          <div className="row-2-middle">
          <div className="column-1">
            <SentimentDisplay/>
          </div>
        </div>

        </div>
      </div>

      <div className="right-column-landing">
        <div className="top-row-landing-right">
          <div style={{ position: 'relative', width: '100%' }}>
            <form onSubmit={handleSearch} style={{ 
              marginBottom: '10px', 
              display: 'flex', 
              alignItems: 'center',
              position: 'relative'
            }}>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setIsDropdownOpen(false);
                }}
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
            </form>

            {/* Dropdown for predefined terms */}
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
          </div>
        </div>
        <div className="bottom-row-landing-right">
          <About />
        </div>
        <div className="bottom-row-landing-right-2">
            <Headlines />
        </div>
      </div>
    </div>
  );
};

export default LandingPage;