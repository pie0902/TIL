# IoC(Inversion of Control)와 DI(Dependency Injection)
### IOC(Inversion of Control)
* IoC(제어의 역전)는 프로그램의 제어 흐름을 사용자 코드가 아닌 프레임워크가 관리하는 개념이다. 이를 통해 결합도는 낮아지고, 유연성 및 확장성이 향상된다.
### DI(Dependency Injection)
* DI(의존성 주입)는 객체 간의 의존 관계를 외부에서 설정하여, 각 객체가 필요로 하는 의존성을 자동으로 제공하는 기법이다. 이 과정은 코드의 재사용성을 높이고, 유지보수를 용이하게 한다.

### IoC와 DI의 관계
* IoC는 프로그램의 제어 흐름을 외부에 맡기는 원리이며, DI는 이 원리를 구현하는 한 방법으로, 객체 간 의존성을 외부에서 주입한다. 두 개념은 서로 밀접하게 연관되어 있어, DI를 통해 IoC의 이점을 실현한다.
## 예시)
```
// 서비스 인터페이스
public interface MessageService {
    String getMessage();
}

// 서비스 인터페이스 구현체
@Component
public class EmailService implements MessageService {
    @Override
    public String getMessage() {
        return "Hello, this is an email message!";
    }
}

@Controller
public class MessageController {
    private final MessageService messageService;

    @Autowired
    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    @GetMapping("/message")
    public String showMessage(Model model) {
        // 모델에 메시지 추가
        model.addAttribute("message", messageService.getMessage());
        // 뷰 이름 반환
        return "messageView"; // messageView.html과 같은 뷰 파일을 찾아서 사용자에게 보여줌
    }
}
```
* 이 과정에서 의존성 주입(DI)이 사용되어 MessageService의 구현체가 MessageController에 자동으로 주입된다.

**P.S 그냥 Spring아 너가 대신 해줘! 인 것 같다.**
