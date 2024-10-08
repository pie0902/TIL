# SQL 함수

### 문자형 함수
1. LOWER: 문자열을 소문자로
2. UPPER: 문자열을 대문자로
3. SUBSTR: 대상에서 찾을 문자열 위치 변환
4. LTRIM: 문자열 중 특정 문자열을 왼쪽에서 삭제
5. RTRIM: 문자열 중 특저 문자열을 오른쪽에서 삭제
6. TRIM: 문자열 중 특저 문자열을 양쪽에서 삭제
7. LPAD: 대상 왼쪽에 문자열을 추가하여 총 n의 길이 리턴
8. RPAD: 대상 오른쪽에 문자열을 추가하여 총 n의 길이 리턴
9. CONTACT: 문자열 결합
10. LENGTH: 문자열 길이
11. REPLACE: 문자열 치환 및 삭제
12. TRANSLATE: 글자를 1대1로 치환

### 숫자함수
1. ABS: 절대값 반환
2. ROUND: 소수점 특정 자리에서 반올림
3. TRUNC: 소수점 특정 자리에서 버림
4. SIGN: 숫자가 양수면 1 음수면 -1 0이면 0 반혼
5. FLOOR: 작거나 같은 최대 정수 리턴
6. CEIL: 크거나 같은 최소 정수 리턴
7. MOD: 숫자1을 숫자2로 나누어 나머지 반환
8. POWER: m의 n 거듭제곱
9. SQRT: 루트값 리턴

### 변환함수
1. TO_NUMBER: 숫자 타입으로 변경하여 리턴
2. TO_CHAR: 날짜의 포맷 변경/숫자의 포맷변경
3. TO_DATE: 주어진 문자를 포맷 형식에 맞게 읽어 날짜로 리턴
4. FORMAT: 날짜의 포맷 변경
5. CAST: 대상을 주어진 데이터타입으로 변환


### 그룹함수
1. COUNT: 행의 수 리턴
2. SUM: 총 합 리턴
3. AVG: 평균 리턴
4. MIN: 최솟값 리턴
5. MAX: 최댓값 리턴
6. VARIANCE: 분산 리턴
7. STDDEV: 표준편차 리턴

### 일반함수
1. DECODE: 대상의 값이 1이면 리턴 1, 값2와 같으면 리턴2, 그외에는 그외리턴값 리턴
2. NVL: 대상이 널이면 치환값으로 치환하여 리턴
3. NVL2: 대상이 널이면 치환값 로 치환 널이 아니면 1로 치환하여 리턴
4. COALESCE: 대상들 중 널이 아닌 값 출력
5. ISNULL: 대상이 널이면 치환값 리턴
6. NULLIF: 두 값이 같으면 널 리턴, 다르면 1 리턴
7. CASE: 조건별 치환 및 연산 수행
