# 서울대학교 웹앱개발 겨울캠프 2024 리액트 샘플

## 리액트 개발서버 구동하기

### 소스코드 받기

```
git clone https://github.com/pyhub-kr/snu-aidatacamp.git
cd snu-aidatacamp/fe-react
```

### 라이브러리 설치

```
npm install
```

### 환경변수 설정

API 서버는 디폴트로 `https://aidatacamp.pyhub.kr`로 설정되어있습니다. 다른 주소로 변경하실려면 아래와 같이 `REACT_APP_HOST` 환경변수를 변경해주세요.
본 Create React App 에서는 프로젝트 루트에 `.env` 파일이 있다면 자동으로 로딩합니다. 

```.env
# .env 파일
REACT_APP_HOST=https://aidatacamp.pyhub.kr
```

### 개발 서버 구동

CRA에서는 디폴트로 3000 포트로 구동됩니다.

```
npm start
```

`https://aidatacamp.pyhub.kr` 서버에서는 다음 3개 주소에 대해 CORS 접근을 허용합니다.

+ `http://fe.aidatacamp.pyhub.kr:3000`
+ `http://fe.aidatacamp.pyhub.kr:5500`
+ `http://fe.aidatacamp.pyhub.kr:5173`

## 커스텀 도메인 지정하기

`aidatacamp.pyhub.kr` 도메인의 세션 쿠키를 공유받을려면, 로컬 개발서버도 `.aidatacamp.pyhub.kr` 도메인을 가져야 합니다.
`localhost` 도메인에서는 브라우저가 세션 쿠키를 공유해주지 않습니다.

로컬 개발머신에서 `hosts` 파일을 변경하여, 로컬 `127.0.0.1` 주소에 대해 `fe.aidatacamp.pyhub.kr` 도메인을 부여해줍시다.
이 주소의 서버는 없으며, 로컬 개발머신 만을 가리키게 될 것입니다.

### 윈도우

관리자 권한으로 메모장을 실행하여 `C:\Windows\System32\drivers\etc\hosts` 파일을 열고 다음을 추가

```
127.0.0.1       fe.aidatacamp.pyhub.kr
```

### 맥/리눅스

`/etc/hosts` 파일에 다음을 추가

```
127.0.0.1       fe.aidatacamp.pyhub.kr
```

### 브라우저로 접속 테스트

먼저 개발서버를 구동해주시구요.

```
npm start
```

본 CRA 프로젝트에서는 디폴트로 `3000` 포트로 구동됩니다. 그렇다면 브라우저로 http://fe.aidatacamp.pyhub.kr:3000 주소로 접속하셔서, 페이지가 뜨면 성공입니다.

로그인이 필요하면 `https://aidatacamp.pyhub.kr/accounts/login/` 주소로 자동 이동할 것이구요.
회원가입 하시면 자동 로그인이 되고 다시 리액트 페이지로 자동 이동할 것입니다.
만약 리액트 페이지로 자동 이동되지 않고 `/accounts/profile/` 페이지로 이동하신다면 수동으로 리액트 페이지로 이동 부탁드립니다.

혹시 `This site can’t provide a secure connection` 페이지가 뜨신다면, 브라우저에서 `https` 페이지로 자동 이동한 상태일 것입니다.

브라우저 설정에서 브라우저 히스토리를 모두 삭제하신 후에 다시 http://fe.aidatacamp.pyhub.kr:3000 주소로 접속해주세요. 

## 소스코드 설명

### Tailwind CSS

`public/index.html`에 Tailwind CSS, CDN 버전이 적용되어있습니다.
이는 개발용일뿐, 실서비스 목적으로는 Tailwind CSS 빌드가 필요합니다.

### 프론트엔드 허용 주소

`https://aidatacamp.pyhub.kr` 서버에서는 다음 3개 주소에 대해서 CORS 허용되어있습니다.

+ `http://fe.aidatacamp.pyhub.kr:3000`
+ `http://fe.aidatacamp.pyhub.kr:5500`
+ `http://fe.aidatacamp.pyhub.kr:5173`

### 채팅내역 조회

