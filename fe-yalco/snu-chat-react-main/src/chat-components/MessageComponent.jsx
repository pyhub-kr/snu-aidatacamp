import React from "react";
import styles from "./MessageComponent.module.css";

const MessageComponent = ({ message }) => {
  if (message.role === "event") {
    return null;
  }

  const roleClasses = {
    notice: styles.roleNotice,
    system: styles.roleSystem,
    assistant: styles.roleAssistant,
    usage: styles.roleUsage,
    user: styles.roleUser,
  };

  if (message.role === "usage") {
    return (
      <div className={roleClasses[message.role]}>
        {message.content}
      </div>
    );
  }

  return (
    <div
      className={`${styles.messageContainer} ${
        message.role ? roleClasses[message.role] : styles.roleSystem
      }`}
    >
      <div className={styles.flexContainer}>
        <span className={`${styles.fontSemibold} capitalize`}>{message.role}</span>
        <span className={styles.textXs}>{message.id}</span>
      </div>
      <div className={styles.whitespacePreWrap}>{message.content}</div>
    </div>
  );
};

export default MessageComponent;
