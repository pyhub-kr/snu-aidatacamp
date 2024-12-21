import { Link } from "react-router-dom";
import styles from "./Header.module.css";

const Header = ({ isLoading }) => (
  <header className={styles.header}>
    <Link to="/">◀ Home</Link>
    <h1>
      AI Chat
    </h1>
    <div className={styles.status}>
      { isLoading && <span>⏳ Loading...</span> }
    </div>
  </header>
)
export default Header;