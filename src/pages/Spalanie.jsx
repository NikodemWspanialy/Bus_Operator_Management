import { useState, useEffect } from "react";

function Spalanie() {
  const [busCombustion, setBusCombustion] = useState([]);
  const [driverCombustion, setDriverCombustion] = useState([]);
  const [buses, setBuses] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [busId, setBusId] = useState('');
  const [busDate, setBusDate] = useState('');
  const [driverId, setDriverId] = useState('');
  const [driverDate, setDriverDate] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/bus/get')
      .then(response => response.json())
      .then((data) => {
        console.log('Buses:', data);
        setBuses(data.buses || []);
      })
      .catch((err) => {
        console.error('Error fetching buses:', err);
      });

    fetch('http://127.0.0.1:5000/drivers/get')
      .then(response => response.json())
      .then((data) => {
        console.log('Drivers:', data);
        setDrivers(data.drivers || []);
      })
      .catch((err) => {
        console.error('Error fetching drivers:', err);
      });
  }, []);

  const handleFetchBusCombustion = () => {
    fetch(`http://127.0.0.1:5000/combustion/get/${busId}/${busDate}`)
      .then(response => response.json())
      .then((data) => {
        console.log('Bus Combustion:', data);
        setBusCombustion(data.combustion || []);
      })
      .catch((err) => {
        console.error('Error fetching bus combustion:', err);
      });
  };

  const handleFetchDriverCombustion = () => {
    fetch(`http://127.0.0.1:5000/combustion/get/${driverId}/${driverDate}`)
      .then(response => response.json())
      .then((data) => {
        console.log('Driver Combustion:', data);
        setDriverCombustion(data.combustion || []);
      })
      .catch((err) => {
        console.error('Error fetching driver combustion:', err);
      });
  };

  return (
    <div className="posts-container">
      <h1>Spalanie</h1>

      <div>
        <h2>Pobierz spalanie dla busa</h2>
        <div>
          <label>ID Busa:</label>
          <input type="text" value={busId} onChange={e => setBusId(e.target.value)} />
        </div>
        <div>
          <label>Data:</label>
          <input type="text" value={busDate} onChange={e => setBusDate(e.target.value)} />
        </div>
        <button onClick={handleFetchBusCombustion}>Pobierz spalanie busa</button>
      </div>

      <div>
        <h2>Pobierz spalanie dla kierowcy</h2>
        <div>
          <label>ID Kierowcy:</label>
          <input type="text" value={driverId} onChange={e => setDriverId(e.target.value)} />
        </div>
        <div>
          <label>Data:</label>
          <input type="text" value={driverDate} onChange={e => setDriverDate(e.target.value)} />
        </div>
        <button onClick={handleFetchDriverCombustion}>Pobierz spalanie kierowcy</button>
      </div>

      <div>
        <h2>Spalanie Busa</h2>
        {busCombustion.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Spalanie</th>
              </tr>
            </thead>
            <tbody>
              {busCombustion.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.combustion}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>Brak danych spalania dla wybranego busa.</p>
        )}
      </div>

      <div>
        <h2>Spalanie Kierowcy</h2>
        {driverCombustion.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Spalanie</th>
              </tr>
            </thead>
            <tbody>
              {driverCombustion.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.combustion}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>Brak danych spalania dla wybranego kierowcy.</p>
        )}
      </div>
    </div>
  );
}

export default Spalanie;
