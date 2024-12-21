import styles from "./Footer.module.css";

const Footer = () => (
  <footer className={styles.footer}>
    <h1>Contacts</h1>
    <address>
      이메일: <a href="mailto:yalco@yalco.kr">yalco@yalco.kr</a>
    </address>
  </footer>
);

export default Footer;
