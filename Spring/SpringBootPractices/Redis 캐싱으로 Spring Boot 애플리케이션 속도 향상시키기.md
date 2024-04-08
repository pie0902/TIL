# Redis 캐싱으로 Spring Boot 애플리케이션 속도 향상시키기
## Redis란?
```
                _._
           _.-``__ ''-._                Redis란 오픈 소스 인메모리 데이터 구조 저장소로,
      _.-``    `.  `_.  ''-._           다양한 데이터 구조를 지원하는 key-value 스토어 이다.
  .-`` .-```.  ```\/    _.,_ ''-._      주로 캐시, 세션 관리, 실시간 분석, 메시징 등의 용도로 사용된다.
 (    '      ,       .-`  | `,    )     
 |`-._`-...-` __...-.``-._|'` _.-'|       
 |    `-._   `._    /     _.-'    |      
  `-._    `-._  `-./  _.-'    _.-'      
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |           
  `-._    `-._`-.__.-'_.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |     Redis 7.2.4 (00000000/0) 64 bit
  `-._    `-._`-.__.-'_.-'    _.-'      Running in standalone mode
      `-._    `-.__.-'    _.-'          https://redis.io
          `-._        _.-'
              `-.__.-'
```

## Redis를 사용하여 데이터를 조회하는 이유

### Redis 사용 이유
- 빠른 읽기/쓰기 성능: Redis는 인메모리 데이터 저장소로, 디스크 기반의 데이터베이스에 비해 매우 빠른 읽기/쓰기 성능을 제공한다.
### 장점
- 빠른 응답 속도: 인메모리 저장소로서 Redis는 빠른 읽기/쓰기 성능을 제공하여 애플리케이션의 응답 속도를 크게 향상시킬 수 있다.
### 단점
- 메모리 사용량: Redis는 모든 데이터를 메모리에 저장하므로 대용량 데이터를 다룰 때는 메모리 사용량이 높아질 수 있다.
- 데이터 일관성: Redis는 단일 스레드로 동작하므로 다중 클라이언트에서 동시에 데이터를 수정할 때 데이터 일관성 문제가 발생할 수 있다.
### 단점 해결책
- Redis의 메모리 사용을 최적화하려면 만료 시간 설정으로 불필요한 데이터를 정리하고, maxmemory 설정으로 메모리 한도를 정하며, 데이터 샤딩을 통해, 단일 서버에 집중되는 부하를 여러 서버로 나누어 분산시킬 수 있다.

## Redis 사용 과정 정리
1. build.gradle에 의존성을 추가해준다.
2. StringRedisTemplate을 bean으로 등록한다.
3. ObjectMapper 인스턴스를 사용하여 Java 객체와 JSON 문자열 간의 변환을 처리한다.
4. 게시글 Id를 기반으로 Redis에서 게시글 데이터를 조회한다. 
   * Redis에 데이터가 존재하면, 해당 데이터를 객체로 역직렬화하여 반환한다.
   * Redis에 데이터가 없다면, 데이터베이스에서 게시글을 조회하고 조회된 게시글 정보를 캐싱한다.
        * 이 과정에서 게시글 객체는 JSON 문자열로 직렬화되어 Redis에 저장된다. 


