import React, { useState, useEffect } from "react";
import ColorPicker from "./ColorPicker";
import styles from "./Main.module.css";

const Main = ({ data, activeId }) => {
  const [color, setColor] = useState("dodgerblue");

  const activeContent = data.find((item) => item.id === activeId);

  return (
    <main className={styles.main}>
      <ColorPicker color={color} setColor={setColor} />
      {activeContent && (
        <section>
          <h1>{activeContent.name}</h1>
          <p>{activeContent.definition}</p>
          <ul className={styles.tags} style={{ backgroundColor: color }}>
            {activeContent.tags.map((tag) => (
              <li key={tag}>#{tag}</li>
            ))}
          </ul>
          <h2>주요 특징</h2>
          <ul className={styles.characteristics}>
            {activeContent.keyCharacteristics.map((c, idx) => (
              <li key={idx}>
                <strong>{c.subtitle}</strong>
                <br />
                <span>{c.description}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
};

export default Main;
