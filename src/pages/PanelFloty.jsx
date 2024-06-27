import { useState, useEffect } from "react";
import "../styles/PanelFloty.css"
function PanelFloty() {
    const [posts, setPosts] = useState([]); //zmienna ze wszystkimi autobusami
    const [newBus, setNewBus] = useState({
      id: "",
      shortcut: "",
      capacity: "",
      bus_type_description: "",
      next_car_review: ""
    });
    const [filter, setFilter] = useState({
      shortcut: "",
      bus_type_description: ""
    });

    useEffect(() => {
      fetch('http://127.0.0.1:5000/bus/get')
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setPosts(data.buses);
        console.log(posts);
      })
      .catch((err) => {
        console.log(err.message);
      });
    }, []);
  
    const handleFilterChange = (e) => {
      const {name, value} = e.target;
      setFilter((prevFilter) => ({
        ...prevFilter, [name]: value
      }));
    }

    const handleNewBusChange = (e) => {
      const {name, value} = e.target;
      setNewBus((prevNewBus) => ({
        ...prevNewBus, [name]: value
      }));
    }

    const handleAddBus = async (e) => {
      console.log("Sending new bus data:", newBus);
      e.preventDefault();
      try {
        const response = await fetch("http://127.0.0.1:5000/bus/add", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newBus),
        });
        if(!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setNewBus({

          id: "",
          shortcut: "",
          capacity: "",
          bus_type_description: "",
          next_car_review: ""
        });
        setPosts(prevPosts => [...prevPosts, data.bus]);
        } catch (error) {
          console.error("Problem z dodaniem autobusu", error);
        }
      }
    
      const handleDeleteBus = async (id) => {
        if (!window.confirm("Czy na pewno chcesz usunąć autobus?")) {
          return;
        }
        try {
          const response = await fetch(`http://127.0.0.1:5000/bus/delete/${id}`, {
            method: 'DELETE',
          });

          if(!response.ok) {
            throw new Error("Network response was not ok");
          }

          setPosts(posts.filter(bus => bus.id !== id));
        } catch (error) {
          console.error("Nie mozna usunąć busa", error);
        }
      }
      const filteredPosts = posts.filter((bus) => {
        return (
          (!filter.shortcut || bus.shortcut.includes(filter.shortcut)) &&
          (!filter.bus_type_description || bus.bus_type_description.includes(filter.bus_type_description))
        )
      })

    return(
      <div className="posts-container">
        <h1>Panel Floty</h1>
        <div className="forms">
          <div className="form-group">
            <label>Wyszukaj busy</label>
          <div>
            <label>Skrót:</label>
            <input
            type="text"
            name="shortcut"
            value={filter.shortcut}
            onChange={handleFilterChange}
            />
          </div>
          <br/>
          <div>
            <label>Opis:</label>
            <input
            type="text"
            name="bus_type_description"
            value={filter.bus_type_description}
            onChange={handleFilterChange}
            />
          </div>
          </div>
          <div className="form-group">
            <form onSubmit={handleAddBus}>
              <div>
                <label>Shortcut:</label>
                <input
                type="text"
                name="shortcut"
                value={newBus.shortcut}
                onChange={handleNewBusChange}
                />
              </div>
              <div>
                <label>Ilość miejsc:</label>
                <input
                type="text"
                name="capacity"
                value={newBus.capacity}
                onChange={handleNewBusChange}
                />
              </div>
              <div>
                <label>Opis:</label>
                <input
                type="text"
                name="bus_type_description"
                value={newBus.bus_type_description}
                onChange={handleNewBusChange}
                />
              </div>
              <div>
                <label>Data przeglądu:</label>
                <input
                type="date"
                name="next_car_review"
                value={newBus.next_car_review}
                onChange={handleNewBusChange}
                />
              </div>
              <button type="submit">Dodaj autobus</button>
            </form>
          </div>
        </div>

        <table>
          <thead>
          <tr>
            <th>Id</th>
            <th>skrót</th>
            <th>Ilość miejsc</th>
            <th>Opis</th>
            <th>Data ważności przeglądu</th>
            <th>Modyfikacja</th>
          </tr>
          </thead>
          <tbody>
        {filteredPosts.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.shortcut}</td>
            <td>{item.capacity}</td>
            <td>{item.bus_type_description}</td>
            <td>{item.next_car_review}</td>
            <td>
              <button onClick={() => handleDeleteBus(item.id)}>Usuń</button>
            </td>
          </tr>
        ))}
        </tbody>
        </table>
      </div>
    );
};

export default PanelFloty;