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
    async function fetchChatHistory() {
      const chatHistory = await getChatHistory();
      await applyChunkList(chatHistory);
    }

    fetchChatHistory();
  }, [getChatHistory]);

  const applyChunkList = async (chunkList) => {
    // 현재 처리 중인 메시지의 내용과 ID를 추적하기 위한 변수
    let currentMessageContent = "";
    let currentMessageId = null;

    // 메시지 내용을 업데이트하는 헬퍼 함수
    // Immer를 사용하여 불변성을 유지하면서 메시지 내용 갱신
    const updateMessages = (id, content) => {
      setMessages(
        produce((draft) => {
          const msg = draft.find((msg) => msg.id === id);
          if (msg) {
            msg.content = content;
          }
        }),
      );
    };

    // 스트리밍 응답을 순차적으로 처리
    for await (const response of chunkList) {
      // 새로운 메시지가 시작되는 경우
      if (currentMessageId !== response.id) {
        // 이전 메시지가 있다면 최종 내용으로 업데이트
        if (currentMessageId) {
          updateMessages(currentMessageId, currentMessageContent);
        }
        // 새 메시지 정보 설정
        currentMessageId = response.id;
        currentMessageContent = response.content;
        // 메시지 추가 전에 중복 확인
        setMessages(
          produce((draft) => {
            // 같은 ID를 가진 메시지가 없을 때만 새 메시지 추가
            if (!draft.some((msg) => msg.id === response.id)) {
              draft.push({
                id: response.id,
                content: response.content,
                role: response.role,
                mode: response.mode,
              });
            }
          }),
        );
      } else {
        // 기존 메시지 업데이트: overwrite 모드면 내용을 덮어쓰고,
        // 아니면 기존 내용에 새 내용을 추가
        currentMessageContent =
          response.mode === "overwrite"
            ? response.content
            : currentMessageContent + response.content;
        updateMessages(currentMessageId, currentMessageContent);
      }
    }
  };

  // 채팅 메시지 제출 및 스트리밍 응답 처리를 위한 핸들러 함수
  const handleSubmit = async (e) => {
    // 폼 기본 제출 동작 방지
    e.preventDefault();
    // 빈 메시지인 경우 제출하지 않음
    if (!message.trim()) return;

    // 입력창 초기화
    setMessage("");

    // 스트리밍 채팅 시작
    const chunkList = await streamChat(message);
    await applyChunkList(chunkList);
  };

  return (
    <div className="max-w-2xl mx-auto px-4">
      <Header title="snu-aidatacamp" />
      <StatusBar isLoading={isLoading} error={error} />
      <hr className="my-4" />
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

export default App;