## 실습
### Post Entity(Test 목적으로 @Setter 어노테이션을 사용했다.)
```java
@Entity
@Getter
@Setter
@EntityListeners(AuditingEntityListener.class)
@NoArgsConstructor
public class Post {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;
    private String content;
    @CreatedDate
    private LocalDateTime createdAt;

    public Post(PostRequest postRequest){
        this.title = postRequest.getTitle();
        this.content = postRequest.getContent();
    }
}

```
### Post Service
```java
    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    
    public PostResponse getPost(Long id) {
        //Redis에서 사용할 키 값
        String postKey = "post: " + id;
        //Postkey키를 키로 사용하여 Redis에서 JSON 형태의 게시글 데이터를 저장한다.
        String postJson = stringRedisTemplate.opsForValue().get(postKey);
        // ObjectMapper 인스턴스를 생성한다. JSON과 Java 객체 간의 변환을 처리한다.
        ObjectMapper objectMapper = new ObjectMapper();
        // Java 8 날짜와 시간 API를 올바르게 처리하기 위해 JavaTimeModule을 등록한다.
        objectMapper.registerModule(new JavaTimeModule());
        //postkey로 조회시 데이터가 있다면
        if(postJson != null) {
            //레디스에서 데이터를 찾으면
            try{
                //postJson 문자열을 post 객체로 역직렬화 한다.
                Post post = objectMapper.readValue(postJson, Post.class);
                System.out.println("데이터가 존재 합니다 : " + postKey);
                return new PostResponse(post);
            } catch (JsonProcessingException e){
                e.printStackTrace();
                throw new RuntimeException("레디스에서 역직렬화에 실패했습니다.",e);
            }
        } else {
            //레디스에서 데이터를 못 찾으면
            Post post = postRepository.findById(id).orElseThrow(()-> new RuntimeException("게시글을 찾을수 없습니다."));
            //조회한 데이터를 레디스에 저장
            try{
                //post 객체를 JSON 문자열로 직렬화 한다.
                String serializedPost = objectMapper.writeValueAsString(post);
                //key값에는 postkey 대응하는 값에는 serializedPost를 저장한다.
                stringRedisTemplate.opsForValue().set(postKey,serializedPost);
                System.out.println("데이터를 레디스에 저장 합니다. : " + postKey);
            }catch (JsonProcessingException e){
                throw new RuntimeException("레디스에서 직렬화에 실패 했습니다.",e);
            }
            return new PostResponse(post);
        }
    }
```

## 개발 중 직면한 문제점
- Postman으로 데이터를 조회하는데 오류가 생겼다.
<img src="https://github.com/pie0902/TIL/assets/47919911/4fe42446-c3eb-45d8-93b2-6590a542a462" height="100">

- 오류의 원인 :
    1. Post 엔티티에는 createdAt이라는 필드가 있다. 이 필드는 게시글의 생성 시간을 기록하는 데 사용되며, LocalDateTime 타입으로 선언되어 있다.
    2. ObjectMapper가 LocalDateTime 타입을 올바르게 처리하지 못해, 직렬화 시 예상치 못한 형식으로 변환되거나, 역직렬화 과정에서 오류가 발생할 수 있다.
- 해결 방법 :
    ### 1. **jackson-datatype-jsr310 모듈 의존성 추가**
    ```java
    implementation 'com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.15.4'
    ```
    * 이 모듈을 통해 Java 8의 LocalDateTime, LocalDate, ZonedDateTime 같은 날짜/시간 타입들을 JSON으로 직렬화하거나 JSON에서 이러한 타입으로 역직렬화할 수 있다.
    ### 2. **JavaTimeModule 등록**
   ```
   objectMapper.registerModule(new JavaTimeModule());
   ```
   * 날짜/시간 타입을 JSON으로 직렬화하거나 JSON에서 이러한 타입으로 역직렬화하기 위해서는 JavaTimeModule을 등록해야 한다. 
    
## 결과

![스크린샷 2024-04-01 오후 3 58 35](https://github.com/pie0902/TIL/assets/47919911/490af480-e9de-4b98-bcb5-c6ed5180ef1c)

- 처음 게시글을 조회하면 Redis에 데이터를 저장한다. "데이터를 레디스에 저장 합니다. :"를 출력한다.
- 두번째 조회부터는 레디스에서 데이터를 가져온다. "데이터가 존재 합니다 : "를 출력한다.

![스크린샷 2024-04-01 오후 3 58 52](https://github.com/pie0902/TIL/assets/47919911/37d59d90-7935-4e2f-97da-96bd048d94ce)

Postman에서 GET 메서드로 테스트한 결과 정상적으로 동작한다.
