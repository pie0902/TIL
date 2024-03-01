# CORS


CORS(Cross-Origin Resource Sharing)은 웹 브라우저에서 다른 도메인 간의 리소스 요청을 제어하는 보안 기능이다. 기본적으로, 브라우저는 다른 도메인의 리소스에 대한 요청을 차단하지만, CORS를 통해 특정 도메인에서의 요청을 허용할 수 있다.

JAVA에서 CORS를 구현하려면 config 파일을 만들어서 전역 CORS를 설정하거나 특정 컨트롤러에 대해 어노테이션을 사용하여 CORS를 설정 할 수 있다.

1. 전역 CORS

```Java


@Configuration
public class WebConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowCredentials(true); // 크로스 오리진 요청 시 쿠키를 포함시키기 위해 true로 설정
        configuration.addAllowedOrigin("http://localhost:3000"); // 개발 중인 로컬 호스트의 프론트엔드 주소
        configuration.addAllowedOrigin("http://localhost:3001"); // 필요한 경우 다른 로컬 개발 주소도 추가
        configuration.addAllowedOrigin("http:커스텀 도메인"); // 프로덕션 환경 도메인 추가
        configuration.addAllowedOrigin("https://커스텀 도메인); // HTTPS를 사용하는 경우 추가
        configuration.addAllowedHeader("*"); // 모든 헤더 허용
        configuration.addAllowedMethod("*"); // 모든 HTTP 메소드 허용
        configuration.addExposedHeader("Authorization"); // Authorization 헤더 노출

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    @Bean
    public CorsFilter corsFilter() {
        return new CorsFilter(corsConfigurationSource());
    }
}

```
2. 특정 컨트롤러에 대한 CORS 설정
```Java
@RestController
public class MyController {

    @CrossOrigin(origins = "http://example.com")
    @GetMapping("/example")
    public String example() {
        return "Hello World";
    }
}

```