+ `credentials: "include"`를 지정하여 세션 쿠키를 함께 전송해야만, `https://aidatacamp.pyhub.kr`의 세션 쿠키를 API 요청에 담을 수 있습니다.
+ `Accept: "application/json"` 헤더를 지정해야만 서버로부터 JSON 응답을 받을 수 있습니다. 지정하지 않으면 HTMX/HTML 응답을 받게 됩니다.
+ 아래 `/example/agent/chat/` 주소에서의 응답은 **항상 SSE 응답**입니다.

```js
const endpointUrl = "https://aidatacamp.pyhub.kr/example/agent/chat/";

const response = await fetch(endpointUrl, {
  credentials: "include",
  headers: {
    Accept: "application/json",
  },
});

response.status;  // 응답 상태코드 확인

response.body.getReader();  // SSE 응답을 채팅 메시지 목록에 반영
```

+ SSE 응답 파싱 루틴은 [./src/hooks/useLLMChat.js](./src/hooks/useLLMChat.js) 코드의 `handleEventStream` 함수를 참고해주세요.

### 비인증 상황에서는 응답 상태코드는 401

API 요청 시에 비인증 상황에서는 응답 상태코드는 `401` 입니다. `401` 응답에서는 `https://aidatacamp.pyhub.kr/accounts/login/` 주소로 페이지 이동을 해주세요. 이때 `next` 쿼리 파라미터로 현재 리액트 주소를 지정해주시면 인증 후에 `next` 주소로 자동 이동합니다.

그런데 로그인 요청 주소가 아래 3개 주소에 해당되지 않는다면 그 주소로 이동하지 않고 디폴트 SUCCESS URL인 `https://aidatacamp.pyhub.kr/accounts/profile/` 주소로 이동하게 됩니다.

+ `http://fe.aidatacamp.pyhub.kr:3000`
+ `http://fe.aidatacamp.pyhub.kr:5500`
+ `http://fe.aidatacamp.pyhub.kr:5173`

```js
const LOGIN_URL = "https://aidatacamp.pyhub.kr/accounts/login/";

useEffect(() => {
  if (status === 401) {
    const currentUrl = encodeURIComponent(window.location.href);
    const redirectUrl = `${LOGIN_URL}?next=${currentUrl}`;
    window.alert("인증이 필요합니다. 로그인 페이지로 이동합니다.");
    window.location.href = redirectUrl;
  }
}, [status]);
```

### 유저 입력 텍스트 메시지 전송

+ 유저 입력 텍스트는 반드시 `user_text` name으로 POST 전송해주셔야 합니다.
+ 서버 응답으로 SSE 방식으로 전송받게 됩니다.

```js
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

response.status;  // 응답 상태 코드 확인

response.body.getReader();  // SSE 응답을 채팅 메시지 목록에 반영
```

### 수신 데이터 예시

```jsonl
{"id": "id_fd1fb5bb9f9c4f908407471ef51de31f", "content": "챗봇 서비스에 오신 것을 환영합니다. ;)", "mode": "overwrite", "role": "notice"}

{"id": "id_067632e8f7de4351be2b2990c6939de5", "content": "You are a language tutor.\r\n[언어]로 대화를 나눕시다. 번역과 발음을 제공하지 않고 [언어]로만 답변해주세요.\r\n\"[상황]\"의 상황으로 상황극을 진행합니다.\r\n가능한한 [언어] [레벨]에 맞는 단어와 표현을 사용해주세요.\r\n--\r\n[언어] : 영어\r\n[상황] : 스타벅스에서 커피 주문\r\n[레벨] : 초급", "mode": "overwrite", "role": "system"}

{"id": "id_b07ee231333849578d7b297dc7868262", "content": "첫 문장으로 대화를 시작하세요.", "mode": "overwrite", "role": "user"}

{"id": "id_c95576fc9a8249babed39c348a6de0c4", "content": null, "mode": "thinking-start", "role": "event"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": "", "mode": "overwrite", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": "Hello", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": "!", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " What", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " can", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " I", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " get", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " for", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " you", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": " today", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": "?", "mode": "append", "role": "assistant"}

{"id": "run_27da75fd_9b45_466d_a8c3_eb40ca8f5ca5", "content": "", "mode": "append", "role": "assistant"}

{"id": "id_befc4b5b355448fd90e0c8f113a1896f", "content": "입력 토큰: 122, 출력 토큰: 10", "mode": "overwrite", "role": "usage"}
```

