import React from "react";
import styles from "./ColorPicker.module.css";

const colors = ["dodgerblue", "darkorange", "mediumseagreen", "mediumpurple", "tomato"];

const ColorPicker = ({ color, setColor }) => {
  return (
    <div className={styles.colorPicker}>
      {colors.map((c) => (
        <button
          key={c}
          onClick={() => setColor(c)}
          className={color === c ? styles.selected : ""}
          style={{ backgroundColor: c }}
        >
        </button>
      ))}
    </div>
  );
};

export default ColorPicker;
