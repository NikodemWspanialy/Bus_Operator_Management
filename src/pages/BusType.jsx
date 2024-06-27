import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css";

function BusType() {
  const [busTypes, setBusTypes] = useState([]); // zmienna ze wszystkimi typami autobusów
  const [busType, setBusType] = useState({
    description: "",
    shortcut: "",
    capacity: 0
  });
  const [selectedBusType, setSelectedBusType] = useState("");
  const [deleteBusType, setDeleteBusType] = useState("");
  const [updateBusType, setUpdateBusType] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/bus-type/get')
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setBusTypes(data.busTypes);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBusType((prevBusType) => ({
      ...prevBusType,
      [name]: value
    }));
  };

  const handleAddBusType = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/bus-type/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(busType),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Bus type added:', data);
      if (data.busType) {
        setBusTypes((prevBusTypes) => [...prevBusTypes, data.busType]);
      } else {
        throw new Error('Invalid data format');
      }

    } catch (error) {
      console.error('There was an error adding the bus type!', error);
    }
  };

  const handleDeleteBusType = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/bus-type/delete/${deleteBusType}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      setBusTypes(busTypes.filter(busType => busType.id !== parseInt(deleteBusType)));
      setDeleteBusType("");
    } catch (error) {
      console.error("Błąd przy usuwaniu typu autobusu", error);
    }
  };

  const handleUpdateBusType = (busType) => {
    setUpdateBusType(busType);
  };

  const handleSaveUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/bus-type/update/${updateBusType.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateBusType),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log('Bus type updated:', data);
      setBusTypes(busTypes.map(busType => busType.id === updateBusType.id ? data.busType : busType));
      setUpdateBusType(null);
    } catch (error) {
      console.error('There was an error updating the bus type!', error);
    }
  };

  return (
    <div className="posts-container">
      <h1>Panel Typów Autobusów</h1>
      <div className="forms">
        <div className="form-group">
          <label>Wybierz typ autobusu:</label>
          <select
            value={selectedBusType}
            onChange={e => setSelectedBusType(e.target.value)}>
            <option value="">Wszystkie typy autobusów</option>
            {
              busTypes.map(item => (
                <option key={item.id} value={item.id}>{item.description}</option>
              ))
            }
          </select>
        </div>
        <div className="form-group">
          <form onSubmit={handleAddBusType}>
            <div>
              <label>Opis:</label>
              <input type="text" name="description" value={busType.description} onChange={handleChange} />
            </div>
            <div>
              <label>Skrót:</label>
              <input type="text" name="shortcut" value={busType.shortcut} onChange={handleChange} />
            </div>
            <div>
              <label>Pojemność:</label>
              <input type="number" name="capacity" value={busType.capacity} onChange={handleChange} />
            </div>
            <br />
            <button type="submit">Dodaj typ autobusu</button>
          </form>
        </div>
        <div className="form-group">
          <form onSubmit={handleDeleteBusType}>
            <label>Usuń typ autobusu:</label>
            <select
              value={deleteBusType}
              onChange={e => setDeleteBusType(e.target.value)}
            >
              <option value="">Wybierz typ autobusu</option>
              {
                busTypes.map(item => (
                  <option key={item.id} value={item.id}>{item.description}</option>
                ))
              }
            </select>
            <br />
            <button type="submit">Usuń typ autobusu</button>
          </form>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Opis</th>
            <th>Skrót</th>
            <th>Pojemność</th>
          </tr>
        </thead>
        <tbody>
          {busTypes
            .filter(busType =>
              !selectedBusType || busType.id === parseInt(selectedBusType))
            .map((item) => (
              <tr key={item.id}>
                <td>{item.description}</td>
                <td>{item.shortcut}</td>
                <td>{item.capacity}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default BusType;
