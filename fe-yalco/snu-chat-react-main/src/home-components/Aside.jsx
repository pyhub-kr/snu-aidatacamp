import styles from "./Aside.module.css";

const Aside = ({ data, onSelect, activeId }) => {
  return (
    <aside className={styles.aside}>
      <ul>
        {data.map((item) => (
          <li
            className={item.id === activeId ? styles.selected : ""}
            key={item.id}
            onClick={() => onSelect(item.id)}
          >
            {item.name}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Aside;
