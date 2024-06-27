import { useState } from "react";
//import "../styles/PanelKursow.css";

function PanelKursow() {
    const [busLine, setBusLine] = useState({
        line_name: "",
    })
    const [event, setEvent] = useState({
        name: "",
        description: "",
    })
    const [busStop, setBusStop] = useState({
        name: "",
        adress: "",
    })

    const handleAddBusLine = async (e) => {
        e.preventDefault();
        try {
          const response = await fetch(`http://127.0.0.1:5000/line/add/${busLine.line_name}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(busLine),
          });
    
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
    
          const data = await response.json();
          console.log("Bus line added:", data);
    
          // Clear the form fields after successful addition
          setBusLine({
            line_name: "",
          });
        } catch (error) {
          console.error("There was an error adding the bus line:", error);
        }
      };

      const handleAddBusStop = async (e) => {
        e.preventDefault();
        try {
          const response = await fetch("http://127.0.0.1:5000/bus-stop/add", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(busStop),
          });
    
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
    
          const data = await response.json();
          console.log("Bus stop added:", data);
    
          // Clear the form fields after successful addition
          setBusStop({
            name: "",
            adress: "",
          });
        } catch (error) {
          console.error("There was an error adding the bus stop:", error);
        }
      };

      const handleAddEvent = async (e) => {
        e.preventDefault();
        try {
          const response = await fetch("http://127.0.0.1:5000/events/add", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(event),
          });
    
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
    
          const data = await response.json();
          console.log("Event added:", data);
    
          // Clear the form fields after successful addition
          setEvent({
            name: "",
            description: "",
          });
        } catch (error) {
          console.error("There was an error adding the event:", error);
        }
      };
    
      const handleBusLineChange = (e) => {
        const { name, value } = e.target;
        setBusLine((prevBusLine) => ({
          ...prevBusLine,
          [name]: value,
        }));
      };
    
      const handleEventChange = (e) => {
        const { name, value } = e.target;
        setEvent((prevEvent) => ({
          ...prevEvent,
          [name]: value,
        }));
      };
    
      const handleBusStopChange = (e) => {
        const { name, value } = e.target;
        setBusStop((prevBusStop) => ({
          ...prevBusStop,
          [name]: value,
        }));
      };
    
    return (
        <div className="panel-container">
          <h1>Panel użytkowy</h1>
    
          <div className="form-container">
            <form onSubmit={handleAddBusLine} className="form">
              <h2>Dodaj linię autobusową</h2>
              <div>
                <label>Nazwa linii:</label>
                <input
                  type="text"
                  name="line_name"
                  value={busLine.line_name}
                  onChange={handleBusLineChange}
                  required
                />
              </div>
              <button type="submit">Dodaj linię</button>
            </form>
    
            <form onSubmit={handleAddEvent} className="form">
              <h2>Dodaj zdarzenie</h2>
              <div>
                <label>Nazwa zdarzenia:</label>
                <input
                  type="text"
                  name="name"
                  value={event.name}
                  onChange={handleEventChange}
                  required
                />
              </div>
              <div>
                <label>Opis:</label>
                <input
                  type="text"
                  name="description"
                  value={event.description}
                  onChange={handleEventChange}
                  required
                />
              </div>
              <button type="submit">Dodaj zdarzenie</button>
            </form>
    
            <form onSubmit={handleAddBusStop} className="form">
              <h2>Dodaj przystanek</h2>
              <div>
                <label>Nazwa przystanku:</label>
                <input
                  type="text"
                  name="name"
                  value={busStop.name}
                  onChange={handleBusStopChange}
                  required
                />
              </div>
              <div>
                <label>Adres:</label>
                <input
                  type="text"
                  name="adress"
                  value={busStop.adress}
                  onChange={handleBusStopChange}
                  required
                />
              </div>
              <button type="submit">Dodaj przystanek</button>
            </form>
          </div>
        </div>
      );
};

export default PanelKursow;