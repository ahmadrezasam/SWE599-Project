import React, { useState, useEffect } from "react";
import { Earthquake } from "../models/earthquake";
import { BACKEND_API_URL } from "../constants";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function Chart() {
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);
  const [selectedYear, setSelectedYear] = useState<number>(
    new Date().getFullYear()
  );
  const [selectedMonth, setSelectedMonth] = useState<number>(
    new Date().getMonth() + 1
  );

  const EARTHQUAKE_API_URL = BACKEND_API_URL + "earthquakes/date/";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const queryParams = new URLSearchParams({
          year: selectedYear.toString(),
          month: selectedMonth.toString(),
        }).toString();
        const apiUrl = `${EARTHQUAKE_API_URL}?${queryParams}`;
        console.log("API URL:", apiUrl);
        const earthquakeObjects = await Earthquake.fetchEarthquakeData(apiUrl);
        console.log("Fetched earthquake data:", earthquakeObjects);
        setEarthquakes(earthquakeObjects);
      } catch (error) {
        console.error("Error fetching earthquake data:", error);
      }
    };
    fetchData();
  }, [selectedYear, selectedMonth]);

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const years = Array.from(
    { length: new Date().getFullYear() - 1900 + 1 },
    (_, i) => new Date().getFullYear() - i
  );

  const getDaysOfMonth = (year: number, monthIndex: number) => {
    const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
    return Array.from({ length: daysInMonth }, (_, i) => i + 1);
  };

  const calculateDailyAverages = () => {
    const dailyAveragesMagnitude: number[] = [];
    const dailyAveragesDepth: number[] = [];
    const monthIndex = selectedMonth - 1;
    const daysOfMonth = getDaysOfMonth(selectedYear, monthIndex);

    daysOfMonth.forEach((day) => {
      const dataForDay = earthquakes.filter((earthquake) => {
        const earthquakeDate = new Date(earthquake.date);
        return (
          earthquakeDate.getMonth() === monthIndex &&
          earthquakeDate.getDate() === day
        );
      });

      const magnitudesForDay = dataForDay.map(
        (earthquake) => earthquake.magnitude
      );
      const depthsForDay = dataForDay.map((earthquake) => earthquake.depth);

      const averageMagnitude =
        magnitudesForDay.reduce((sum, magnitude) => sum + magnitude, 0) /
        magnitudesForDay.length;
      const averageDepth =
        depthsForDay.reduce((sum, depth) => sum + depth, 0) /
        depthsForDay.length;

      dailyAveragesMagnitude.push(averageMagnitude || 0);
      dailyAveragesDepth.push(averageDepth || 0);
    });

    return { magnitude: dailyAveragesMagnitude, depth: dailyAveragesDepth };
  };

  const handleMonthChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedMonth(months.indexOf(event.target.value) + 1); // Add 1 to convert from zero-based to one-based index
  };

  const handleYearChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedYear(parseInt(event.target.value));
  };

  const data = {
    labels: getDaysOfMonth(selectedYear, selectedMonth - 1), // Subtract 1 to convert from one-based to zero-based index
    datasets: [
      {
        label: "Average Magnitude",
        data: calculateDailyAverages().magnitude,
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
      {
        label: "Average Depth",
        data: calculateDailyAverages().depth,
        borderColor: "rgb(54, 162, 235)",
        backgroundColor: "rgba(54, 162, 235, 0.5)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: `${
          months[selectedMonth - 1]
        } ${selectedYear} Earthquakes - Daily Averages`, // Subtract 1 to convert from one-based to zero-based index
      },
    },
  };

  return (
    <div className="container">
      <h2>Earthquake Chart</h2>
      <div className="form-group h6 d-flex">
        <label htmlFor="months" className="col-1">
          Select Month:
        </label>
        <select
          className="form-control w-auto"
          id="months"
          value={months[selectedMonth - 1]}
          onChange={handleMonthChange}
        >
          {" "}
          {/* Subtract 1 to convert from one-based to zero-based index */}
          {months.map((month) => (
            <option key={month} value={month}>
              {month}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group h6 d-flex">
        <label htmlFor="years" className="col-1">
          Select Year:
        </label>
        <select
          className="form-control w-auto"
          id="years"
          value={selectedYear}
          onChange={handleYearChange}
        >
          {years.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>
      <Line options={options} data={data} />
    </div>
  );
}
