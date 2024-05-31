import { useState, useEffect } from "react";

function PanelFloty() {
    const [posts, setPosts] = useState([]);

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
  
    return(
      <div className="posts-container">
        <h1>Panel Floty</h1>
        <table>
          <tr>
            <th>Id</th>
            <th>skrót</th>
            <th>Ilość miejsc</th>
            <th>Opis</th>
          </tr>
        {posts.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.shortcut}</td>
            <td>{item.capacity}</td>
            <td>{item.description}</td>
          </tr>
        ))}
        </table>
      </div>
    );
};

export default PanelFloty;