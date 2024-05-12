import "./App.css";
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar";
import { Row, Col } from "react-bootstrap";
import SidebarComponent from "./components/sidebar";
import EarthQuakeTableComponent from "./components/table";
import GoogleMapComponent from "./components/map";
import Boxplot from "./components/boxplot";
import { FilterParams } from "./interfaces/filter";
import { Earthquake } from "./models/earthquake";
import Visualization from "./pages/visualization";

function App() {
  const [filterParams, setFilterParams] = useState<FilterParams>({
    latitude__gt: "",
    latitude__lt: "",
    longitude__gt: "",
    longitude__lt: "",
    depth__gt: "",
    depth__lt: "",
    magnitude__gt: "",
    magnitude__lt: "",
    date__gt: "",
    date__lt: "",
  });

  const [earthquakeObjects, setEarthquakeObjects] = useState<Earthquake[]>([]);

  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/data-visualization" element={<Visualization />} />
          <Route path="/" element={
            <>
              <Row className="g-0">
                <Col md={3}>
                  <SidebarComponent
                    filterParams={filterParams}
                    setFilterParams={setFilterParams}
                  />
                </Col>
                <Col md={9}>
                  <div className="main-content">
                    <GoogleMapComponent filterParams={filterParams} setEarthquakeObjects={setEarthquakeObjects}/>
                  </div>
                  <div>
                    <Boxplot earthquakes={earthquakeObjects}/>
                  </div>
                  <div className="main-content">
                    <EarthQuakeTableComponent filterParams={filterParams} earthquakes={earthquakeObjects} />
                  </div>
                </Col>
              </Row>
            </>
          } />
        </Routes>
      </Router>
    </>
  );
}

export default App;
