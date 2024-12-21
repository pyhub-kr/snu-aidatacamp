import { useState } from "react";

export const useLLMChat = ({ endpointUrl }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(null);

  // GET 요청용 함수
  const getChatHistory = async () => {
    setIsLoading(true);
    setError(null);
    setStatus(null);

    try {
      const response = await fetch(endpointUrl, {
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      });

      setStatus(response.status);
      return await response.json();
    } catch (err) {
      setError(err);
      console.error("Chat History Error:", err);
    } finally {
      setIsLoading(false);
    }

    return [];
  };

  // POST 요청용 함수
  const streamChat = async (userText) => {
    setIsLoading(true);
    setError(null);
    setStatus(null);

    try {
      const formData = new FormData();
      formData.append("user_text", userText);

      const response = await fetch(endpointUrl, {
        method: "POST",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
        body: formData,
      });

      setStatus(response.status);
      return await response.json();
    } catch (err) {
      setError(err);
      console.error("Chat Error:", err);
    } finally {
      setIsLoading(false);
    }

    return [];
  };

  return {
    getChatHistory,
    streamChat,
    isLoading,
    error,
    status,
  };
};
