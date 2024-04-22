
# 동시성 제어에서 주문 취소 통보: Amazon SES를 활용한 메일 전송 전략

## Amazon SimpleEmailService란?

AWS Simple Email Service (SES)는 아마존 웹 서비스(AWS)가 제공하는 확장 가능한 이메일 전송 서비스다. 이 서비스는 기업이 마케팅, 알림, 트랜잭션 이메일을 손쉽게 보낼 수 있도록 설계되었다. AWS SES는 높은 전달성, 강력한 인증 기능, 그리고 광범위한 모니터링으로 이메일 관리의 복잡성을 감소시켜 준다.
## 주요 기능
1. 이메일 전송: AWS SES를 사용하면 HTML 또는 일반 텍스트 포맷의 이메일을 전송할 수 있다. 이메일은 개별적으로 또는 대량으로 전송할 수 있다.
2. 이메일 수신: SES는 이메일 수신 기능도 제공한다. 이를 통해 사용자는 SES를 이용해 이메일을 받고, 해당 이메일에 대한 처리 작업을 자동으로 수행할 수 있다.
3. 유연한 이메일 처리: 이메일을 보내고 받는 과정에서 다양한 SNS 토픽(Simple Notification Service)으로 알림을 설정하거나, Lambda 함수를 통해 이메일 내용을 처리하고 분석할 수 있다.
4. SPAM 및 바이러스 필터링: AWS SES는 보내는 이메일에 대해 자동으로 스팸 및 바이러스 필터링을 수행하여, 이메일이 수신자의 정크 폴더로 분류되는 것을 최소화한다.

>**사용법은 따로 작성하지 않아도 될 정도로 쉽다**

## 동시성 제어에서 주문 취소 통보를 할 때 고려해야 할 상황

| 상품명 | 수량   |
| --- | ---- |
| 음료수 | 100개 |

예시)200명의 유저가 동시에 음료수를 1개씩 주문한 상황
1. 100명의 유저는 주문에 성공함
2. 100명의 유저는 주문에 실패함 -> 100명한테 재고가 부족하다고 메일 보냄

이후 상황)
1. 100명의 성공 유저중에서 50명이 결제를 하고 50명은 5분동안 결제를 안해서 취소됨
2. 50명의 유저는 상태가 "결제완료"로 변경
3. 50명의 유저는 상태가 "주문취소"로 변경 -> 50명한테 5분동안 주문을 안해서 취소 됐다고 메일 보냄

| 상품명 | 수량  |
| --- | --- |
| 음료수 | 50개 |

그렇다면 나머지 100명한테 재고가 업데이트 됐다고 메일을 보내야함.
주문은 선착순이라는 것을 공지해야함
## 정리

### 주문 처리 및 알림 흐름

1. **주문 초기 처리**:
   - 200명의 유저가 동시에 음료수를 1개씩 주문한다.
   - 시스템은 분산락을 사용하여 재고를 관리한다.
   - 100명의 유저는 주문에 성공하고, 나머지 100명은 재고 부족으로 주문에 실패한다.
   - 실패한 100명에게는 "재고 부족으로 주문이 실패했다"는 내용의 메일을 발송한다.
2. **결제 처리 및 주문 최종화**:
   - 성공적으로 주문한 100명 중 50명이 결제를 완료한다. 이들의 주문 상태는 "결제완료"로 변경된다.
   - 나머지 50명은 5분 동안 결제를 완료하지 않아 자동으로 주문이 취소된다. 이들의 주문 상태는 "주문취소"로 변경되며, "5분 내에 결제가 완료되지 않아 주문이 취소되었다"는 내용의 메일을 발송한다.
   - 주문 취소로 인해 재고는 다시 50개로 업데이트 된다.
3. **재고 업데이트 알림**:
   - 재고가 부족해서 주문이 취소된 유저의 ID와 상품 ID를 레디스에 24시간 동안 저장을 한다.
   - 재고가 업데이트되면 업데이트된 사실을 이전에 실패했던 100명의 유저를 레디스에서 조회해서, "재고가 업데이트되었으니 주문이 가능합니다"라는 내용의 메일을 발송한다. 이 메일은 재고가 다시 빨리 소진될 수 있으므로 선착순으로 주문하라는 내용도 포함할 수 있다.
