import { useEffect, useRef } from "react";

import MessageComponent from "./MessageComponent";
import styles from "./ChatContainer.module.css";

function ChatContainer({ messages }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  }, [messages]);

  return (
    <div className={styles.chatContainer}>
      {messages.map((msg) => (
        <MessageComponent key={msg.id} message={msg} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatContainer;
