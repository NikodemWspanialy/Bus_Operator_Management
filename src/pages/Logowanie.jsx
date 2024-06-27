import { useState } from "react";

function Logowanie() {

  const [admin, setAdmin] = useState({
    login: "",
    password: ""
  })

  const handleSubmit = (e) => {
    e.preventDefault();
  }

  const handleChange = (e) => {
    const {name, value} = e.target;
    setAdmin((prevAdmin) => ({
      ...prevAdmin,
      [name]: value
    }))
  }

    return (
      <>
        <h1>Panel logowania</h1>
        <br/>
        <form onSubmit={handleSubmit}>
          <label>Podaj login: </label>
          <input
          type="text"
          name="login"
          value={admin.login}
          onChange={handleChange} />
          <br/>
          <label>Podaj hasło:</label>
          <input
          type="password"
          name="password"
          value={admin.password}
          onChange={handleChange} />
          <br/>
          <button type="submit">Zaloguj się</button>
        </form>
      </>
    );
  };
  
  export default Logowanie;