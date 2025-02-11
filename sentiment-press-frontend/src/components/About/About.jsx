import React from 'react';


const About = () => {
  return (
    <div style={{ textAlign: 'left', padding: '20px', fontSize: '18px', maxWidth: '700px', margin: 'auto' }}>
      <h2>Stay Informed with Sentiment Analysis</h2>
      <p>
        Want to understand the news sentiment around a topic? Our platform analzes 
        <strong> 100 news articles from yesterday</strong>, processes the data, and generates a 
        <strong> sentiment score</strong> to reveal the overall tone.
      </p>

      <p><strong>🔍 Search any term to discover:</strong></p>
      <ul style={{ textAlign: 'left', display: 'inline-block' }}>
        <li>📌 A concise summary of yesterday’s news coverage</li>
        <li>📊 The <strong>top 3</strong> and <strong>bottom 3</strong> articles ranked by sentiment</li>
        <li>📈 A trend chart tracking sentiment over time</li>
        <li>📊 Side-by-side comparisons of multiple search terms</li>
      </ul>

      <p><strong>Stay ahead with real-time sentiment insights!</strong></p>
    </div>
  );
};

export default About;
