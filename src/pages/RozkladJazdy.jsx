import { useState, useEffect } from "react";

function RozkladJazdy() {
    const [posts, setPosts] = useState([]);
    const [przystanki, setPrzystanki] = useState([]);
    const [filteredStops, setFilteredStops] = useState([]);
    const [selectedStop, setSelectedStop] = useState('');
    const [selectedStopId, setSelectedStopId] = useState(null);
    const [direction, setDirection] = useState("");

    useEffect(() => {
      if (selectedStopId !== null) {
      fetch(`http://127.0.0.1:5000/bus-stop-schedule/get/${selectedStopId}`)
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setPosts(data.departures);
        console.log(posts);
      })
      .catch((err) => {
        console.log(err.message);
      });
    }
    }, [selectedStopId]);
  
    const handleStopChange = (e) => {
      const { value } = e.target;
      setSelectedStop(value);
      if (Array.isArray(przystanki)) {
        const filtered = przystanki.filter(stop => stop.name.includes(value));  // Zaktualizowane, aby sprawdzać `name`
        setFilteredStops(filtered);
  
        if (filtered.length > 0) {
          const lastChar = filtered[0].name.slice(-1);  // Pobierz ostatni znak `name` pierwszego dopasowanego przystanku
          if (lastChar === '1') {
            setDirection('petla');
          } else if (lastChar === '2') {
            setDirection('dworzec');
          } else {
            setDirection('');
          }
        } else {
          setDirection('');
        }
      } else {
        console.error("przystanki is not an array", przystanki);
      }
    };
       
    const handleStopSelect = (stop) => {
      setSelectedStop(stop.name);
      setSelectedStopId(stop.id);
      setFilteredStops([]);
    };

    useEffect(() => {
      fetch('http://127.0.0.1:5000/bus-stop/get').then(response => response.json())
      .then((data) => {
        console.log(data);
        setPrzystanki(data.bus_stops);
        console.log(przystanki);
      })
      .catch((err) => {
        console.log(err.message);
      })
    }, []);

    const transformData = (data) => {
      const transformed = {};
      data.forEach(item => {
        if (!transformed[item.line_name]) {
          transformed[item.line_name] = [];
        }
        transformed[item.line_name].push(item.time);
      });
      return transformed;
    };
  
    const transformedPosts = transformData(posts);

    return(
      <div className="posts-container">
        <h1>Rozklad jazdy dla przystanku o danym przystanku</h1>

        <div className="autocomplete-container">
        <input
          type="text"
          placeholder="Wpisz nazwę przystanku"
          value={selectedStop}
          onChange={handleStopChange}
        />
        {filteredStops.length > 0 && (
          <ul className="autocomplete-list">
            {filteredStops.map(stop => (
              <li key={stop.id} onClick={() => handleStopSelect(stop)}>
                {stop.name}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h2>Kierunek jazdy: {direction}</h2>
      </div>
        <table>
          <thead>
          <tr>
            <th>Linia</th>
            <th>Czas odjazdu</th>
          </tr>
          </thead>
        <tbody>
          {Object.entries(transformedPosts).map(([line_name, time]) => (
            <tr key={line_name}>
              <td>{line_name}</td>
              <td>{time.join(', ')}</td>
            </tr>
          ))}
        </tbody>
        </table>
      </div>
    );
};

export default RozkladJazdy;