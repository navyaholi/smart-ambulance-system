
import { useEffect, useState } from "react";
import "./App.css";
import api, { allocateAmbulances, getRoute } from "./api";

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [selectedPatient, setSelectedPatient] = useState(null);

  const [patients, setPatients] = useState([]);
  const [ambulances, setAmbulances] = useState([]);
  const [hospitals, setHospitals] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [allocationResults, setAllocationResults] = useState([]);
  const [allocationLoading, setAllocationLoading] = useState(false);
  const [allocationError, setAllocationError] = useState("");

  const [routeResult, setRouteResult] = useState(null);
  const [routeLoading, setRouteLoading] = useState(false);
  const [routeError, setRouteError] = useState("");
  const [routeStart, setRouteStart] = useState("Area A");
  const [routeDestination, setRouteDestination] = useState("Hospital A");

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError("");

        const [pResponse, aResponse, hResponse] = await Promise.all([
          api.get("/patients"),
          api.get("/ambulances"),
          api.get("/hospitals"),
        ]);

        const patientData = Array.isArray(pResponse.data)
          ? pResponse.data
          : pResponse.data.patients ?? [];

        const ambulanceData = Array.isArray(aResponse.data)
          ? aResponse.data
          : aResponse.data.ambulances ?? [];

        const hospitalData = Array.isArray(hResponse.data)
          ? hResponse.data
          : hResponse.data.hospitals ?? [];

        setPatients(
          patientData.map((p) => ({
            ...p,
            id: p.patient_id ?? p.id,
            name: p.name ?? p.patient_name ?? "Unknown patient",
            age: p.age ?? "N/A",
            location: p.location ?? "Unknown",
            emergency: Number(p.emergency_level ?? p.emergency ?? 1),
            condition:
              p.condition ??
              (Number(p.emergency_level ?? p.emergency ?? 1) >= 5
                ? "Critical"
                : Number(p.emergency_level ?? p.emergency ?? 1) >= 4
                  ? "Serious"
                  : "Moderate"),
          }))
        );

        setAmbulances(
          ambulanceData.map((a) => ({
            ...a,
            id: a.ambulance_id ?? a.id,
            driver: a.driver_name ?? a.driver ?? "Not specified",
            location: a.location ?? "Unknown",
            status: String(a.status ?? "Unknown"),
          }))
        );

        setHospitals(
          hospitalData.map((h) => ({
            ...h,
            id: h.hospital_id ?? h.id,
            name: h.name ?? h.hospital_name ?? "Hospital",
            location: h.location ?? "Unknown",
            beds: h.available_beds ?? h.beds ?? 0,
            capacity: h.emergency_capacity ?? h.capacity ?? 0,
          }))
        );
      } catch (err) {
        console.error("Backend connection failed:", err);
        setError(
          "Unable to load data. Make sure the Python backend is running on port 8000."
        );
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const navigate = (page) => {
    setActivePage(page);
    setSelectedPatient(null);
  };

  const availableAmbulances = ambulances.filter(
    (a) => a.status.toLowerCase() === "available"
  ).length;

  const handleAllocation = async () => {
    try {
      setAllocationLoading(true);
      setAllocationError("");
      setAllocationResults([]);

      const response = await allocateAmbulances();
      const data = response.data;

      const results = Array.isArray(data)
        ? data
        : data.assignments ??
          data.allocations ??
          data.results ??
          data.data ??
          [];

      setAllocationResults(results);

      if (!Array.isArray(results) || results.length === 0) {
        setAllocationError(
          "The backend responded, but no allocation list was found. Check the response in the browser console."
        );
        console.log("Allocation response:", data);
      }
    } catch (err) {
      console.error("Allocation failed:", err);
      setAllocationError(
        err.response?.data?.detail ?? "Unable to allocate ambulances."
      );
    } finally {
      setAllocationLoading(false);
    }
  };

  const handleRouteSearch = async (event) => {
    event.preventDefault();

    try {
      setRouteLoading(true);
      setRouteError("");
      setRouteResult(null);

      const response = await getRoute(
        routeStart.trim(),
        routeDestination.trim()
      );

      setRouteResult(response.data);
    } catch (err) {
      console.error("Route search failed:", err);
      setRouteError(
        err.response?.data?.detail ?? "Unable to calculate the route."
      );
    } finally {
      setRouteLoading(false);
    }
  };

  const renderDashboard = () => (
    <>
      <div className="welcome-card">
        <div>
          <p className="welcome-label">EMERGENCY RESPONSE CENTER</p>
          <h2>Smart Ambulance Dashboard</h2>
          <p>
            Monitor emergency cases, ambulances and hospitals from one place.
          </p>
        </div>
        <div className="system-online">
          <span className="online-dot"></span>
          System Online
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon ambulance-icon">🚑</div>
          <div>
            <span>Total Ambulances</span>
            <strong>{ambulances.length}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon available-icon">✓</div>
          <div>
            <span>Available</span>
            <strong>{availableAmbulances}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon hospital-icon">🏥</div>
          <div>
            <span>Hospitals</span>
            <strong>{hospitals.length}</strong>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon emergency-icon">⚠</div>
          <div>
            <span>Emergencies</span>
            <strong>{patients.length}</strong>
          </div>
        </div>
      </div>

      <div className="dashboard-columns">
        <div className="panel">
          <div className="panel-header">
            <div>
              <h3>Emergency Cases</h3>
              <p>Current emergency patients</p>
            </div>
            <button onClick={() => navigate("patients")}>View All</button>
          </div>

          {patients.map((p) => (
            <div className="patient-row" key={p.id}>
              <div className="avatar">P</div>
              <div className="row-main">
                <strong>{p.name}</strong>
                <span>
                  {p.id} • Age {p.age} • {p.location}
                </span>
              </div>
              <span className={`priority priority-${p.emergency}`}>
                Level {p.emergency}
              </span>
            </div>
          ))}
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <h3>Ambulance Status</h3>
              <p>Current ambulance availability</p>
            </div>
            <button onClick={() => navigate("ambulances")}>View All</button>
          </div>

          {ambulances.map((a) => (
            <div className="patient-row" key={a.id}>
              <div className="ambulance-small">🚑</div>
              <div className="row-main">
                <strong>{a.id}</strong>
                <span>
                  {a.driver} • {a.location}
                </span>
              </div>
              <span
                className={`status ${
                  a.status.toLowerCase() === "available"
                    ? "available"
                    : "busy"
                }`}
              >
                {a.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="section-heading">
        <h3>Quick Actions</h3>
        <p>Emergency management operations</p>
      </div>

      <div className="quick-grid">
        <button onClick={() => navigate("ambulances")}>
          <span>🚑</span>
          <strong>Find Ambulance</strong>
          <small>View available ambulances</small>
        </button>

        <button onClick={() => navigate("hospitals")}>
          <span>🏥</span>
          <strong>Find Hospital</strong>
          <small>Check hospital capacity</small>
        </button>

        <button onClick={() => navigate("allocation")}>
          <span>🔄</span>
          <strong>Allocate Ambulance</strong>
          <small>Assign emergency resources</small>
        </button>

        <button onClick={() => navigate("route")}>
          <span>📍</span>
          <strong>Route Planning</strong>
          <small>Find shortest route</small>
        </button>
      </div>
    </>
  );

  const renderPatients = () => (
    <div>
      <div className="page-title">
        <div>
          <h2>Emergency Patients</h2>
          <p>Monitor and manage emergency cases.</p>
        </div>
        <div className="page-badge">{patients.length} Active Cases</div>
      </div>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Patient ID</th>
              <th>Patient</th>
              <th>Age</th>
              <th>Location</th>
              <th>Emergency Level</th>
              <th>Condition</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.id}>
                <td><strong>{p.id}</strong></td>
                <td>{p.name}</td>
                <td>{p.age}</td>
                <td>{p.location}</td>
                <td>
                  <span className={`priority priority-${p.emergency}`}>
                    Level {p.emergency}
                  </span>
                </td>
                <td>{p.condition}</td>
                <td>
                  <button
                    className="small-button"
                    onClick={() => setSelectedPatient(p)}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedPatient && (
        <div className="detail-card">
          <div>
            <h3>{selectedPatient.name}</h3>
            <p>
              {selectedPatient.id} • Age {selectedPatient.age}
            </p>
          </div>
          <div className="detail-items">
            <span>
              Location <strong>{selectedPatient.location}</strong>
            </span>
            <span>
              Emergency Level <strong>{selectedPatient.emergency}</strong>
            </span>
            <span>
              Condition <strong>{selectedPatient.condition}</strong>
            </span>
          </div>
          <button
            className="close-button"
            onClick={() => setSelectedPatient(null)}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );

  const renderAmbulances = () => (
    <div>
      <div className="page-title">
        <div>
          <h2>Ambulance Management</h2>
          <p>Track ambulance availability and locations.</p>
        </div>
        <div className="page-badge green-badge">
          {availableAmbulances} Available
        </div>
      </div>

      <div className="ambulance-grid">
        {ambulances.map((a) => (
          <div className="ambulance-card" key={a.id}>
            <div className="ambulance-card-top">
              <div className="large-ambulance">🚑</div>
              <span
                className={`status ${
                  a.status.toLowerCase() === "available"
                    ? "available"
                    : "busy"
                }`}
              >
                {a.status}
              </span>
            </div>
            <h3>{a.id}</h3>
            <div className="info-line">
              <span>Driver</span><strong>{a.driver}</strong>
            </div>
            <div className="info-line">
              <span>Current Location</span><strong>{a.location}</strong>
            </div>
            <button
              className="primary-button"
              disabled={a.status.toLowerCase() !== "available"}
              onClick={() => navigate("allocation")}
            >
              {a.status.toLowerCase() === "available"
                ? "Go to Allocation"
                : "Currently Busy"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderHospitals = () => (
    <div>
      <div className="page-title">
        <div>
          <h2>Hospital Management</h2>
          <p>View hospital beds and emergency capacity.</p>
        </div>
        <div className="page-badge blue-badge">
          {hospitals.length} Hospitals
        </div>
      </div>

      <div className="hospital-grid">
        {hospitals.map((h) => (
          <div className="hospital-card" key={h.id}>
            <div className="hospital-top">
              <div className="hospital-large-icon">🏥</div>
              <span className="hospital-open">OPEN</span>
            </div>
            <h3>{h.name}</h3>
            <p className="hospital-id">{h.id} • {h.location}</p>
            <div className="capacity">
              <div>
                <span>Available Beds</span><strong>{h.beds}</strong>
              </div>
              <div>
                <span>Emergency Capacity</span><strong>{h.capacity}</strong>
              </div>
            </div>
            <div className="capacity-bar">
              <div
                style={{
                  width: `${Math.min(Number(h.beds) * 4, 100)}%`,
                }}
              ></div>
            </div>
            <button className="primary-button" onClick={() => navigate("route")}>
              Plan Route
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderAllocation = () => (
    <div>
      <div className="page-title">
        <div>
          <h2>Ambulance Allocation</h2>
          <p>Emergency resource allocation using a greedy strategy.</p>
        </div>
        <div className="page-badge">Greedy Algorithm</div>
      </div>

      <div className="algorithm-banner">
        <div className="algorithm-symbol">⚙</div>
        <div>
          <h3>Greedy Ambulance Assignment</h3>
          <p>
            The backend assigns available ambulances to emergency cases.
          </p>
        </div>
      </div>

      <div className="route-card">
        <button
          className="primary-button"
          onClick={handleAllocation}
          disabled={allocationLoading}
        >
          {allocationLoading ? "Allocating..." : "Allocate Ambulances"}
        </button>

        {allocationError && (
          <p style={{ color: "red", marginTop: "12px" }}>
            {allocationError}
          </p>
        )}

        {allocationResults.length > 0 && (
          <div style={{ marginTop: "20px" }}>
            <h3>Allocation Results</h3>
            <div className="table-card">
              <table>
                <thead>
                  <tr>
                    <th>Ambulance</th>
                    <th>Patient / Emergency</th>
                    <th>Destination / Details</th>
                  </tr>
                </thead>
                <tbody>
                  {allocationResults.map((item, index) => (
                    <tr key={item.ambulance_id ?? item.id ?? index}>
                      <td>
                        {item.ambulance_id ??
                          item.ambulance ??
                          item.id ??
                          "Not specified"}
                      </td>
                      <td>
                        {item.patient_id ??
                          item.patient ??
                          item.emergency_location ??
                          item.location ??
                          "Not specified"}
                      </td>
                      <td>
                        {item.hospital_id ??
                          item.hospital ??
                          item.destination ??
                          item.status ??
                          "Assigned"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <details style={{ marginTop: "12px" }}>
              <summary>View complete backend response</summary>
              <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>
                {JSON.stringify(allocationResults, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>

      <div className="allocation-list">
        <div className="allocation-header">
          <span>Ambulance</span><span>Location</span><span>Status</span>
        </div>
        {ambulances.map((a) => (
          <div className="allocation-item" key={a.id}>
            <div>
              <strong>🚑 {a.id}</strong>
              <small>Driver: {a.driver}</small>
            </div>
            <strong>{a.location}</strong>
            <span
              className={`status ${
                a.status.toLowerCase() === "available" ? "available" : "busy"
              }`}
            >
              {a.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  const renderRoute = () => (
    <div>
      <div className="page-title">
        <div>
          <h2>Route Planning</h2>
          <p>Calculate the shortest emergency route using Dijkstra's algorithm.</p>
        </div>
        <div className="page-badge red-badge">Dijkstra</div>
      </div>

      <div className="route-layout">
        <div className="route-card">
          <h3>Emergency Route Planner</h3>

          <form onSubmit={handleRouteSearch}>
            <div className="info-line" style={{ marginTop: "18px" }}>
              <label htmlFor="route-start">Starting location</label>
              <input
                id="route-start"
                value={routeStart}
                onChange={(event) => setRouteStart(event.target.value)}
                required
              />
            </div>

            <div className="info-line" style={{ marginTop: "12px" }}>
              <label htmlFor="route-destination">Destination</label>
              <input
                id="route-destination"
                value={routeDestination}
                onChange={(event) => setRouteDestination(event.target.value)}
                required
              />
            </div>

            <button
              className="primary-button"
              type="submit"
              disabled={routeLoading}
              style={{ marginTop: "18px" }}
            >
              {routeLoading ? "Calculating..." : "Calculate Shortest Route"}
            </button>
          </form>

          {routeError && (
            <p style={{ color: "red", marginTop: "12px" }}>{routeError}</p>
          )}

          {routeResult && (
            <div style={{ marginTop: "22px" }}>
              <h3>Calculated Route</h3>
              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  overflowWrap: "anywhere",
                  marginTop: "12px",
                }}
              >
                {JSON.stringify(routeResult, null, 2)}
              </pre>
            </div>
          )}
        </div>

        <div className="route-info">
          <div className="info-icon">🗺️</div>
          <h3>Dijkstra's Algorithm</h3>
          <p>
            The road network is represented as a weighted graph. Dijkstra's
            algorithm calculates the shortest path between the selected
            starting location and destination.
          </p>
          <div className="complexity">
            <span>Time Complexity</span>
            <strong>O((V + E) log V)</strong>
          </div>
          <div className="complexity">
            <span>Data Structure</span>
            <strong>Priority Queue</strong>
          </div>
        </div>
      </div>
    </div>
  );

  const pageContent = () => {
    switch (activePage) {
      case "patients":
        return renderPatients();
      case "ambulances":
        return renderAmbulances();
      case "hospitals":
        return renderHospitals();
      case "allocation":
        return renderAllocation();
      case "route":
        return renderRoute();
      default:
        return renderDashboard();
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">🚑</div>
          <div>
            <h1>Smart Ambulance</h1>
            <span>Emergency Management</span>
          </div>
        </div>

        <nav className="navigation">
          {[
            ["dashboard", "⌂", "Dashboard"],
            ["patients", "👤", "Patients"],
            ["ambulances", "🚑", "Ambulances"],
            ["hospitals", "🏥", "Hospitals"],
            ["allocation", "🔄", "Allocation"],
            ["route", "📍", "Route Planning"],
          ].map(([page, icon, label]) => (
            <button
              key={page}
              className={
                activePage === page ? "nav-item active" : "nav-item"
              }
              onClick={() => navigate(page)}
            >
              <span>{icon}</span>{label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="system-box">
            <span className="online-dot"></span>
            <div>
              <strong>{error ? "Backend Offline" : "Smart Ambulance"}</strong>
              <small>
                {error ? "Connection problem" : "Emergency Management"}
              </small>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h2>Smart Ambulance System</h2>
            <p>Route &amp; Hospital Allocation</p>
          </div>
          <div className="topbar-right">
            <span className="date-text">Emergency Response Center</span>
            <div className="profile">
              <div className="profile-avatar">SA</div>
              <div>
                <strong>Admin</strong>
                <small>Dispatcher</small>
              </div>
            </div>
          </div>
        </header>

        <div className="content">
          {loading ? (
            <p>Loading emergency data from backend...</p>
          ) : error ? (
            <div>
              <p style={{ color: "red" }}>{error}</p>
              <button
                className="primary-button"
                onClick={() => window.location.reload()}
              >
                Retry
              </button>
            </div>
          ) : (
            pageContent()
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
