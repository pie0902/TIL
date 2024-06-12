테스트 코드는 중요하다. 하지만 어렵게 느껴질 수 있다. 좀 더 쉽게 생각하고 접근할 필요가 있다. 예를 들어, `Add`라는 클래스에 `addNumber`라는 함수가 있다고 가정해 보자.


```java
public class Add{
	public int addNumber(int a, int b){
        return a+b;
    }
}
```
위 코드에 대해 테스트 코드를 작성하는 것은
- addNumber 함수의 매개변수에 int a와 int b를 넣고 a,b 값을 더한 값이 올바르게 반환되는지를 확인한다
```java
@Test
@DisplayName("더하기 기능")
void add_test(){
	//given
	int a = 1;
	int b = 2;
	Add add = new Add();

	//when
	int num = add.addNumber(a,b);

	//then
	assertThat(num).isEqualTo(3);
	
}
```
반환된 값이 예상한 결과 값이 같은지 검증만 하면 된다.

하지만 서비스 로직이나 컨트롤러를 테스트할 때는 너무 복잡하게 느껴질 수 있다. 예를 들어, `PostService` 클래스에 `createPost`라는 함수를 테스트할 때, 어떤 값을 넣고, 어떤 것을 실행하며, 어떤 결과를 검증할지에 대해 헷갈릴 수 있다. 아주 간단하게 코드를 작성해보겠다.

java

코드 복사

```Java
@Service 
public class PostService {
	private PostRepository postRepository;
    
	public PostService(PostRepository postRepository) {
	    this.postRepository = postRepository;     
	}      
    
	public PostResponse createPost(PostRequest postRequest) {
		Post post = new Post(postRequest.getTitle(), postRequest.getContent());          
                postRepository.save(post);                                                       
                return new PostResponse(post.getTitle(), post.getContent());     
	}
}
```

위 코드를 테스트 코드로 작성할 때도, 더하기 테스트 코드처럼 순서를 정하고 반환되는 값을 검증하면 된다.

#### Given

1. Mock 객체를 사용해서 `PostRepository`를 주입 받는다.
2. Inject를 사용해서 `PostService`를 주입 받는다.
3. `PostRequest`를 준비한다.

#### When

1. `postService`의 `createPost` 함수를 실행시켜서 `postResponse`를 생성한다.

#### Then

1. `post` 객체와 `postResponse`의 값이 일치하는지 검증한다.
2. `postRepository`의 `save`가 한 번 실행됐는지 검증한다.

```java
@InjectMocks 
private PostService postService;  
@Mock 
private PostRepository postRepository;
@Test 
@DisplayName("포스트 생성 테스트") 
void createPost_test() {     
	// given
    PostRequest postReq = new PostRequest("title", "content");      
	// when
    PostResponse postResponse = postService.createPost(postReq);      
	// then
    assertEquals(postResponse.getTitle(), postReq.getTitle());                       
    assertEquals(postResponse.getContent(), postReq.getContent());                   
    verify(postRepository, times(1)).save(any(Post.class)); 
}

```
이렇게 정리하고 작성하면 테스트 코드를 조금은 쉽게 접근할 수 있다고 생각이 든다.
