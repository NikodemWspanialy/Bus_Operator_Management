import { Outlet, Link } from "react-router-dom";
import "../styles/navbar.css";

const Layout = () => {
  return (
    <>
      <nav className="navbar">
        <ul className="navbar-list">
          <li className="navbar-item">
            <Link to="/">Logowanie</Link>
          </li>
          <li className="navbar-item">
            <Link to="/panelfloty">Panel Floty</Link>
          </li>
          <li className="navbar-item">
            <Link to="/panelkierowcow">Panel Kierowcow</Link>
          </li>
          <li className="navbar-item">
            <Link to="/rozkladjazdy">Rozklad jazdy</Link>
          </li>
          <li className="navbar-item">
            <Link to="/panelkursow">Panel uzytkowy</Link>
          </li>
          <li className="navbar-item">
            <a href="#more">Więcej</a>
            <div className="dropdown">
            <Link to="/paneleventow">Panel zdarzen</Link>
            <Link to="/panellinii">Panel linii</Link>
            <Link to="/przystanki">Panel przystankow</Link>
            <Link to="/bustype">Panel typów autobusu</Link>
            <Link to="/paneleventlog">Panel event log</Link>
            <Link to="/spalanie">Panel spalania</Link>
            <Link to="/tankowanie">Panel tankowania</Link>
            <Link to="/opoznienia">Panel opoznien</Link>
            </div>
          </li>
        </ul>
      </nav>
      <Outlet />
    </>
  );
};

export default Layout;
