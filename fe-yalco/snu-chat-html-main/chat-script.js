if (!window.location.hostname.includes("aidatacamp.pyhub.kr")) {
  const message = {
    id: 0,
    role: "system", 
    content: "이 도메인에서는 채팅이 동작하지 않습니다."
  };
  appendMessages([message]);

} else {
  const chatInputText = document.getElementById("chat-input-text");
  const chatInputButton = document.getElementById("chat-input-button");

  chatInputButton.addEventListener("click", () => {
    streamChat(chatInputText.value);
  });
  chatInputText.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      streamChat(chatInputText.value);
    }
  });

  getChatHistory();
}

