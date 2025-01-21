import React from 'react';
import './Home.css';
import GlobeComponent from '../components/Globe/Globe';
import QueryComponent from '../components/QueryComponent/QueryComponent';

const Homepage = () => {
  return (
    <div className="homepage">
      {/* Swapped the positions of the left-column and right-column */}
      <div className="right-column">
        <div className="spinning-globe">
          <GlobeComponent position={[0, 0, 0]} scale={[2, 2, 2]} />
        </div>
      </div>
      
      <div className="left-column">
        <div>
          <QueryComponent />
        </div>
      </div>
    </div>
  );
}

export default Homepage;
