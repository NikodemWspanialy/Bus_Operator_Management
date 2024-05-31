import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import Logowanie from "./pages/Logowanie";
import PanelFloty from "./pages/PanelFloty";
import PanelKierowcow from "./pages/PanelKierowcow";
import PanelKursow from "./pages/PanelKursow";
import RozkladJazdy from "./pages/RozkladJazdy";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Logowanie />} />
          <Route path="panelfloty" element={<PanelFloty />} />
          <Route path="Panelkierowcow" element={<PanelKierowcow />} />
          <Route path="panelkursow" element={<PanelKursow />} />
          <Route path="rozkladjazdy" element={<RozkladJazdy />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App