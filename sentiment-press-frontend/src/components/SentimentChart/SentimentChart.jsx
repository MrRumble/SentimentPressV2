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
import ChartAnnotation from "chartjs-plugin-annotation";

ChartJS.register(ChartAnnotation);

// Registering Chart.js components
ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, TimeScale);
ChartJS.defaults.plugins.legend.labels.color = "white"; // Legend labels
ChartJS.defaults.plugins.tooltip.bodyColor = "white";   // Tooltip body
ChartJS.defaults.plugins.tooltip.titleColor = "white";  // Tooltip title

const SentimentChart = ({ searchTerm }) => {
  const [chartData, setChartData] = useState({ datasets: [] });  
  const chartRef = useRef(null);
  
  // Add new dataset when the searchTerm changes
  useEffect(() => {
    if (!searchTerm) return;

    const fetchData = async () => {
      try {
        const baseURL = process.env.REACT_APP_API_BASE_URL;
        const response = await fetch(`${baseURL}/api/get_sentiment?search_term=${searchTerm}`);
        const data = await response.json();

        const newDataset = {
          label: searchTerm, // Label for the dataset
          data: data.datasets[0].data.map((item) => ({
            x: new Date(item.x), // Convert string date to JavaScript Date object
            y: item.y,
            summary: item.summary, // Keep summary for tooltips
          })),
          borderColor: getRandomColor(), // Assign a random color to differentiate datasets
          fill: false,
          tension: 0.4,
        };

        setChartData((prevData) => ({
          ...prevData,
          datasets: [...prevData.datasets, newDataset], // Append new dataset
        }));
      } catch (error) {
        console.error("Error fetching sentiment data:", error);
      }
    };

    fetchData();
  }, [searchTerm]);

  // Generate random color for datasets
  const getRandomColor = () => {
    const letters = "456789ABCDEF"; // A more moderate range for better visibility
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * letters.length)];
    }
    return color;
  };
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Sentiment Over Time",
        color: "white",
      },
      tooltip: {
        callbacks: {
          title: () => "",
          label: (tooltipItem) => {
            const point = tooltipItem.raw;
            const formattedDate = new Intl.DateTimeFormat("en-GB", {
              weekday: "short",
              year: "numeric",
              month: "short",
              day: "numeric",
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
            type: "box",
            yMin: 0,
            yMax: 1,
            backgroundColor: "rgba(0,255,0,0.2)",
            borderWidth: 1,
          },
          {
            type: "box",
            yMin: -1,
            yMax: 0,
            backgroundColor: "rgba(255, 0, 0, 0.22)",
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
          color: "white",
        },
        title: {
          display: true,
          text: "Date",
          color: "white",
        },
        ticks: {
          color: "white", // Date labels (X-axis ticks) color
        },
      },
      y: {
        min: -1,
        max: 1,
        title: {
          display: true,
          text: "Sentiment Score",
          color: "white",
        },
        ticks: {
          stepSize: 0.5,
          color: "white",
        },
      },
    },
  };
{/* <div style={{ display: "flex", height: "95%", width: "95%" }}></div> */}
  return (
    <div style={{ display: "flex", height: "95%", width: "95%" }}>
      <div style={{ flex: 1 }}>
        {chartData.datasets.length > 0 ? (
          <Line data={chartData} options={options} ref={chartRef} />
        ) : (
          <p>Loading chart...</p>
        )}
      </div>
    </div>
  );
};

export default SentimentChart;
