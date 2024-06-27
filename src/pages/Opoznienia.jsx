import { useState, useEffect } from "react";
import "../styles/RealTimePanel.css";

function PanelOpoznien() {
  const [realTimeData, setRealTimeData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [rideId, setRideId] = useState("");
  const [trackrouteId, setTrackrouteId] = useState("");

  useEffect(() => {
    fetch('http://127.0.0.1:5000/real-time/get')
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setRealTimeData(data.realtimes || []);
        setFilteredData(data.realtimes || []);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  const handleFilterByRideId = async () => {
    if (rideId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/real-time/get-by-ride-id/${rideId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Filtered by ride_id:', data);
        setFilteredData(data.realtimes || []);
      } catch (error) {
        console.error('There was an error fetching the real time data by ride_id!', error);
      }
    } else {
      setFilteredData(realTimeData);
    }
  };

  const handleFilterByTrackrouteId = async () => {
    if (trackrouteId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/real-time/get/${trackrouteId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Filtered by trackroute_id:', data);
        setFilteredData(data.realtimes || []);
      } catch (error) {
        console.error('There was an error fetching the real time data by trackroute_id!', error);
      }
    } else {
      setFilteredData(realTimeData);
    }
  };

  const calculateTimeDifference = (scheduled, real) => {
    const scheduledTime = new Date(`1970-01-01T${scheduled}Z`);
    const realTime = new Date(`1970-01-01T${real}Z`);
    const diffMs = Math.abs(realTime - scheduledTime);
    const diffMins = Math.floor(diffMs / 60000);
    return `${diffMins} min`;
  };

  return (
    <div className="posts-container">
      <h1>Real-Time Panel</h1>
      <div className="forms">
        <div className="form-group">
          <div>
            <label>Wyszukaj po Ride ID:</label>
            <input
              type="text"
              value={rideId}
              onChange={(e) => setRideId(e.target.value)}
            />
            <button onClick={handleFilterByRideId}>Wyszukaj</button>
          </div>
          <div>
            <label>Wyszukaj po Trackroute ID:</label>
            <input
              type="text"
              value={trackrouteId}
              onChange={(e) => setTrackrouteId(e.target.value)}
            />
            <button onClick={handleFilterByTrackrouteId}>Wyszukaj</button>
          </div>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Ride ID</th>
            <th>Trackroute ID</th>
            <th>Scheduled Time</th>
            <th>Real Time</th>
            <th>Date</th>
            <th>Difference</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((item) => (
            <tr key={`${item.ride_id}-${item.track_route_id}-${item.date}`}>
              <td>{item.ride_id}</td>
              <td>{item.track_route_id}</td>
              <td>{item.scheduled_time}</td>
              <td>{item.real_time}</td>
              <td>{item.date}</td>
              <td>{calculateTimeDifference(item.scheduled_time, item.real_time)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PanelOpoznien;
