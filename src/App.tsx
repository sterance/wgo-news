import { Navbar } from "./components/Navbar.tsx";
import { Footer } from "./components/Footer.tsx";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.tsx";
import News from "./pages/News.tsx";
import Article from "./pages/Article.tsx";
import Admin from "./pages/Admin.tsx";

function App() {
  return (
    <>
      <Navbar />
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/news" element={<News />} />
          <Route path="/news/:id" element={<Article />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </div>
      <Footer />
    </>
  );
}

export default App;
