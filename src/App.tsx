import { Navbar } from "./components/Navbar.tsx";

function App() {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <Navbar />
      <main id="main" className="page" tabIndex={-1}></main>
    </>
  );
}

export default App;
