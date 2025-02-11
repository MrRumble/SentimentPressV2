import React, { useState, useEffect } from "react";

const TopSearchTerm = () => {
  const [topSearch, setTopSearch] = useState({ term: "", count: 0 });

  useEffect(() => {
    // Function to fetch the top search term from the backend
    const fetchTopSearch = async () => {
      try {
        const baseURL = process.env.REACT_APP_API_BASE_URL;
        const response = await fetch(`${baseURL}/api/get-todays-top-search`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        console.log(data); // Log the response to verify the structure

        if (data.term) {
          setTopSearch({ term: data.term, count: data.count });
        } else {
          setTopSearch({ term: "No searches today", count: 0 });
        }
      } catch (error) {
        console.error("Error fetching top search term:", error);
      }
    };

    fetchTopSearch(); // Fetch immediately when component mounts
  }, []); // Empty dependency array ensures this runs only once on mount

  return (
    <div className="top-search-container">
      <h3>Today's Top Search:</h3>
      <p>
        <i>{topSearch.term}</i> - <strong>{topSearch.count} searches</strong>
      </p>
    </div>
  );
};

export default TopSearchTerm;
