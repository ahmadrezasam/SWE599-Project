import React, { useEffect } from "react";
import { Form } from "react-bootstrap";
import { FilterParams } from "../interfaces/filter";

interface SidebarProps {
  filterParams: FilterParams;
  setFilterParams: React.Dispatch<React.SetStateAction<FilterParams>>;
}

const SidebarComponent: React.FC<SidebarProps> = ({
  filterParams,
  setFilterParams,
}) => {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFilterParams((prevParams) => ({ ...prevParams, [name]: value }));
  };

  useEffect(() => {
    const handleScroll = () => {
      const sidebar = document.getElementById("sidebar-component");
      const stickyOffset = 500; 

      if (sidebar && window.scrollY > stickyOffset) {
        sidebar.classList.add("sticky");
      } else if (sidebar) {
        sidebar.classList.remove("sticky");
      }
    };

    window.addEventListener("scroll", handleScroll);

    // Clean up event listener on unmount
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div id="sidebar-component">
      <div className="sidebar">
        <div className="mb-3">
          <h5>Latitude & Longitude</h5>
          <label className="fw-bold">Latitude</label>
          <div className="d-flex">
            <Form.Group controlId="latitudeMin">
              <Form.Label>Min:</Form.Label>
              <Form.Control
                type="number"
                name="latitude__gt"
                value={filterParams.latitude__gt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Min"
                className="sidebar-input"
              />
            </Form.Group>
            <Form.Group controlId="latitudeMax">
              <Form.Label>Max:</Form.Label>
              <Form.Control
                type="number"
                name="latitude__lt"
                value={filterParams.latitude__lt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Max"
                className="sidebar-input"
              />
            </Form.Group>
          </div>
          <label className="fw-bold mt-3">Longitude</label>
          <div className="d-flex">
            <Form.Group controlId="longitudeMin">
              <Form.Label>Min:</Form.Label>
              <Form.Control
                type="number"
                name="longitude__gt"
                value={filterParams.longitude__gt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Min"
                className="sidebar-input"
              />
            </Form.Group>
            <Form.Group controlId="longitudeMax">
              <Form.Label>Max:</Form.Label>
              <Form.Control
                type="number"
                name="longitude__lt"
                value={filterParams.longitude__lt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Max"
                className="sidebar-input"
              />
            </Form.Group>
          </div>
        </div>
        <hr/>

        <div className="mb-4">
          <h5>Depth</h5>
          <div className="d-flex">
            <Form.Group controlId="depthMin">
              <Form.Label>Min:</Form.Label>
              <Form.Control
                type="number"
                name="depth__gt"
                value={filterParams.depth__gt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Min"
                className="sidebar-input"
              />
            </Form.Group>
            <Form.Group controlId="depthMax">
              <Form.Label>Max:</Form.Label>
              <Form.Control
                type="number"
                name="depth__lt"
                value={filterParams.depth__lt}
                onChange={handleInputChange}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Max"
                className="sidebar-input"
              />
            </Form.Group>
          </div>
        </div>
        <hr />

        <div className="mb-4">
          <h5>Magnitude</h5>
          <div className="d-flex">
            <Form.Group controlId="magnitude__gt">
              <Form.Label>Min:</Form.Label>
              <Form.Control
                type="number"
                name="magnitude__gt"
                value={filterParams.magnitude__gt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Min"
                className="sidebar-input"
              />
            </Form.Group>
            <Form.Group controlId="magnitudeMax">
              <Form.Label>Max:</Form.Label>
              <Form.Control
                type="number"
                name="magnitude__lt"
                value={filterParams.magnitude__lt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Max"
                className="sidebar-input"
              />
            </Form.Group>
          </div>
        </div>
        <hr />

        <div className="mb-4">
          <h5>Date</h5>
          <div className="d-flex">
            <Form.Group controlId="dateMin">
              <Form.Label>Start:</Form.Label>
              <Form.Control
                type="date"
                name="date__gt"
                value={filterParams.date__gt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Min"
                className="sidebar-input sidebar-input-date"
              />
            </Form.Group>
            <Form.Group controlId="dateMax">
              <Form.Label>End:</Form.Label>
              <Form.Control
                type="date"
                name="date__lt"
                value={filterParams.date__lt}
                onChange={handleInputChange}
                min={0}
                onFocus={(e) =>
                  e.target.addEventListener(
                    "wheel",
                    function (e) {
                      e.preventDefault();
                    },
                    { passive: false }
                  )
                }
                placeholder="Max"
                className="sidebar-input sidebar-input-date"
              />
            </Form.Group>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SidebarComponent;