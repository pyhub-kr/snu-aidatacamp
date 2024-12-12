import { useEffect, useState } from "react";
import { ENDPOINT_URL, LOGIN_URL } from "./constants";

import { produce } from "immer";
import ChatContainer from "./components/ChatContainer";
import ChatInput from "./components/ChatInput";
import Header from "./components/Header";
import StatusBar from "./components/StatusBar";
import { useLLMChat } from "./hooks/useLLMChat";

function App() {
  const [messages, setMessages] = useState([]);
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
    async function fetchChatHistory() {
      const chatMessages = await getChatHistory();
      setMessages(
        produce((draft) => {
          draft.push(...chatMessages);
        })
      );
    }

    fetchChatHistory();
  }, [getChatHistory]);

  // 채팅 메시지 제출 및 스트리밍 응답 처리를 위한 핸들러 함수
  const handleSubmit = async (e) => {
    // 폼 기본 제출 동작 방지
    e.preventDefault();

    // 상탯값에 의존하지 않고 form 요소를 통한 값 조회
    const userText = e.target.message.value.trim();
    e.target.reset();

    // 빈 메시지인 경우 제출하지 않음
    if (!userText) return;

    // 스트리밍 채팅 시작
    const chunkList = await streamChat(userText);
    setMessages(
      produce((draft) => {
        draft.push(...chunkList);
      })
    );
  };

  return (
    <div className="max-w-2xl mx-auto px-4">
      <Header title="snu-aidatacamp" />
      <StatusBar isLoading={isLoading} error={error} />
      <hr className="my-4" />
      <ChatContainer messages={messages} />
      <ChatInput
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
