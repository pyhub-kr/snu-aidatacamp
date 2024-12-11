const MessageComponent = ({ message }) => {
  
    if(message.role === "event") {
      return null;
    }
  
    const roleStyles = {
      notice: "bg-blue-100 text-blue-800 border-blue-200", 
      system: "bg-gray-100 text-gray-800 border-gray-200",
      assistant: "bg-green-100 text-green-800 border-green-200",
      usage: "text-gray-500 text-xs",
      user: "bg-yellow-100 text-yellow-800 border-yellow-200",
    };
  
    if (message.role === 'usage') {
      return (
        <div className={`${roleStyles[message.role]}`}>
          {message.content}
        </div>
      );
    }
  
    return (
      <div
        className={`p-4 my-2 rounded-lg border ${roleStyles[message.role] || roleStyles.system} ${
          message.role === 'user' ? 'ml-auto max-w-[80%]' : 
          message.role === 'assistant' ? 'mr-auto max-w-[80%]' : 'w-full'
        }`}
      >
        <div className="flex items-center gap-2 mb-1">
          <span className="font-semibold capitalize">{message.role}</span>
          <span className="text-xs text-gray-500">{message.id}</span>
        </div>
        <div className="whitespace-pre-wrap">{message.content}</div>
      </div>
    );
  };
  
  export default MessageComponent;
  