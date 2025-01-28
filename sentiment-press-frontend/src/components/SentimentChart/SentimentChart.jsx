import React, { useState, useEffect, useRef } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
} from "chart.js";
import "chartjs-adapter-luxon"; // Import Luxon date adapter
import ChartAnnotation from 'chartjs-plugin-annotation';

ChartJS.register(ChartAnnotation);

// Registering Chart.js components
ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, TimeScale);
ChartJS.defaults.plugins.legend.labels.color = "white"; // Legend labels
ChartJS.defaults.plugins.tooltip.bodyColor = "white";   // Tooltip body
ChartJS.defaults.plugins.tooltip.titleColor = "white";  // Tooltip title
ChartJS.defaults.font.color = "white";  

const SentimentChart = ({ searchTerm }) => {
  const [chartData, setChartData] = useState(null);  
  const chartRef = useRef(null);

  // Fetch data only if searchTerm is not empty
  useEffect(() => {
    const fetchData = async () => {
      if (!searchTerm) {
        return; // Do not fetch if searchTerm is empty
      }
      try {
        const baseURL = process.env.REACT_APP_API_BASE_URL;
        // Request the sentiment data for the specific search term
        const response = await fetch(`${baseURL}/api/get_sentiment?search_term=${searchTerm}`);
        const data = await response.json();
        console.log("Fetched Data:", data);

        // Create datasets with additional information (e.g., summary)
        const datasets = data.datasets.map((item) => ({
          label: item.label,
          data: item.data.map((item) => ({
            x: new Date(item.x),  // Convert string date to JavaScript Date object
            y: item.y,
            summary: item.summary, // Adding the summary field here
          })),
          borderColor: item.borderColor, // Using color from backend
          fill: false,
          tension: 0.4, // Line smoothing
        }));

        setChartData({
          datasets: datasets,
        });
      } catch (error) {
        console.error("Error fetching sentiment data:", error);
      }
    };

    if (searchTerm) {
      fetchData();
    }
  }, [searchTerm]); // Re-fetch data whenever searchTerm changes

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Sentiment Over Time",
        color: "white"
      },
      tooltip: {
        callbacks: {
          title: () => '',
          label: (tooltipItem) => {
            const point = tooltipItem.raw;
            const formattedDate = new Intl.DateTimeFormat('en-GB', {
              weekday: 'short',
              year: 'numeric',
              month: 'short',
              day: 'numeric',
            }).format(point.x);
  
            return [
              `Date: ${formattedDate}`,
              `Sentiment: ${point.y}`,
              `Summary: ${point.summary}`,
            ];
          },
        },
        intersect: false,
        mode: "nearest",
      },
      annotation: {
        annotations: [
          {
            type: 'box',
            yMin: 0,
            yMax: 1,
            backgroundColor: 'rgba(0,255,0,0.2)', 
            borderWidth: 1,
          },
          {
            type: 'box',
            yMin: -1,
            yMax: 0,
            backgroundColor: 'rgba(255, 0, 0, 0.22)', 
            borderWidth: 1,
          },
        ],
      },
    },
    scales: {
      x: {
        type: "time",
        time: {
          unit: "day",
          tooltipFormat: "ll",
          color: 'white'
        },
        title: {
          display: true,
          text: "Date",
          color: 'white'
        },
        ticks: {
          color: 'white', // Date labels (X-axis ticks) color
        },
      },
      
      y: {
        min: -1, // Extend the lower limit
        max: 1,  // Extend the upper limit
        title: {
          display: true,
          text: "Sentiment Score",
          color: 'white'
        },
        ticks: {
          stepSize: 0.5, // Optional: adjust tick spacing
          color: "white"
        },
      },
      
    },
  };
  

  return (
    <div style={{ display: 'flex', height: '95%', width: "95%" }}>
      <div style={{ flex: 1 }}>
        {chartData ? (
          <Line
            data={chartData}
            options={options}
            ref={chartRef} // Storing chart reference for cleanup
          />
        ) : (
          <p>Loading chart...</p>
        )}
      </div>
    </div>
  );
};

export default SentimentChart;
