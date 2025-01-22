import React, { useState } from 'react';
import Slider from "react-slick"; // Import react-slick
import './Query.css';
import { FcNegativeDynamic } from "react-icons/fc";
import { FcPositiveDynamic } from "react-icons/fc";
import { SiCoveralls } from "react-icons/si";
import { IoSearchCircle } from "react-icons/io5";
import { BiAnalyse } from "react-icons/bi";
import { IoIosHappy } from "react-icons/io";
import { IoIosSad } from "react-icons/io";


import Speedometer from '../Speedometer/Speedometer';

const QueryComponent = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeSection, setActiveSection] = useState('summary'); // State to control which section is shown

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!query.trim()) {
      setError("Query text cannot be empty.");
      return;
    }

    try {
      const baseURL = process.env.REACT_APP_API_BASE_URL;
      const response = await fetch(`${baseURL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Something went wrong. Please try again.');
      }
    } catch (err) {
      setError('Failed to fetch data. Please check your connection.');
    }
  };

  // Slick carousel settings
  const carouselSettings = {
    dots: true,
    infinite: false,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    adaptiveHeight: true,
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Search Query</h1>
      <form onSubmit={handleQuerySubmit}>
        <div style={{ marginBottom: '10px', display: 'flex', alignItems: 'center' }}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
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

      {error && <div style={{ color: 'red', marginTop: '10px' }}>{error}</div>}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <div className="query-data">
            <div className="grid">
              <div className="data-column">
                <div className="nested-data">
                  <div className="nested-data-item">
                    <div className="grid-item">
                      <BiAnalyse style={{ color: '#008000' }} /> Articles Analysed: {result.query_info.total_articles}
                    </div>
                    <div className="grid-item">
                      <FcPositiveDynamic /> Positive Count: {result.query_info.positive_count}
                    </div>
                    <div className="grid-item">
                      <FcNegativeDynamic /> Negative Count: {result.query_info.negative_count}
                    </div>
                  </div>
                  <div className="nested-data-item">
                    <div className="grid-item2">
                      <Speedometer value={parseFloat(result.query_info.mean_sentiment)} />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="summary">
              <div className="nested-grid">
                <div
                  className={`nested-item ${activeSection === 'summary' ? 'active' : ''}`}
                  onClick={() => setActiveSection('summary')}
                >
                  <SiCoveralls style={{ color: '#89CFF0' }} /> Summary
                </div>
                <div
                  className={`nested-item ${activeSection === 'top3' ? 'active' : ''}`}
                  onClick={() => setActiveSection('top3')}
                >
                  <FcPositiveDynamic /> Top 3 Articles
                </div>
                <div
                  className={`nested-item ${activeSection === 'bottom3' ? 'active' : ''}`}
                  onClick={() => setActiveSection('bottom3')}
                >
                  <FcNegativeDynamic /> Bottom 3 Articles
                </div>
              </div>

              <div className="nested-content">
                {activeSection === 'summary' && <p>Summary: {result.query_info.summary}</p>}
                {activeSection === 'top3' && (
                  <Slider {...carouselSettings}>
                    {result.top3.map((article, index) => (
  <div key={index} className="carousel-item">
    <strong style={{ display: "block", borderBottom: "1px solid #FFFFFF", paddingBottom: "5px", marginBottom: "10px" }}>
      <IoIosHappy style={{ color: 'green' }} /> {article.title}
    </strong>
    <p style={{ fontStyle: "italic", color: "red" }}>Source: {article.source}</p>
    <p>{article.description}</p>
    <p style={{ color: "lightblue" }}>
      Published Date:{" "}
      {new Date(article.published_date).toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      })}
    </p>
  </div>
))}
                  </Slider>
                )}
                {activeSection === 'bottom3' && (
                  <Slider {...carouselSettings}>
                    {result.bottom3.map((article, index) => (
                      <div key={index} className="carousel-item">
                        <strong style={{ display: "block", borderBottom: "1px solid #FFFFFF", paddingBottom: "5px", marginBottom: "10px" }}>
                        <IoIosSad style={{ color: 'red' }}/>  {article.title}
                        </strong>
                        <p style={{ fontStyle: "italic", color: "red" }}>Source: {article.source}</p>
                        <p>{article.description}</p>
                        <p style={{ color: "lightblue" }}>
                          Published Date:{" "}
                          {new Date(article.published_date).toLocaleDateString("en-GB", {
                            day: "2-digit",
                            month: "long",
                            year: "numeric",
                          })}
                        </p>
                      </div>
                    ))}
                  </Slider>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QueryComponent;
