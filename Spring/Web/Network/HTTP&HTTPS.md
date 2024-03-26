# HTTP & HTTPS
## HTTP란?(HyperText Transfer Protocol)
* 인터넷에서 클라이언트와 서버가 자원을 주고 받을 때 쓰는 통신 규약이다.
* HTTP의 구조는 요청/응답 (Request/Response) 구조로 되어있다.
1. HTTP 요청 (Requset)
  * HTTP의 메소드는 웹 서버에 대한 다양한 요청을 나타낸다. 
  * HTTP의 주요 메서드는 GET/POST/PUT/DELETE/PATCH 등이 있다.
  * 헤더(Headers) 는 요청에 대한 추가 정보를 제공한다. 헤더를 통해 서버에게 요청 컨텍스트를 알릴 수 있으며
    Content-Type(요청 데이터 유형)/Accept(응답 데이터 유형)/User-Agent(클라이언트의 브라우저/애플리케이션 정보 제공)/Authorization(인증 토큰 같은 인증 정보)를 포함할 수 있다.
* 본문(Body)은 서버로 보낼 실제 데이터를 담는다. 본문에는 폼 데이터,파일,JSON 객체 등 요청에 필요한 데이터가 포함될 수 있다. 예를 들어, 사용자가 웹 폼에 입력한 정보나 API 요청으로 보내는 JSON 데이터 등이 이에 해당된다.
2. HTTP 응답(Response)
* 상태 라인(Status Line) 은 HTTP 버전,상태 코드, 상태 메시지를 포함한다. 상태 코드는 요청이 성공했는지 실패했는지를 나타낸다(200은 성공,404는 찾을 수 없음)
* 헤더(Headers)/본문(Body)을 포함한다.

## HTTP의 단점
* HTTP의 주요 단점은 데이터가 암호화되지 않아 중간자 공격에 취약하다. 이로 인해 개인 정보와 데이터의 노출 위험이 있다.이를 보완하기 위해 HTTPS를 사용한다.

## HTTPS란?(HyperText Transfer Protocol Secure)
* HTTPS는 HTTP에 데이터 암호화 기능을 추가한 버전으로, 클라이언트와 서버 간의 안전한 자원 교환을 가능하게 한다.
* HTTPS는 SSL(Secure Socket Layer) 또는 TLS(Transport Layer Security) 프로토콜을 사용하여 데이터를 암호화한다. 이는 데이터의 기밀성과 무결성을 보장하여 중간자 공격으로부터 보호한다.
* HTTPS의 구조 역시 HTTP와 유사하게 요청/응답(Request/Response) 구조를 가지나, 모든 데이터 전송이 암호화되어 이루어진다. 이로 인해 사용자의 정보와 데이터가 안전하게 보호될 수 있다.
* HTTPS를 사용함으로써 웹사이트는 신뢰성을 높일 수 있으며, 사용자는 보안된 연결을 통해 데이터를 주고받을 수 있게 된다. 대부분의 현대 웹 브라우저는 HTTPS 연결을 통해 보안을 강조하고, 사용자에게 안전하지 않은 연결에 대해 경고한다.

###  SSL(Secure Socket Layer) 그리고 TLS(Transport Layer Security)
* SSL과 TLS를 쉽게 예를 들어 설명하자면 컴퓨터와 컴퓨터 사이에 비밀 방이 만들어지게 해준다. 이 방 안에서 우리가 주고받는 정보는 모두 암호화되어 있어서, 방 밖에 있는 사람들은 그 정보를 볼 수 없다.
* SSL과 TLS를 사용하는 이유는 인터넷을 사용해서 정보를 보낼 때 중간에 누군가 정보를 볼 수 없게 안전하게 보호하기 위해서 이다.
* TLS는 SSL의 업데이트 버전이다. 지금은 대부분 TLS를 사용하지만, 많은 사람들이 여전히 TLS 연결을 설명하는 데 SSL이라는 용어를 많이 사용한다.
