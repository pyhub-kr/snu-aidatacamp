import { Link } from "react-router-dom";
import styles from "./Nav.module.css";

const Nav = () => (
  <nav className={styles.nav}>
    <ul>
      <li className={styles.current}>
        <Link to="/">JS & React</Link>
      </li>
      <li>
        <Link to="/chat">Chat Project</Link>
      </li>
    </ul>
  </nav>
);

export default Nav;
