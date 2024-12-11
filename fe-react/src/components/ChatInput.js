function ChatInput({ message, setMessage, onSubmit, isLoading }) {
  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-2">
      <input
        type="text"
        className="w-full p-2 border border-gray-300 rounded"
        placeholder="메시지를 입력하세요"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded"
        disabled={isLoading}
      >
        전송
      </button>
    </form>
  );
}

export default ChatInput;
