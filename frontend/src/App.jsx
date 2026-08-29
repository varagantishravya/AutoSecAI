import "./styles/variables.css";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Analysis from "./components/Analysis/Analysis";
import Dashboard from "./components/Dashboard/Dashboard";
import Footer from "./components/Layout/Footer";

function App() {
  return (
    <>
      <Navbar />
      <Hero />
      <Analysis />
      <Dashboard />
      <Footer />
    </>
  );
}

export default App;