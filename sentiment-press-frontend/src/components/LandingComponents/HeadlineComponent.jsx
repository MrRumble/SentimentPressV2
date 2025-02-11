import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./Headline.css";

const Headlines = () => {
  const [headlines, setHeadlines] = useState([]);
  const [currentHeadline, setCurrentHeadline] = useState(null);

  // Function to get yesterday's date
  const getYesterdayDate = () => {
    const today = new Date();
    today.setDate(today.getDate() - 1);  // Set the date to yesterday
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return today.toLocaleDateString('en-US', options); // Format the date
  };

  useEffect(() => {
    // Function to fetch headlines from the backend
    const fetchHeadlines = async () => {
      try {
        const baseURL = process.env.REACT_APP_API_BASE_URL;
        const response = await fetch(`${baseURL}/api/get-headlines`, {
          method: 'GET',  // Adjusted to GET request
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        console.log(data);  // Log the response to verify the structure
        setHeadlines(data.headlines);  // Set headlines from the nested 'headlines' array
      } catch (error) {
        console.error("Error fetching headlines:", error);
      }
    };

    fetchHeadlines();  // Fetch the headlines when the component mounts
  }, []);  // Empty dependency array means this runs only once when the component mounts

  // Set an interval to switch the current headline every 3 seconds
  useEffect(() => {
    const intervalId = setInterval(() => {
      if (headlines.length > 0) {
        const randomIndex = Math.floor(Math.random() * headlines.length);
        setCurrentHeadline(headlines[randomIndex]);
      }
    }, 6000); // 3 seconds

    // Clear the interval on component unmount
    return () => clearInterval(intervalId);
  }, [headlines]);  // Runs only after headlines are fetched

  return (
    <div className="headline-container">
      <AnimatePresence>
        {currentHeadline && (
          <motion.div
            key={currentHeadline.main_headline}  // Use main_headline to ensure unique key
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }} // 0.5 second fade-in and fade-out
            className="headline"
          >
            <p><strong>Yesterday's Headlines:</strong> <i>{getYesterdayDate()}</i></p> {/* Italicize yesterday's date */}
            <h2 style={{ color: '#920089' }}><i>{currentHeadline.search_term}</i></h2> {/* Italicize search term */}
            <p><i>{currentHeadline.main_headline}</i></p> {/* Italicize main headline */}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Headlines;
