import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Logowanie</Link>
          </li>
          <li>
            <Link to="/panelfloty">Panel Floty</Link>
          </li>
          <li>
            <Link to="/panelkierowcow">Panel Kierowcow</Link>
          </li>
          <li>
            <Link to="/panelkursow">Panel kursow</Link>
          </li>
          <li>
            <Link to="/rozkladjazdy">Rozklad jazdy</Link>
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  )
};

export default Layout;