## 해결책
### 구현 예시
![스크린샷 2024-04-22 오후 9 18 10](https://github.com/pie0902/TIL/assets/47919911/66ed888a-ce24-4727-a2f6-b6650c0d7457)

1. **상태 정의**:
   - `NOTPAYED`: 주문이 생성되었으나 아직 결제가 이루어지지 않은 상태.
   - `PREPARING`: 결제가 완료되어 주문 준비 중인 상태.
   - `SHIPPING`: 상품이 배송 중인 상태.
   - `DELIVERED`: 상품이 배송 완료된 상태.
   - `CANCELLED`: 다른 원인으로 인한 일반적인 주문 취소 상태.
3. **상태 전환 로직**:
   - 주문 시 `NOTPAYED` 상태로 설정.
   - 5분 내 결제 시 `PREPARING` 상태로 전환.
   - 5분 내에 결제가 이루어지지 않을 경우 `CANCELLED` 상태로 전환 후 주문 취소 메일 발송
   - 재고 부족으로 주문을 받을 수 없는 경우 `CANCELLED` 상태로 전환 후 재고 수량 부족 메일 발송
   - 재고가 업데이트 되면 재고 부족으로 주문 못한 사람들에게 재고 업데이트 메일 발송.
## 코드
### Amazon ses를 사용하기 위한 config 생성
```java
@Configuration
public class AwsSesConfig {

   @Value("${aws.access.key}")
   private String accessKey;

   @Value("${aws.secret.key}")
   private String secretKey;

   @Bean
   public SesClient sesClient() {
      AwsBasicCredentials awsCreds = AwsBasicCredentials.create(accessKey, secretKey);
      return SesClient.builder()
              .credentialsProvider(StaticCredentialsProvider.create(awsCreds))
              .region(Region.of("ap-northeast-2"))
              .build();
   }
}
```
### EmailService 클래스 생성
```java
@Service
@RequiredArgsConstructor
public class EmailService {
    private final SesClient sesClient;
    private final RedissonClient redissonClient;

    public enum EmailType {
        STOCK_OUT,
        PAYMENT_TIMEOUT,
        STOCK_UPDATE
    }

    public void sendCancellationEmail(
        String recipientEmail,
        String orderDetails,
        EmailType emailType
    ) {
        //이메일 보내는 사람의 주소
        String sender = "발신자 이메일"; // 검증된 발신자 이메일
        String htmlBody;
        String subject;
        // 상황에 따른 이메일 폼
        switch (emailType) {
            case STOCK_OUT:
                htmlBody = buildStockOutCancellationHtml(orderDetails);
                subject = "주문 취소 안내";
                break;
            case PAYMENT_TIMEOUT:
                htmlBody = buildPaymentTimeoutCancellationHtml(orderDetails);
                subject = "결제 시간 초과로 인한 주문 취소";
                break;
            case STOCK_UPDATE:
                htmlBody = buildStockUpdateHtml(orderDetails);
                subject = "재고 업데이트 알림";
                break;
            default:
                throw new IllegalArgumentException("Unknown email type");
        }
        //이메일 요청 객체 빌더 초기화
        SendEmailRequest request = SendEmailRequest.builder()
            //이메일 수신자 설정
            .destination(Destination.builder().toAddresses(recipientEmail).build())
            //이메일 내용 구성
            .message(Message.builder()
                //이메일 제목 생성
                .subject(Content.builder().data(subject).build())
                //이메일 내용 구성
                .body(Body.builder().text(Content.builder().data(htmlBody).build()).build())
                //Massage 객체 빌드 완료
                .build())
            //발송자 설정 완료
            .source(sender)
            //sandMailRequest 빌드 완료
            .build();
        //SES 클라이언트를 통해 이메일 전송
        sesClient.sendEmail(request);
        //이메일 전송 성공 로그 출력
        System.out.println("Cancellation email sent to " + recipientEmail);
    }
    //이메일 템플릿 1) 재고가 부족할 경우
    private String buildStockOutCancellationHtml(String productDetails) {
       return "안녕하세요 10-trillon-dollars 입니다. 주문 상품" + orderDetails +
               "의 재고가 부족해서 주문이 취소 되었습니다.\n재고가 추가되면 메일을 발송해드립니다.";
    }
    //이메일 템플릿 2) 결제를 5분동안 안해서 주문이 취소된 경우
    private String buildPaymentTimeoutCancellationHtml(String productDetails) {
        return "안녕하세요 10-trillon-dollars 입니다. 주문 상품" + orderDetails +
            "의 주문이 취소 되었습니다.\n지정된 기간 내에 결제가 이루어지지 않아 주문이 취소되었습니다.";
    }
    //이메일 템플릿 3) 재고가 업데이트 될 경우
    private String buildStockUpdateHtml(String productDetails) {
       return "안녕하세요 10-trillon-dollars 입니다. 주문 상품" + orderDetails +
               "의 재고가 업데이트 되었습니다..\n주문은 선착순으로 이루어 집니다.";
    }
    //재고 부족으로 인한 주문 취소 고객 저장 메서드 (레디스 사용)
    public void saveStock_Out_UserInfoToRedis(String email, Long productId) {
        String key = "stockOut:" + productId;
        //재고 업데이트를 받을 사용자 이메일 저장
        redissonClient.getList(key).add(email);
        //재고 업데이트 알림 유지 기간 설정, 24시간
        redissonClient.getBucket(key).expire(10, TimeUnit.MINUTES);
    }

    //재고 업데이트 시 레디스 조회 및 이메일 전송
    public void nofityStockUpdate(Long productId,String productName) {
        // 레디스 키 생성
        String key = "stockOut:" + productId;
        // 레디스에서 이 키에 해당하는 메일 리스트를 가져옴
        RList<String> emails = redissonClient.getList(key);
        if (!emails.isEmpty()) {
            String productDetails = productName;
            for (String email : emails) {
                sendCancellationEmail(email, productDetails, EmailType.STOCK_UPDATE);
            }
            redissonClient.getKeys().delete(key);
        } else {
            System.out.println("해당되는 상품이 없습니다" + productId);
        }
    }

    @PreDestroy
    public void close() {
        if (sesClient != null) {
            sesClient.close();
            System.out.println("SES Client has been closed.");
        }
    }
}

```
