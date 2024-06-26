# TCP 3-way handshake

TCP 3-way handshake는 클라이언트와 서버 간에 안정적인 연결을 설정하기 위한 과정이다.
세 단계로 이루어져 있다.

### 정리
1. SYN: 클라이언트가 서버에 요청을 보내면서 초기 순서 번호(SYN)을 보낸다.
2. SYN-ACK: 서버가 클라이언트의 요청을 받아들이고, 자신의 초기 순서 번호(SYN)과 함께 확인 응답(ACK)을 보낸다.
3. ACK: 클라이언트가 서버의 응답을 확인(ACK)하고, 연결이 설정된다.

이 과정을 통해 클라이언트와 서버는 데이터 전송을 위한 안정적인 연결을 설정한다.
