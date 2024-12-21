import styles from "./ErrorAlert.module.css";

export default function ErrorAlert({ error }) {
  return (
    <div className={styles.errorAlert} role="alert">
      <strong>Error: </strong>
      <span>
        {error.message || JSON.stringify(error)}
      </span>
    </div>
  );
}
