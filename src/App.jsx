import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import Logowanie from "./pages/Logowanie";
import PanelFloty from "./pages/PanelFloty";
import PanelKierowcow from "./pages/PanelKierowcow";
import PanelKursow from "./pages/PanelKursow";
import RozkladJazdy from "./pages/RozkladJazdy";
import Przystanki from "./pages/Przystanki";
import Linia from "./pages/PanelLinii";
import Events from "./pages/PanelEventow";
import BusType from "./pages/BusType";
import PanelEventLog from "./pages/PanelEventLog";
import Spalanie from "./pages/Spalanie";
import PanelTankowania from "./pages/Tankowanie";
import PanelOpoznien from "./pages/Opoznienia";

function App() {
  return (
    <BrowserRouter>
    <div style={{ paddingTop: '60px' }}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Logowanie />} />
          <Route path="panelfloty" element={<PanelFloty />} />
          <Route path="Panelkierowcow" element={<PanelKierowcow />} />
          <Route path="panelkursow" element={<PanelKursow />} />
          <Route path="rozkladjazdy" element={<RozkladJazdy />} />
          <Route path="przystanki" element={<Przystanki />} />
          <Route path="panellinii" element={<Linia />} />
          <Route path="paneleventow" element={<Events />} />
          <Route path="bustype" element={<BusType />} />
          <Route path="paneleventlog" element={<PanelEventLog />} />
          <Route path="spalanie" element={<Spalanie /> } />
          <Route path="tankowanie" element={<PanelTankowania />} />
          <Route path="opoznienia" element={<PanelOpoznien />} />
        </Route>
      </Routes>
    </div>
    </BrowserRouter>
  );
}

export default App