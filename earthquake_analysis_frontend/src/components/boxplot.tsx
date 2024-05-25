import React, { useEffect, useRef, useState } from "react";
import Plotly from "plotly.js-dist-min";
import { Earthquake } from "../models/earthquake";
import * as XLSX from "xlsx";

const Boxplot: React.FC<{ earthquakes: Earthquake[] }> = ({ earthquakes }) => {
  const plotRef = useRef<HTMLDivElement>(null);
  const [type, setType] = useState("box");
  const [earthquakesParameters, setEarthquakesParameters] =
    useState("magnitude");

  const getDataForParameter = (parameter: string): number[] => {
    switch (parameter) {
      case "magnitude":
        return earthquakes.map((quake) => quake.magnitude);
      case "depth":
        return earthquakes.map((quake) => quake.depth);
      default:
        return [];
    }
  };

  useEffect(() => {
    if (!plotRef.current) return;

    let trace;
    if (type === "box") {
      trace = {
        x: getDataForParameter(earthquakesParameters),
        type: "box",
        name: earthquakesParameters === "magnitude" ? "Magnitude" : "Depth",
        orientation: "h",
      };
    } else if (type === "histogram") {
      trace = {
        x: getDataForParameter(earthquakesParameters),
        type: "histogram",
      };
    }

    const data = [trace];

    const layout = {
      title:
        type === "histogram"
          ? `Histogram of ${earthquakesParameters}`
          : `Box Plot of ${earthquakesParameters}`,
      yaxis: {
        title:
          type === "histogram"
            ? "Count"
            : earthquakesParameters === "magnitude"
            ? "Magnitude"
            : "Depth",
      },
      xaxis: {
        title: earthquakesParameters === "magnitude" ? "Magnitude" : "Depth",
      },
    };

    Plotly.newPlot(plotRef.current, data, layout);

    return () => {
      Plotly.purge(plotRef.current as HTMLElement);
    };
  }, [earthquakesParameters, earthquakes, type]);

  const handleShapeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setType(event.target.value);
  };

  const handleParameterChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setEarthquakesParameters(event.target.value);
  };

  const handleDownload = () => {
    const data = earthquakes.map(({ id, event_id, date, origin_time, latitude, longitude, magnitude, depth, location }) => ({
      ID: id,
      EventID: event_id,
      Date: date,
      OriginTime: origin_time,
      Latitude: latitude,
      Longitude: longitude,
      Magnitude: magnitude,
      Depth: depth,
      Location: location,
    }));

    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Earthquakes");
    XLSX.writeFile(wb, "earthquakes.xlsx");
  };

  return (
    <div>
      <div className="d-flex justify-content-center mb-3 mt-3">
        <select
          className="form-control w-auto me-2 "
          value={type}
          onChange={handleShapeChange}
        >
          <option value="box">Boxplot</option>
          <option value="histogram">Histogram</option>
        </select>
        <select
          className="form-control w-auto me-2 ms-3"
          value={earthquakesParameters}
          onChange={handleParameterChange}
        >
          <option value="magnitude">Magnitude</option>
          <option value="depth">Depth</option>
        </select>
      </div>
      <button className="btn btn-success ms-3" onClick={handleDownload}>Download Data in CSV</button>
      <div ref={plotRef} />
    </div>
  );
};

export default Boxplot;
