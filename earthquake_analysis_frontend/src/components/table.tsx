import React, { useEffect, useState } from "react";
import { Table, Container, Pagination } from "react-bootstrap";
import { BACKEND_API_URL } from "../constants";
import { Earthquake } from "../models/earthquake";
import { FilterParams } from "../interfaces/filter";

const EarthQuakeTableComponent: React.FC<{ filterParams: FilterParams; earthquakes: Earthquake[] }> = ({
  filterParams,
  earthquakes,
}) => {
  const ROWS_PER_PAGE = 1000;
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(earthquakes.length / ROWS_PER_PAGE);

  const handlePageChange = (pageNumber: number) => {
    setCurrentPage(pageNumber);
  };

  return (
    <Container>
      {Object.values(filterParams).every((value) => value === "") ? (
        <h4>Recent Earthquakes</h4>
      ) : (
        <h4>Filtered Earthquakes</h4>
      )}

      <Table responsive>
        <thead>
          <tr>
            <th>Event ID</th>
            <th>Date</th>
            <th>Time</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Depth</th>
            <th>Magnitude</th>
            <th>Location</th>
          </tr>
        </thead>
        <tbody>
          {earthquakes.map((quake, index) => (
            <tr key={index}>
              <td>{quake.event_id}</td>
              <td>{quake.date}</td>
              <td>{quake.origin_time}</td>
              <td>{quake.latitude}</td>
              <td>{quake.longitude}</td>
              <td>{quake.depth}</td>
              <td>{quake.magnitude}</td>
              <td>{quake.location}</td>
            </tr>
          ))}
        </tbody>
      </Table>

      <Pagination>
        {Array.from(Array(totalPages).keys()).map((pageNumber) => (
          <Pagination.Item
            key={pageNumber + 1}
            active={pageNumber + 1 === currentPage}
            onClick={() => handlePageChange(pageNumber + 1)}
          >
            {pageNumber + 1}
          </Pagination.Item>
        ))}
      </Pagination>
    </Container>
  );
};
export default EarthQuakeTableComponent;