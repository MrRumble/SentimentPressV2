import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoSearchCircle } from "react-icons/io5";
import GlobeComponent from '../components/Globe/Globe';
import About from '../components/About/About';
import Headlines from '../components/LandingComponents/HeadlineComponent';
import TopSearchTerm from '../components/LandingComponents/TopSearchTerm';
import SentimentDisplay from '../components/LandingComponents/TopBottomSentimentToday';
import './Landing.css';

const LandingPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      navigate(`/home?search=${encodeURIComponent(searchTerm)}`);
    }
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
          <h1>Search for Sentiment Analysis</h1>
          <form onSubmit={handleSearch} style={{ marginBottom: '10px', display: 'flex', alignItems: 'center' }}>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
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
          </form>
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
