# REST API
REST API(Representational State Transfer Application Programming Interface)
## REST란?
* REST는 웹의 기본 프로토콜인 HTTP를 효과적으로 활용하여 애플리케이션 간에 정보를 교환하기 위한 아키텍처 스타일이다.
* 웹에서 자원(Resource)는 URL로 식별된다.
> ex)</br>
http://rest-api/post</br>
> 모든 것을 명사로 표현하고 세부 Resource에는 id를 붙인다.
* 자원의 상태는 JSON이나 XML 같은 형식으로 전달된다.
* 요청 메시지가 자신을 어떻게 처리해야 할지 충분한 정보를 포함해야 한다.(자기 서술적 메세지)
* 각 요청은 독립적이며, 이전 요청의 정보를 기반으로 하지 않는다.(애플리케이션 상태의 전이)
## API란?
* API는 소프트웨어 또는 애플리케이션 간의 상호작용을 가능하게 하는 규약이나 정의의 집합이다.
* API를 통해 개발자는 기존의 코드나 서비스를 재사용하여 효율적으로 새로운 애플리케이션을 개발하고, 다양한 서비스 간에 데이터를 교환하며 통합할 수 있다.

### **REST API는 이러한 원칙들을 따르면서, 웹에서 자원의 상태 정보를 쉽고 효율적으로 교환할 수 있도록 설계된 API의 한 형태이다.**

### Method
| Method  | 의미     | Idempotent |
|---------|--------|------------|
| POST    | Create | No         |
| GET     | Read   | Yes        |
| PUT     | Update | Yes        |
| DELETE  | Delete | Yes        |
###### 웹 서비스와 API에서의 Idempotent(멱등성)
* 요청을 여러 번 보내더라도 그 결과가 최초의 한 번 요청한 결과와 동일하게 유지되어야 한다는 원칙
