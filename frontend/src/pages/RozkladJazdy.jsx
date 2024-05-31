import { useState, useEffect } from "react";

function RozkladJazdy() {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
      fetch('http://127.0.0.1:5000/bus_stop_schedule/get/4')
      .then(response => response.json())
      .then((data) => {
        console.log(data);
        setPosts(data.departures);
        console.log(posts);
      })
      .catch((err) => {
        console.log(err.message);
      });
    }, []);
  
    return(
      <div className="posts-container">
        <h1>Rozklad jazdy dla przystanku o od 4</h1>
        <table>
          <tr>
            <th>Id</th>
            <th>Linia</th>
            <th>Czas odjazdu</th>
          </tr>
        {posts.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.line_name}</td>
            <td>{item.time}</td>
          </tr>
        ))}
        </table>
      </div>
    );
};

export default RozkladJazdy;