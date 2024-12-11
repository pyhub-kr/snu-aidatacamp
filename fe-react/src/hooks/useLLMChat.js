import { useCallback, useState } from "react";

export const useLLMChat = ({ endpointUrl }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(null);

  // GET 요청용 스트림 함수
  const getChatHistory = useCallback(
    async function* () {
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

        yield* handleEventStream(response.body.getReader());
      } catch (err) {
        setError(err);
        console.error("Chat History Error:", err);
      } finally {
        setIsLoading(false);
      }
    },
    [endpointUrl],
  );

  // POST 요청용 스트림 함수
  const streamChat = useCallback(
    async function* (userText) {
      setIsLoading(true);
      setError(null);
      setStatus(null);

      // const csrftoken = window.document.cookie
      //   .split("; ")
      //   .find((row) => row.startsWith("csrftoken="))
      //   ?.split("=")[1];

      try {
        const formData = new FormData();
        formData.append("user_text", userText);
        // formData.append("csrfmiddlewaretoken", csrftoken);

        const response = await fetch(endpointUrl, {
          method: "POST",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
          body: formData,
        });

        setStatus(response.status);

        yield* handleEventStream(response.body.getReader());
      } catch (err) {
        setError(err);
        console.error("Chat Error:", err);
      } finally {
        setIsLoading(false);
      }
    },
    [endpointUrl],
  );

  return {
    getChatHistory,
    streamChat,
    isLoading,
    error,
    status,
  };
};

// Event stream 처리를 위한 헬퍼 함수
const handleEventStream = async function* (reader) {
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const text = decoder.decode(value);

    const lines = text.split("\n\n");
    for (const line of lines) {
      if (line.trim()) {
        const cleanedLine = line.replace(/^data:\s*/, "");
        try {
          yield JSON.parse(cleanedLine);
        } catch (err) {
          console.error(err);
        }
      }
    }
  }
};
