import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css";

function PanelEventLog() {
  const [eventLogs, setEventLogs] = useState([]);
  const [eventLog, setEventLog] = useState({
    bus_id: "",
    event_id: "",
    status: "",
    start_date: "",
    end_date: ""
  });
  const [selectedEventLog, setSelectedEventLog] = useState("");
  const [deleteEventLog, setDeletedEventLog] = useState("");
  const [updateEventLog, setUpdateEventLog] = useState(null);
  const [buses, setBuses] = useState([]);
  const [events, setEvents] = useState([]);

  // Pobranie listy wszystkich event-logów
  useEffect(() => {
    fetch("http://127.0.0.1:5000/event-log/get")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setEventLogs(data.eventLogs); // Ustawienie event-logów w stanie
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  // Pobranie listy wszystkich autobusów
  useEffect(() => {
    fetch("http://127.0.0.1:5000/bus/get")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setBuses(data.buses); // Ustawienie autobusów w stanie
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  // Pobranie listy wszystkich eventów
  useEffect(() => {
    fetch("http://127.0.0.1:5000/events/get")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setEvents(data.events); // Ustawienie eventów w stanie
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  // Obsługa zmiany danych w formularzu
  const handleChange = (e) => {
    const { name, value } = e.target;
    setEventLog((prevEventLog) => ({
      ...prevEventLog,
      [name]: value
    }));
  };

  // Dodawanie nowego event-logu
  const handleAddEventLog = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/event-log/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(eventLog)
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("Event log added:", data);
      if (data.eventLog) {
        setEventLogs((prevEventLogs) => [...prevEventLogs, data.eventLog]);
      } else {
        throw new Error("Invalid data format");
      }
    } catch (error) {
      console.error("There was an error adding the event log!", error);
    }
  };

  // Usuwanie event-logu
  const handleDeleteEventLog = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/event-log/delete/${deleteEventLog}`,
        {
          method: "DELETE"
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      setEventLogs(eventLogs.filter((log) => log.id !== parseInt(deleteEventLog)));
      setDeletedEventLog("");
    } catch (error) {
      console.error("There was an error deleting the event log!", error);
    }
  };

  return (
    <div className="posts-container">
      <h1>Panel Event-Log</h1>
      <div className="forms">
        <div className="form-group">
          <label>Wybierz event:</label>
          <select
            value={selectedEventLog}
            onChange={(e) => setSelectedEventLog(e.target.value)}
          >
            <option value="">Wszystkie eventy</option>
            {eventLogs.map((log) => (
              <option key={log.id} value={log.id}>
                ID: {log.id}, Bus ID: {log.bus_id}, Event ID: {log.event_id}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <form onSubmit={handleAddEventLog}>
            <div>
              <label>Bus ID:</label>
              <select
                name="bus_id"
                value={eventLog.bus_id}
                onChange={handleChange}
              >
                <option value="">Wybierz autobus</option>
                {buses.map((bus) => (
                  <option key={bus.id} value={bus.id}>
                    {bus.description} ({bus.shortcut})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label>Event ID:</label>
              <select
                name="event_id"
                value={eventLog.event_id}
                onChange={handleChange}
              >
                <option value="">Wybierz event</option>
                {events.map((event) => (
                  <option key={event.id} value={event.id}>
                    {event.name}: {event.description}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label>Status:</label>
              <input
                type="text"
                name="status"
                value={eventLog.status}
                onChange={handleChange}
              />
            </div>
            <div>
              <label>Data rozpoczęcia:</label>
              <input
                type="date"
                name="start_date"
                value={eventLog.start_date}
                onChange={handleChange}
              />
            </div>
            <div>
              <label>Data zakończenia:</label>
              <input
                type="date"
                name="end_date"
                value={eventLog.end_date}
                onChange={handleChange}
              />
            </div>
            <br />
            <button type="submit">Dodaj event</button>
          </form>
        </div>
        <div className="form-group">
          <form onSubmit={handleDeleteEventLog}>
            <label>Usuń event:</label>
            <select
              value={deleteEventLog}
              onChange={(e) => setDeletedEventLog(e.target.value)}
            >
              <option value="">Wybierz event do usunięcia</option>
              {eventLogs.map((log) => (
                <option key={log.id} value={log.id}>
                  ID: {log.id}, Bus ID: {log.bus_id}, Event ID: {log.event_id}
                </option>
              ))}
            </select>
            <br />
            <button type="submit">Usuń event-log</button>
          </form>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Bus ID</th>
            <th>Event ID</th>
            <th>Status</th>
            <th>Data rozpoczęcia</th>
            <th>Data zakończenia</th>
          </tr>
        </thead>
        <tbody>
          {eventLogs
            .filter(
              (log) =>
                !selectedEventLog || log.id === parseInt(selectedEventLog)
            )
            .map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.bus_id}</td>
                <td>{log.event_id}</td>
                <td>{log.status}</td>
                <td>{log.start_date}</td>
                <td>{log.end_date}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default PanelEventLog;
