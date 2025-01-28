import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from './pages/Home';
import SentimentChart from './components/SentimentChart/SentimentChart';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Homepage />} /> 
          <Route path="/linegraph" element={<SentimentChart />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;