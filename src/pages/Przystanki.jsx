import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css"
import React from 'react';

function Przystanki() {
  const [posts, setPosts] = useState([]); //zmienna ze wszystkimi przystankami
  const [busStop, setBusStop] = useState({
    name: "",
    adress: "",
    latitude: "",
    longitude: ""
  });
  const [selectedBusStop, setSelectedBusStop] = useState("");
  const [deleteBusStop, setDeleteBusStop] = useState("");
  const [updateBusStop, setUpdateBusStop] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/bus-stop/get')
    .then(response => response.json())
    .then((data) => {
      console.log(data);
      setPosts(data.bus_stops);
      console.log(posts);
    })
    .catch((err) => {
      console.log(err.message);
    });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBusStop((prevBusStop) => ({
      ...prevBusStop,
      [name]: value
    }))
  }

  const handleAddBusStop = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/bus-stop/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(busStop),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      console.log('Bus Stop added:', data);
      if (data.bus_stop) {
        setPosts((prevPosts) => [...prevPosts, data.bus_stop]);
      } else {
        throw new Error('Invalid data format');
      }
    } catch (error) {
      console.error('There was an error adding the bus stop!', error);
    }
  };

  const handleDeleteBusStop = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/bus-stop/delete/${deleteBusStop}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      setPosts(posts.filter(busStop => busStop.id !== deleteBusStop));
      setDeleteBusStop("");
    } catch (error) {
      console.error("Błąd przy usuwaniu przystanku", error);
    }
  }

  const handleUpdateBusStop = (busStop) => {
    setUpdateBusStop(busStop);
  };

  const handleSaveUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/bus-stop/update/${updateBusStop.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateBusStop),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log('Bus Stop updated:', data);
      setPosts(posts.map(busStop => busStop.id === updateBusStop.id ? data.bus_stop : busStop));
      setUpdateBusStop(null);
    } catch (error) {
      console.error('There was an error updating the bus stop!', error);
    }
  };

  return (
    <div className="posts-container">
      <h1>Panel Przystanków</h1>
      <div className="forms">
        <div className="form-group">
          <label>Wybierz przystanek:</label>
          <select
            value={selectedBusStop}
            onChange={e => setSelectedBusStop(e.target.value)}>
            <option value="">Wszystkie przystanki</option>
            {
              posts.map(item => (
                <option key={item.id} value={item.id}>{item.name}</option>
              ))
            }
          </select>
        </div>
        <div className="form-group">
          <form onSubmit={handleAddBusStop}>
            <div>
              <label>Nazwa:</label>
              <input type="text" name="name" value={busStop.name} onChange={handleChange} />
            </div>
            <div>
              <label>Adres:</label>
              <input type="text" name="adress" value={busStop.adress} onChange={handleChange} />
            </div>
            <div>
              <label>Szerokość geograficzna:</label>
              <input type="text" name="latitude" value={busStop.latitude} onChange={handleChange} />
            </div>
            <div>
              <label>Długość geograficzna:</label>
              <input type="text" name="longitude" value={busStop.longitude} onChange={handleChange} />
            </div>
            <br />
            <button type="submit">Dodaj przystanek</button>
          </form>
        </div>
        <div className="form-group">
          <form onSubmit={handleDeleteBusStop}>
            <label>Usuń przystanek:</label>
            <select
              value={deleteBusStop}
              onChange={e => setDeleteBusStop(e.target.value)}
            >
              <option value="">Wybierz przystanek</option>
              {
                posts.map(item => (
                  <option key={item.id} value={item.id}>{item.name}</option>
                ))
              }
            </select>
            <br />
            <button type="submit">Usuń przystanek</button>
          </form>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Nazwa</th>
            <th>Adres</th>
            <th>Szerokość geograficzna</th>
            <th>Długość geograficzna</th>
          </tr>
        </thead>
        <tbody>
          {posts
            .filter(busStop => 
              !selectedBusStop || busStop.id === parseInt(selectedBusStop))
            .map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.adress}</td>
                <td>{item.latitude}</td>
                <td>{item.longitude}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default Przystanki;
