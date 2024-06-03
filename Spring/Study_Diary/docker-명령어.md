### 이미지 관련 명령어

1. docker images: 로컬에 다운로드된 이미지 목록 확인
2. docker pull 이미지명: 원격 레지스트리에서 이미지 다운로드
3. docker rmi 이미지명: 로컬에서 이미지 삭제
### 컨테이너 관련 명령어

1. docker ps: 실행 중인 컨테이너 목록 확인
2. docker ps -a: 모든 컨테이너(중지된 것 포함) 목록 확인
3. docker run 이미지명: 새 컨테이너 실행
4. docker start 컨테이너명: 중지된 컨테이너 재시작
5. docker stop 컨테이너명: 실행 중인 컨테이너 중지
6. docker rm 컨테이너명: 컨테이너 삭제

### 컨테이너 실행 옵션

* -d: 백그라운드 모드(데몬 모드)
* -p 호스트포트:컨테이너포트: 포트 매핑
* -v 호스트경로:컨테이너경로: 볼륨 마운트
* --name 컨테이너명: 컨테이너 이름 지정
### Docker Compose 명령어

1. docker-compose up: 컨테이너 생성 및 시작
2. docker-compose up -d: 백그라운드 모드로 컨테이너 생성 및 시작
3. docker-compose down: 컨테이너 중지 및 삭제
4. docker-compose ps: 실행 중인 컨테이너 목록 확인

### 기타 명령어

1. docker logs 컨테이너명: 컨테이너 로그 확인
2. docker exec -it 컨테이너명 /bin/bash: 컨테이너 내부 bash 셸 접속
3. docker network ls: 네트워크 목록 확인
4. docker volume ls: 볼륨 목록 확인
