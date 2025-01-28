import React, { useState } from 'react';
import './Home.css';
import GlobeComponent from '../components/Globe/Globe';
import QueryComponent from '../components/QueryComponent/QueryComponent';
import SentimentChart from '../components/SentimentChart/SentimentChart';

const Homepage = () => {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="homepage">
      <div className="right-column">
        <div className="top-row">
          <div className="spinning-globe">
            <GlobeComponent position={[0, 0, 0]} scale={[2, 2, 2]} />
          </div>
        </div>
        <div className="bottom-row">
          <SentimentChart searchTerm={searchTerm} />
        </div>
      </div>

      <div className="left-column">
        <QueryComponent onSearch={setSearchTerm} />
      </div>
    </div>
  );
}

export default Homepage;
