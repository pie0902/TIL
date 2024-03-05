# Spring MVC 개념 정리
### Intro
MVC패턴은 사용자 인터페이스를 구현하는 데 널리 사용되는 디자인 패턴이다.<br>
MVC패턴은 어플리케이션을 세 가지 주요 구성 요소인 Model,View,Controller로 분리하여 관리한다.
## MVC란?
MVC는 Model-View-Controller의 약자로, 애플리케이션의 데이터 처리(Model), 사용자 인터페이스(View), 그리고 입력 처리(Controller)를 분리하여 애플리케이션의 유연성과 확장성을 높인다.
### Model
* Model은 애플리케이션의 데이터와 비즈니스 로직을 처리한다.사용자의 요청에 대한 응답으로 데이터를 저장하고 검색하는 메소드를 포함한다.
### View
* View는 사용자에게 보여지는 UI요소이다. Model로부터 데이터를 받아 사용자에게 그래픽 형태로 표시한다.
### Controller
* Controller는 사용자의 입력을 받고 처리하는 컴포넌트다. 사용자의 액션에 따라 Model을 업데이트하고,변경된 상태를 View에 반영하도록 요청한다.(Model과 View의 중간에서 상호작용을 해주는 역할을 한다.)
# Spring MVC 구조
## DispatcherServlet
* DispatcherServlet은 웹 애플리케이션에서 들어오는 모든 요청을 처음으로 받아서 처리하는 프론트 컨트롤러 패턴의 구현체이다.
### 주요 역할과 특징
* 웹 애플리케이션으로 들어오는 모든 요청을 하나의 서블릿인 DispatcherServlet이 받아들여, 요청에 맞는 처리기(Controller)에게 전달한다. 이를 통해 애플리케이션의 요청 처리 로직이 하나의 진입점을 통해 관리된다.
* DispatcherServlet은 요청 URL을 분석하여 해당 요청을 처리할 적절한 컨트롤러를 찾는 역할을 한다. 이는 HandlerMapping을 통해 이루어진다.
* 컨트롤러가 처리 로직을 수행한 후, DispatcherServlet은 처리 결과를 나타내는 모델 데이터와 이를 표현할 뷰를 연결한다. 뷰를 결정하는 과정은 ViewResolver에 의해 수행된다.
* 다양한 뷰 기술 지원: DispatcherServlet은 JSP, Thymeleaf, FreeMarker 등 다양한 뷰 기술을 지원하여, 동적인 웹 페이지를 생성할 수 있다.
* 스프링 MVC 애플리케이션에서 DispatcherServlet은 web.xml이나 스프링 부트의 자동 설정을 통해 구성된다. 스프링 부트를 사용하는 경우, 별도의 설정 없이도 DispatcherServlet이 자동으로 등록되고 구성되어 개발자가 웹 애플리케이션을 보다 쉽게 개발할 수 있도록 도와준다.
## Spring MVC에서의 요청 처리 순서
1. DispatcherServlet이 클라이언트로부터의 모든 웹 요청을 처음으로 받는다.
2. DispatcherServlet은 HandlerMapping을 사용하여 요청 URL을 처리할 컨트롤러를 찾는다.
3. 찾아진 컨트롤러의 메소드가 호출되어 요청을 처리한다. 이 과정에서 비즈니스 로직이 실행되고, 모델 객체가 생성 및 수정될 수 있다.
4. 컨트롤러는 처리 결과와 함께 뷰 이름을 포함한 ModelAndView 객체를 DispatcherServlet에 반환된다.
5. DispatcherServlet은 반환된 뷰 이름을 ViewResolver에 전달하여 실제 뷰 객체를 찾는다.
6. 뷰 객체는 모델 데이터를 사용하여 최종적인 클라이언트 응답을 생성한다.
7. 생성된 응답이 클라이언트에게 전송된다.

**DispatcherServlet은 이 모든 과정의 중심에 있으며, 스프링 MVC의 작동 원리를 이해하는 데 핵심적인 역할을 한다.**
