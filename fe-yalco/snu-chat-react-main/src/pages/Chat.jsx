import { useEffect, useState } from "react";
import { ENDPOINT_URL, LOGIN_URL } from "../constants";
import Header from "../chat-components/Header";
import ChatContainer from "../chat-components/ChatContainer";
import ChatInput from "../chat-components/ChatInput";
import { useLLMChat } from "../useLLMChat";
import styles from "./Chat.module.css";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  const { getChatHistory, streamChat, isLoading, error, status } = useLLMChat({
    endpointUrl: ENDPOINT_URL,
  });

  // 401 Unauthorized 에러 처리
  useEffect(() => {
    if (status === 401) {
      const currentUrl = encodeURIComponent(window.location.href);
      const redirectUrl = `${LOGIN_URL}?next=${currentUrl}`;
      window.alert("인증이 필요합니다. 로그인 페이지로 이동합니다.");
      window.location.href = redirectUrl;
    }
  }, [status]);

  // 기존 대화내역 조회
  useEffect(() => {
    if (!window.location.hostname.includes("aidatacamp.pyhub.kr")) {
      setMessages([{
        id: 0,
        role: "system", 
        content: "이 도메인에서는 채팅이 동작하지 않습니다."
      }]);
    } else {
      async function fetchChatHistory() {
        const chatMessages = await getChatHistory();
        setMessages((prevMessages) => [...prevMessages, ...chatMessages]);
      }

      fetchChatHistory();
    }
  }, []);

  // 채팅 메시지 제출 및 스트리밍 응답 처리
  const handleSubmit = async (e) => {
    // 폼 기본 제출 동작 방지
    e.preventDefault();
    // 빈 메시지인 경우 제출하지 않음
    if (!message.trim()) return;

    // 입력창 초기화
    setMessage("");

    // 채팅 시작
    const chunkList = await streamChat(message);
    setMessages((prevMessages) => [...prevMessages, ...chunkList]);
  };

  return (
    <div className={styles.chat}>
      <Header isLoading={isLoading} />
      <hr />
      <ChatContainer messages={messages} />
      <ChatInput
      message={message}
      setMessage={setMessage}
      onSubmit={handleSubmit}
      isLoading={isLoading}
    />
    </div>
  );
}

export default Chat;
