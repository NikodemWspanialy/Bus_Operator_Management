import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css"
function PanelKierowcow() {
  const [posts, setPosts] = useState([]); //zmienna ze wszystkimi kierowcami
  const [driver, setDriver] = useState({
    name: "",
    lastname: "",
    license: "",
    salary: 0,
    holidays_days: 0
  });
  const [selectedDriver, setSelectedDriver] = useState("");
  const [deleteDriver, setDeletedDriver] = useState("");
  const [updateDriver, setUpdateDriver] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/drivers/get')
    .then(response => response.json())
    .then((data) => {
      console.log(data);
      setPosts(data.drivers);
      console.log(posts);
    })
    .catch((err) => {
      console.log(err.message);
    });
  }, []);

  const handleChange = (e) => {
    const {name, value} = e.target;
    setDriver((prevDriver) => ({
      ...prevDriver,
      [name]: value
    }))
  }

  const handleAddDriver = async (e) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/drivers/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(driver),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      console.log('Driver added:', data);
      if (data.driver) {
        setPosts((prevPosts) => [...prevPosts, data.driver]);
      } else {
        throw new Error('Invalid data format');
      }


    } catch (error) {
      console.error('There was an error adding the driver!', error);
    }
  };

const handleDeleteDriver = async (e) => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/drivers/delete/${deleteDriver}`, {
      method: 'DELETE',
    });

    if(!response.ok) {
      throw new Error("Network response was not ok");
    }

    setPosts(posts.filter(driver => driver.id !== deleteDriver));
    setDeletedDriver("");
  } catch (error) {
    console.error("Błąd przy usuwaniu kierowcy", error);
  }
}

const handleUpdateDriver = (driver) => {
  setUpdateDriver(driver);
};

const handleSaveUpdate = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch(`http://127.0.0.1:5000/drivers/update/${updateDriver.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateDriver),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    console.log('Driver updated:', data);
    setPosts(posts.map(driver => driver.id === updateDriver.id ? data.driver : driver));
    setUpdateDriver(null);
  } catch (error) {
    console.error('There was an error updating the driver!', error);
  }
};

  return(
    <div className="posts-container">
      <h1>Panel Kierowcow</h1>
      <div className="forms">
        <div className="form-group">
          <label>Wybierz kierowcę:</label>
          <select
          value={selectedDriver}
          onChange={e => setSelectedDriver(e.target.value)}>
            <option value="">Wszyscy kierowcy</option>
            {
              posts.map(item => (
                <option key={item.id} value={item.id}>{item.name} {item.lastname}
                </option>
              ))
            }
          </select>
        </div>
        <div className="form-group">
          <form onSubmit={handleAddDriver}>
        <div>
          <label>Imię:</label>
          <input type="text" name="name" value={driver.name} onChange={handleChange} />
        </div>
        <div>
          <label>Nazwisko:</label>
          <input type="text" name="lastname" value={driver.lastname} onChange={handleChange} />
        </div>
        <div>
          <label>Licencja:</label>
          <input type="text" name="license" value={driver.license} onChange={handleChange} />
        </div>
        <div>
          <label>Wypłata:</label>
          <input type="text" name="salary" value={driver.salary} onChange={handleChange} />
        </div>
        <div>
          <label>Dni wolne:</label>
          <input type="text" name="holidays_days" value={driver.holidays_days} onChange={handleChange} />
        </div>
        <br/>
        <button type="submit">Dodaj kierowcę</button>
          </form>
        </div>
        <div className="form-group">
          <form onSubmit={handleDeleteDriver}>
            <label>Usuń kierowcę:</label>
            <select
            value={deleteDriver}
            onChange={e => setDeletedDriver(e.target.value)}
            >
              <option value="">Wybierz kierowcę</option>
              {
                posts.map(item => (
                  <option key={item.id} value={item.id}>{item.name} {item.lastname}</option>
                ))
              }
            </select>
            <br/>
            <button type="submit">Usuń kierowcę</button>
          </form>
        </div>
      </div>
      <table>
        <thead>
        <tr>
          <th>Imie</th>
          <th>Nazwisko</th>
          <th>Zarobki</th>
          <th>Licencja</th>
          <th>Ilość dni wolnych</th>
        </tr>
        </thead>
        <tbody>
      {posts
      .filter(driver => 
      !selectedDriver || driver.id === parseInt(selectedDriver))
      .map((item) => (
        <tr key={item.id}>
          <td>{item.name}</td>
          <td>{item.lastname}</td>
          <td>{item.salary}</td>
          <td>{item.license}</td>
          <td>{item.holidays_days}</td>
        </tr>
      ))}
      </tbody>
      </table>
    </div>
  );
};

export default PanelKierowcow