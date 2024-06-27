import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css";
function Events() {
  const [events, setEvents] = useState([]); // zmienna ze wszystkimi zdarzeniami
  const [event, setEvent] = useState({
    name: "",
    description: ""
  });
  const [selectedEvent, setSelectedEvent] = useState("");
  const [deleteEvent, setDeleteEvent] = useState("");
  const [updateEvent, setUpdateEvent] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/events/get')
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setEvents(data.events);
        console.log(events);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEvent((prevEvent) => ({
      ...prevEvent,
      [name]: value
    }));
  };

  const handleAddEvent = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/events/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(event),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Event added:', data);
      if (data.event) {
        setEvents((prevEvents) => [...prevEvents, data.event]);
      } else {
        throw new Error('Invalid data format');
      }
    } catch (error) {
      console.error('There was an error adding the event!', error);
    }
  };

  const handleDeleteEvent = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/events/delete/${deleteEvent}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      setEvents(events.filter(event => event.id !== deleteEvent));
      setDeleteEvent("");
    } catch (error) {
      console.error("Błąd przy usuwaniu zdarzenia", error);
    }
  }

  const handleUpdateEvent = (event) => {
    setUpdateEvent(event);
  };

  const handleSaveUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/events/update/${updateEvent.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateEvent),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log('Event updated:', data);
      setEvents(events.map(event => event.id === updateEvent.id ? data.event : event));
      setUpdateEvent(null);
    } catch (error) {
      console.error('There was an error updating the event!', error);
    }
  };

  return (
    <div className="posts-container">
      <h1>Panel zdarzeń</h1>
      <div className="forms">
        <div className="form-group">
          <label>Wybierz zdarzenie:</label>
          <select
            value={selectedEvent}
            onChange={e => setSelectedEvent(e.target.value)}>
            <option value="">Wszystkie zdarzenia</option>
            {
              events.map(item => (
                <option key={item.id} value={item.id}>{item.name} - {item.description}</option>
              ))
            }
          </select>
        </div>
        <div className="form-group">
          <form onSubmit={handleAddEvent}>
            <div>
              <label>Nazwa:</label>
              <input type="text" name="name" value={event.name} onChange={handleChange} />
            </div>
            <div>
              <label>Opis:</label>
              <input type="text" name="description" value={event.description} onChange={handleChange} />
            </div>
            <br />
            <button type="submit">Dodaj zdarzenie</button>
          </form>
        </div>
        <div className="form-group">
          <form onSubmit={handleDeleteEvent}>
            <label>Usuń zdarzenie:</label>
            <select
              value={deleteEvent}
              onChange={e => setDeleteEvent(e.target.value)}
            >
              <option value="">Wybierz zdarzenie</option>
              {
                events.map(item => (
                  <option key={item.id} value={item.id}>{item.name} - {item.description}</option>
                ))
              }
            </select>
            <br />
            <button type="submit">Usuń zdarzenie</button>
          </form>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Nazwa</th>
            <th>Opis</th>
          </tr>
        </thead>
        <tbody>
          {events
            .filter(event =>
              !selectedEvent || event.id === parseInt(selectedEvent))
            .map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.description}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default Events;
