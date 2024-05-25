import React, { useState, useEffect } from "react";
import {
  BACKEND_API_URL,
  magnitudeColors,
  magnitudeColorsName,
  magnitudeColorsPicker,
} from "../constants";
import { Earthquake } from "../models/earthquake";
import { FilterParams } from "../interfaces/filter";
import {
  APIProvider,
  Map,
  Marker,
  InfoWindow,
  useMarkerRef,
} from "@vis.gl/react-google-maps";

import { Circle } from "./maps/circle";
import { Rectangle } from "./maps/rectangle";

const GoogleMapComponent: React.FC<{
  filterParams: FilterParams;
  setEarthquakeObjects: React.Dispatch<React.SetStateAction<Earthquake[]>>;
}> = ({ filterParams, setEarthquakeObjects }) => {
  const position = { lat: 39.0, lng: 35.2667 };
  var bound = {
    north: position.lat + 0.5,
    south: position.lat - 0.5,
    east: position.lng + 1.0,
    west: position.lng - 1.0,
  };
  const [bounds, setBounds] = React.useState(bound);

  const handleRectangleBoundsChange = (
    newBounds: google.maps.LatLngBoundsLiteral
  ) => {
    setBounds(newBounds);
  };

  const [apiKey, setApiKey] = useState("");
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);

  const [markerRef, marker] = useMarkerRef();
  const [activeMarker, setActiveMarker] = useState<Earthquake | null>(null);

  const [center, setCenter] = React.useState(position);
  const [radius, setRadius] = React.useState(43000);

  const [shape, setShape] = useState("none");

  const [searchButton, setSearchButton] = useState(false);

  const [infoWindowOpen, setInfoWindowOpen] = useState(true);
  const [dataCount, setDataCount] = useState<number>(0);

  const [isCircleDragging, setIsCircleDragging] = useState(false);
  const [isRectangleDragging, setIsRectangleDragging] = useState(false);

  const handleInfoWindowClose = () => {
    setInfoWindowOpen(false);
  };

  const handleShapeChange = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setShape(event.target.value);
  };

  const changeCenter = (newCenter: google.maps.LatLng | null) => {
    if (!newCenter) return;
    setCenter({ lng: newCenter.lng(), lat: newCenter.lat() });
  };

  const apiKeyUrl = BACKEND_API_URL + "google_map_key/";

  const EARTHQUAKE_API_URL = BACKEND_API_URL + "earthquakes/";
  const RECENT_EARTHQUAKE_API_URL = BACKEND_API_URL + "earthquakes/recent/";
  const EARTHQUAKE_AREA_LIST_API_URL =
    BACKEND_API_URL + "earthquakes/list/within_area/";

    useEffect(() => {
      const fetchData = async () => {
        try {
          let earthquakeObjects;
  
          const queryParams = new URLSearchParams(
            filterParams as unknown as Record<string, string>
          ).toString();
  
          if ((shape === "circle" && searchButton) || isCircleDragging) {
            const apiUrl = `${EARTHQUAKE_AREA_LIST_API_URL}?shape=circle&circle_center_lat=${center.lat}&circle_center_lng=${center.lng}&circle_radius=${radius}&${queryParams}`;
            earthquakeObjects = await Earthquake.fetchEarthquakeData(apiUrl);
          } else if ((shape === "rectangle" && searchButton) || isRectangleDragging) {
            const apiUrl = `${EARTHQUAKE_AREA_LIST_API_URL}?shape=rectangle&north=${bounds.north}&south=${bounds.south}&east=${bounds.east}&west=${bounds.west}&${queryParams}`;
            earthquakeObjects = await Earthquake.fetchEarthquakeData(apiUrl);
          } else {
            const apiUrl = Object.values(filterParams).every(
              (value) => value === ""
            )
              ? RECENT_EARTHQUAKE_API_URL
              : `${EARTHQUAKE_API_URL}?${queryParams}`;
  
            earthquakeObjects = await Earthquake.fetchEarthquakeData(apiUrl);
          }
  
          setEarthquakes(earthquakeObjects);
          setEarthquakeObjects(earthquakeObjects);
          setDataCount(earthquakeObjects.length);
        } catch (error) {
          console.error("Error fetching earthquake data:", error);
        }
      };
  
      if (searchButton || isCircleDragging || isRectangleDragging) {
        fetchData();
        setSearchButton(false);
      }
    }, [filterParams, shape, center, radius, bounds, searchButton, isCircleDragging, isRectangleDragging, setEarthquakeObjects]);
  
  const markers = earthquakes.map((earthquake) => ({
    lat: earthquake.latitude,
    lng: earthquake.longitude,
    scale: earthquake.depth,
    color: magnitudeColorsPicker(earthquake.magnitude),
  }));

  useEffect(() => {
    fetch(apiKeyUrl)
      .then((response) => response.json())
      .then((data) => setApiKey(data.GOOGLE_MAP_API_KEY))
      .catch((error) => console.error("Error fetching API key:", error));
  }, [apiKeyUrl]);

  function formatTime(originTime: any) {
    const formattedTime = originTime.split(".")[0];
    return formattedTime;
  }

  const handleSearch = () => {
    console.log("Perform API call for shape:", shape);
    setSearchButton(true);
  };

  return (
    <div>
      <div>
        <h5>Earthquake Magnitude Color Palette</h5>
        <ul
          className="d-flex justify-content-around"
          style={{ listStyleType: "none", padding: 0 }}
        >
          {Object.entries(magnitudeColors).map(([magnitude, color]) => (
            <li key={magnitude} className="d-flex">
              <div
                style={{
                  width: "20px",
                  height: "20px",
                  backgroundColor: color,
                  display: "inline-block",
                  marginRight: "10px",
                  border: "1px solid black",
                }}
              ></div>
              {
                magnitudeColorsName[
                  Object.keys(magnitudeColors).indexOf(magnitude)
                ]
              }
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h5>Map Area Shape</h5>
        <div className="d-flex">
          <select
            className="form-control w-auto me-2"
            value={shape}
            onChange={handleShapeChange}
          >
            <option value="none">None</option>
            <option value="circle">Circle</option>
            <option value="rectangle">Rectangular</option>
          </select>
          <button className="btn btn-info" onClick={handleSearch}>
            Search
          </button>
        </div>
      </div>

      <div>
        <p>Data Count: {dataCount}</p>
      </div>

      {apiKey && (
        <APIProvider apiKey={apiKey}>
          <div style={{ height: "91vh", width: "100%", overflow: "scroll" }}>
            <Map defaultZoom={6.5} defaultCenter={position}>
              {markers.map((m, index) => (
                <React.Fragment key={index}>
                  <Marker
                    key={index}
                    position={{ lat: m.lat, lng: m.lng }}
                    ref={markerRef}
                    icon={{
                      path: "M10 0 A10 10 0 1 0 10 20 A10 10 0 1 0 10 0 Z",
                      fillColor: m.color,
                      fillOpacity: 1,
                      scale: 0.6,
                      strokeColor: "black",
                      strokeWeight: 1,
                    }}
                    onClick={() => {
                      console.log("Marker clicked:", m);
                      setActiveMarker(earthquakes[index]);
                      setInfoWindowOpen(true);
                    }}
                  />
                </React.Fragment>
              ))}
              {shape === "circle" && (
                <Circle
                  radius={radius}
                  center={center}
                  onRadiusChanged={setRadius}
                  onCenterChanged={changeCenter}
                  strokeColor={"#0c4cb3"}
                  strokeOpacity={1}
                  strokeWeight={3}
                  fillColor={"#3b82f6"}
                  fillOpacity={0.3}
                  editable
                  draggable
                />
              )}
              {shape === "rectangle" && (
                <Rectangle
                  bounds={bounds}
                  onBoundsChanged={handleRectangleBoundsChange}
                  strokeColor={"#0c4cb3"}
                  strokeOpacity={1}
                  strokeWeight={3}
                  fillColor={"#3b82f6"}
                  fillOpacity={0.3}
                  editable
                  draggable
                />
              )}
              {activeMarker !== null && infoWindowOpen && (
                <InfoWindow
                  position={{
                    lat: activeMarker.latitude,
                    lng: activeMarker.longitude,
                  }}
                  onCloseClick={handleInfoWindowClose}
                >
                  <div>
                    <h6>Earthquake Information</h6>
                    <p>Location: {activeMarker.location}</p>
                    <p>Date: {activeMarker.date}</p>
                    <p>Time: {formatTime(activeMarker.origin_time)}</p>
                    <p>Magnitude: {activeMarker.magnitude}</p>
                    <p>Depth: {activeMarker.depth}</p>
                  </div>
                </InfoWindow>
              )}
            </Map>
          </div>
        </APIProvider>
      )}
      {!apiKey && <p>Loading API key...</p>}
    </div>
  );
};

export default GoogleMapComponent;
