import { useEffect, useRef } from "react";

import MessageComponent from "./MessageComponent";

function ChatContainer({ messages }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  }, [messages]);

  return (
    <div className="mb-4 space-y-2 h-[60vh] overflow-y-auto">
      {messages.map((msg) => (
        <MessageComponent key={msg.id} message={msg} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatContainer;
