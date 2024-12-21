import styles from "./ChatInput.module.css";

function ChatInput({ message, setMessage, onSubmit, isLoading }) {
  return (
    <form onSubmit={onSubmit} className={styles.chatInput}>
      <input
        type="text"
        placeholder="메시지를 입력하세요"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button
        type="submit"
        disabled={isLoading}
      >
        전송
      </button>
    </form>
  );
}

export default ChatInput;
