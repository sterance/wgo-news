import { Navbar } from "./components/Navbar.tsx";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.tsx";
import News from "./pages/News.tsx";
import Admin from "./pages/Admin.tsx";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/news" element={<News />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </>
  );
}

export default App;
