import { useEffect } from "react";
import "./styles/variables.css";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Analysis from "./components/Analysis/Analysis";
import Dashboard from "./components/Dashboard/Dashboard";
import Footer from "./components/Layout/Footer";

function App() {
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      localStorage.setItem('github_token', token);
      window.history.replaceState({}, document.title, "/");
      window.dispatchEvent(new Event("user-auth-changed"));
    }
  }, []);


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