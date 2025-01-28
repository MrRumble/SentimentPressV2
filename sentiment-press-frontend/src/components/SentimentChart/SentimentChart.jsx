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

    // Cleanup the chart instance when the component unmounts or data changes
    return () => {
      if (chartRef.current && chartRef.current.chartInstance) {
        chartRef.current.chartInstance.destroy();
      }
    };
  }, []); // Empty dependency array to fetch data once on mount

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Sentiment Over Time",
      },
      tooltip: {
        callbacks: {
          // Custom tooltip callback to show more detailed information
          label: (tooltipItem) => {
            const point = tooltipItem.raw;
            return `Sentiment: ${point.y}, Summary: ${point.summary}`; // Format tooltip label
          },
        },
        intersect: false,
        mode: "nearest",
      },
    },
    scales: {
      x: {
        type: "time",
        time: {
          unit: "day",  // You can change this to "minute", "hour", etc., if you have smaller time intervals
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
    <div>
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
  );
};

export default SentimentChart;
