const setIsLoading = (isLoading) => {
  const statusBar = document.getElementById("status");
  if (isLoading) {
    statusBar.classList.add("loading");
  } else {
    statusBar.classList.remove("loading");
  }
};

const getChatHistory = async () => {
  setIsLoading(true);

  try {
    const response = await fetch(ENDPOINT_URL, {
      credentials: "include",
      headers: {
        Accept: "application/json",
      },
    });

    if (response.status === 401) {
      const currentUrl = encodeURIComponent(window.location.href);
      const redirectUrl = `${LOGIN_URL}?next=${currentUrl}`;
      window.alert("인증이 필요합니다. 로그인 페이지로 이동합니다.");
      window.location.href = redirectUrl;
    } else {
      const messages = await response.json();
      appendMessages(messages)
    }
  } catch (err) {
    console.error("Chat History Error:", err);
  } finally {
    setIsLoading(false);
  }

  return [];
};

const streamChat = async (userText) => {
  setIsLoading(true);

  try {
    const formData = new FormData();
    formData.append("user_text", userText);

    const response = await fetch(ENDPOINT_URL, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
      },
      body: formData,
    });

    const messages = await response.json();
    appendMessages(messages)
  } catch (err) {
    console.error("Chat Error:", err);
  } finally {
    setIsLoading(false);
  }

  return [];
};

function appendMessages(messages) {
  console.log(messages);
  const chatContainer = document.getElementById("chat-container");
  if (!chatContainer) return;

  const roleClasses = {
    notice: "role-notice",
    system: "role-system",
    assistant: "role-assistant",
    usage: "role-usage",
    user: "role-user",
  };

  messages.forEach((message) => {
    if (message.role === "event") {
      return; // Skip rendering for "event" role
    }

    const container = document.createElement("div");
    container.className = `message-container`;

    if (message.role === "usage") {
      container.className += ` ${roleClasses[message.role]}`;
      container.textContent = message.content;
      chatContainer.appendChild(container);
      return;
    }

    const roleClass = message.role ? roleClasses[message.role] : "role-system";

    container.className += ` ${roleClass}`;

    const flexContainer = document.createElement("div");
    flexContainer.className = "flex-container";

    const roleSpan = document.createElement("span");
    roleSpan.className = "font-semibold capitalize";
    roleSpan.textContent = message.role;

    const idSpan = document.createElement("span");
    idSpan.className = "text-xs";
    idSpan.textContent = message.id;

    flexContainer.appendChild(roleSpan);
    flexContainer.appendChild(idSpan);

    const contentDiv = document.createElement("div");
    contentDiv.className = "whitespace-pre-wrap";
    contentDiv.textContent = message.content;

    container.appendChild(flexContainer);
    container.appendChild(contentDiv);

    chatContainer.appendChild(container);
  });
}
