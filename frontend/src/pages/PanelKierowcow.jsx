import { useState, useEffect } from "react";

function PanelKierowcow() {
  const [posts, setPosts] = useState([]);

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

  return(
    <div className="posts-container">
      <h1>Panel Kierowcow</h1>
      <table>
        <tr>
          <th>Imie</th>
          <th>Nazwisko</th>
          <th>Zarobki</th>
          <th>Licencja</th>
          <th>Ilość dni wolnych</th>
        </tr>
      {posts.map((item) => (
        <tr key={item.id}>
          <td>{item.name}</td>
          <td>{item.lastname}</td>
          <td>{item.salary}</td>
          <td>{item.license}</td>
          <td>{item.holidays_days}</td>
        </tr>
      ))}
      </table>
    </div>
  );
};

export default PanelKierowcow