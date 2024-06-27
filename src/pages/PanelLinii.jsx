import { useState, useEffect } from "react";
import "../styles/PanelKierowcow.css"
import React from 'react';

function Linia() {
  const [lines, setLines] = useState([]); //zmienna ze wszystkimi liniami
  const [line, setLine] = useState({
    name: ""
  });
  const [selectedLine, setSelectedLine] = useState("");
  const [deleteLine, setDeleteLine] = useState("");
  const [updateLine, setUpdateLine] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/line/get')
    .then(response => response.json())
    .then((data) => {
      console.log(data);
      setLines(data.lines);
      console.log(lines);
    })
    .catch((err) => {
      console.log(err.message);
    });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLine((prevLine) => ({
      ...prevLine,
      [name]: value
    }))
  }

  const handleAddLine = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/line/add/${line.name}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(line),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      console.log('Line added:', data);
      if (data.line) {
        setLines((prevLines) => [...prevLines, data.line]);
      } else {
        throw new Error('Invalid data format');
      }
    } catch (error) {
      console.error('There was an error adding the line!', error);
    }
  };

  const handleDeleteLine = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/line/delete/${deleteLine}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      setLines(lines.filter(line => line.id !== deleteLine));
      setDeleteLine("");
    } catch (error) {
      console.error("Błąd przy usuwaniu linii", error);
    }
  }

  const handleUpdateLine = (line) => {
    setUpdateLine(line);
  };

  const handleSaveUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5000/line/update/${updateLine.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateLine),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log('Line updated:', data);
      setLines(lines.map(line => line.id === updateLine.id ? data.line : line));
      setUpdateLine(null);
    } catch (error) {
      console.error('There was an error updating the line!', error);
    }
  };

  return (
    <div className="posts-container">
      <h1>Panel Linii</h1>
      <div className="forms">
        <div className="form-group">
          <label>Wybierz linię:</label>
          <select
            value={selectedLine}
            onChange={e => setSelectedLine(e.target.value)}>
            <option value="">Wszystkie linie</option>
            {
              lines.map(item => (
                <option key={item.id} value={item.id}>{item.name}</option>
              ))
            }
          </select>
        </div>
        <div className="form-group">
          <form onSubmit={handleAddLine}>
            <div>
              <label>Nazwa linii:</label>
              <input type="text" name="name" value={line.name} onChange={handleChange} />
            </div>
            <br />
            <button type="submit">Dodaj linię</button>
          </form>
        </div>
        <div className="form-group">
          <form onSubmit={handleDeleteLine}>
            <label>Usuń linię:</label>
            <select
              value={deleteLine}
              onChange={e => setDeleteLine(e.target.value)}
            >
              <option value="">Wybierz linię</option>
              {
                lines.map(item => (
                  <option key={item.id} value={item.id}>{item.name}</option>
                ))
              }
            </select>
            <br />
            <button type="submit">Usuń linię</button>
          </form>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Nazwa linii</th>
          </tr>
        </thead>
        <tbody>
          {lines
            .filter(line => 
              !selectedLine || line.id === parseInt(selectedLine))
            .map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default Linia;
