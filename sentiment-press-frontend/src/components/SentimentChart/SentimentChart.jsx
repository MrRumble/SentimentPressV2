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

const SentimentChart = () => {
  const [chartData, setChartData] = useState(null);  
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseURL = process.env.REACT_APP_API_BASE_URL;
        const response = await fetch(`${baseURL}/api/get_sentiments`);
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

    fetchData();
  }, []); // Fetch only once on mount

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Sentiment Over Time",
      },
      tooltip: {
        callbacks: {
          title: () => '',  // Hides the top line (title) in the tooltip
          label: (tooltipItem) => {
            const point = tooltipItem.raw;
      
            // Format the date (stored as point.x) into a user-friendly format
            const formattedDate = new Intl.DateTimeFormat('en-GB', {
              weekday: 'short',
              year: 'numeric',
              month: 'short',
              day: 'numeric',
            }).format(point.x);
      
            // Return an array with multiline text
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
            backgroundColor: 'rgba(0,255,0,0.2)',  // Green shading for above 0
            borderWidth: 1,
          },
          {
            type: 'box',
            yMin: -1,
            yMax: 0,
            backgroundColor: 'rgba(255, 0, 0, 0.22)',  // Red shading for below 0
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
          tooltipFormat: "ll",  // Format used by the tooltip for the date
        },
        title: {
          display: true,
          text: "Date",
        },
      },
      y: {
        min: -1,
        max: 1,
        title: {
          display: true,
          text: "Sentiment Score",
        },
      },
    },
  };
  

  return (
    <div style={{ display: 'flex' }}>
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
