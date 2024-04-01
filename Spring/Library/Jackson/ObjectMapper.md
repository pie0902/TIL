# 1.오브젝트 매퍼란?
> * 오브젝트 매퍼(Object Mapper)는 데이터를 하나의 포맷에서 다른 포맷으로 변환하는 도구 또는 라이브러리를 의미한다.
> * 특히, 프로그래밍에서는 자주 JSON, XML 같은 데이터 포맷을 자바 객체로 변환하거나 그 반대로 변환할 때 사용된다.
> * 가장 일반적인 사용 사례는 JSON 데이터를 자바 객체로 변환(역직렬화)하고, 자바 객체를 JSON으로 변환(직렬화)하는 과정이다. 
> * 이 과정은 API 통신, 데이터 저장, 설정 파일 읽기 등 다양한 상황에서 필요하다. 
## 2.사용법
### 오브젝트 매퍼의 기본 사용법은 대체로 다음과 같다.
* #### 직렬화: 자바 객체를 JSON 문자열로 변환하는 과
* #### 역직렬화: JSON 문자열을 자바 객체로 변환하는 과정.
> * 자바에서 JSON을 처리하는데 널리 사용되는 라이브러리로는 Jackson과 Gson이 있다.
> * 여기서는 Jackson을 예로 들어보며 학습을 해보겠다.
## Jackson 사용법:
1. #### 의존성 추가
> * implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.0'
2. #### ObjectMapper 인스턴스 생성: 데이터 변환 작업을 수행할 ObjectMapper 인스턴스를 생성한다.
```java
ObjectMapper objectMapper = new ObjectMapper();
```
3. ### 직렬화: writeValueAsString() 메소드를 사용하여 자바 객체를 JSON 문자열로 변환한다.
```java
MyObject myObject = new MyObject();
String jsonString = objectMapper.writeValueAsString(myObject);
```
4. ### 역직렬화: readValue() //메소드를 사용하여 JSON 문자열을 자바 객체로 변환한다
```java
MyObject myObject = objectMapper.readValue(jsonString, MyObject.class);
```
## 3.예제
* 자바에서 사용자(User) 객체를 JSON으로 변환하고, JSON 문자열을 다시 사용자 객체로 변환하는 간단한 예제

User 클래스:
```jave
java
Copy code
public class User {
private String name;
private int age;
}
```
* 직렬화 및 역직렬화:
```java
import com.fasterxml.jackson.databind.ObjectMapper;

public class ObjectMapperExample {
public static void main(String[] args) throws Exception {
ObjectMapper objectMapper = new ObjectMapper();

        // User 객체 생성
        User user = new User();
        user.setName("John Doe");
        user.setAge(30);

        // User 객체를 JSON 문자열로 직렬화
        String userJson = objectMapper.writeValueAsString(user);
        System.out.println("Serialized JSON: " + userJson);

        // JSON 문자열을 User 객체로 역직렬화
        User userDeserialized = objectMapper.readValue(userJson, User.class);
        System.out.println("Deserialized user: " + userDeserialized.getName() + ", Age: " + userDeserialized.getAge());
    }
}
```
* 이 예제에서는 ObjectMapper를 사용하여 User 객체를 JSON 문자열로 직렬화하고, 그 JSON 문자열을 다시 User 객체로 역직렬화하는 과정을 보여준다.이런 방식으로, 복잡한 객체 구조도 쉽게 JSON 형태로 변환하거나 JSON 데이터를 객체로 변환할 수 있다

### 테스트 코드
- 코드<br>
![스크린샷 2024-04-01 오전 1 02 09](https://github.com/pie0902/TIL/assets/47919911/1b9f5a1f-7341-4215-a8cd-ffdb7c110885)
- 결과<br>
![스크린샷 2024-04-01 오전 1 18 59](https://github.com/pie0902/TIL/assets/47919911/2f9bf4c0-3159-4738-8623-7365df9835ec)









