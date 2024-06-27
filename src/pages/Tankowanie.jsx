import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css";

function PanelTankowania() {
  const [refuelings, setRefuelings] = useState([]);
  const [refueling, setRefueling] = useState({
    bus_id: "",
    quantity: "",
    date: ""
  });
  const [selectedBusId, setSelectedBusId] = useState("");
  const [selectedDate, setSelectedDate] = useState("");

  useEffect(() => {
    fetch('http://127.0.0.1:5000/refueling/get')
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setRefuelings(data.refuelings || []);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setRefueling((prevRefueling) => ({
      ...prevRefueling,
      [name]: value
    }));
  };

  const handleAddRefueling = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/refueling/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(refueling),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Refueling added:', data);
      if (data.refueling) {
        setRefuelings((prevRefuelings) => [...prevRefuelings, data.refueling]);
      } else {
        throw new Error('Invalid data format');
      }
    } catch (error) {
      console.error('There was an error adding the refueling!', error);
    }
  };

  const handleFetchByBusId = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/refueling/get-by-busid/${selectedBusId}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('Refuelings by bus_id:', data);
      setRefuelings(data.buses || []); // Upewnij się, że ustawiasz właściwe dane
    } catch (error) {
      console.error('There was an error fetching the refuelings by bus_id!', error);
    }
  };

  const handleFetchByDate = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/refueling/get-by-date/${selectedDate}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('Refuelings by date:', data);
      setRefuelings(data.buses || []); // Upewnij się, że ustawiasz właściwe dane
    } catch (error) {
      console.error('There was an error fetching the refuelings by date!', error);
    }
  };

  return (
    <div className="posts-container">
      <h1>Panel Tankowania</h1>
      <div className="forms">
        <div className="form-group">
          <form onSubmit={handleAddRefueling}>
            <div>
              <label>ID Busa:</label>
              <input type="text" name="bus_id" value={refueling.bus_id} onChange={handleChange} />
            </div>
            <div>
              <label>Ilość:</label>
              <input type="text" name="quantity" value={refueling.quantity} onChange={handleChange} />
            </div>
            <div>
              <label>Data:</label>
              <input type="text" name="date" value={refueling.date} onChange={handleChange} />
            </div>
            <br />
            <button type="submit">Dodaj tankowanie</button>
          </form>
        </div>
        <div className="form-group">
          <div>
            <label>Wyszukaj tankowania po ID Busa:</label>
            <input type="text" value={selectedBusId} onChange={e => setSelectedBusId(e.target.value)} />
            <button onClick={handleFetchByBusId}>Wyszukaj</button>
          </div>
          <div>
            <label>Wyszukaj tankowania po dacie:</label>
            <input type="text" value={selectedDate} onChange={e => setSelectedDate(e.target.value)} />
            <button onClick={handleFetchByDate}>Wyszukaj</button>
          </div>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID Busa</th>
            <th>Ilość</th>
            <th>Data</th>
          </tr>
        </thead>
        <tbody>
          {refuelings.map((item) => (
            <tr key={`${item.bus_id}-${item.date}`}>
              <td>{item.bus_id}</td>
              <td>{item.quantity}</td>
              <td>{item.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PanelTankowania;
