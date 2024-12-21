import React, { useState, useEffect } from "react";
import { DATA_URL } from "../constants";
import Header from "../home-components/Header";
import Nav from "../home-components/Nav";
import Aside from "../home-components/Aside";
import Main from "../home-components/Main";
import Footer from "../home-components/Footer";
import styles from "./Home.module.css";

const Home = () => {
  const [data, setData] = useState([]);
  const [activeId, setActiveId] = useState("js");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(DATA_URL);
        const json = await response.json();
        setData(json);
      } catch (error) {
        console.error("Data fetching error:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <Header />
      <Nav />
      <div className={styles.contents}>
        <Aside data={data} onSelect={setActiveId} activeId={activeId} />
        <Main data={data} activeId={activeId} />
      </div>
      <Footer />
    </>
  );
};

export default Home;
