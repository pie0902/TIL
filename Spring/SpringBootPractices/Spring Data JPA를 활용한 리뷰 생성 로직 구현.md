# Spring Data JPA를 활용한 리뷰 생성 로직 구현
## 리뷰 생성 조건
### 클라이언트가 주문한 횟수 만큼 리뷰 작성 제한
- 사용자는 특정 상품을 주문한 횟수와 동일한 수의 리뷰만 작성할 수 있다.

### 구현 방법
1. **주문 횟수 조회**
    - 사용자 ID와 상품 ID를 기준으로 해당 사용자의 특정 상품에 대한 주문 횟수를 조회한다.
      ```java
      long orderCount = orderDetailRepository.countByUserIdAndProductId(userId, productId);
      ```
    - `OrderDetailRepository`에서 사용자 ID와 상품 ID로 주문 횟수를 조회하는 메서드를 정의한다.
      ```java
      @Query("SELECT COUNT(od) FROM OrderDetail od WHERE od.order.user.id = :userId AND od.productId = :productId")
      long countByUserIdAndProductId(@Param("userId") Long userId, @Param("productId") Long productId);
      ```
      1. OrderDetail 엔티티에서 order 필드를 통해 연관된 Order 엔티티의 user.id가 전달받은 userId와 일치하는 레코드를 조회한다.
         * od.order.user.id = :userId: OrderDetail 엔티티의 order 필드를 통해 Order 엔티티의 user 필드에 접근하여 id가 userId와 일치하는지 확인한다.
      2. OrderDetail 엔티티의 productId 필드가 전달받은 productId와 일치하는 레코드를 조회한다.
         * od.productId = :productId: OrderDetail 엔티티의 productId 필드가 productId와 일치하는지 확인한다.
      3. 위의 두 조건을 모두 만족하는 OrderDetail 레코드의 개수를 조회한다.
         * SELECT COUNT(od): 조회된 OrderDetail 레코드의 개수를 반환한다.

2. **리뷰 개수 조회**
    - 사용자 ID와 상품 ID를 기준으로 해당 사용자가 특정 상품에 대해 작성한 리뷰 개수를 조회한다.
      ```java
      long reviewCount = reviewRepository.countByUserIdAndProductId(userId, productId);
      ```

3. **리뷰 작성 가능 여부 판단**
    - 주문 횟수와 리뷰 개수를 비교하여 리뷰 작성 가능 여부를 판단한다.
    - `canUserReviewProduct` 메서드를 정의하여 주문 횟수와 리뷰 개수를 비교한다.
      ```java
      private boolean canUserReviewProduct(Long userId, Long productId) {
          long orderCount = orderDetailRepository.countByUserIdAndProductId(userId, productId);
          long reviewCount = reviewRepository.countByUserIdAndProductId(userId, productId);
          return orderCount > reviewCount;
      }
      ```
    - 주문 횟수(`orderCount`)가 리뷰 개수(`reviewCount`)보다 크면 `true`를 반환하여 리뷰 작성이 가능함을 나타낸다.
    - 주문 횟수가 리뷰 개수보다 작거나 같으면 `false`를 반환하여 리뷰 작성이 불가능함을 나타낸다.

### review Table
| 컬럼명      | 데이터 타입 | 제약 조건                         | 설명                        |
|-------------|------------|-----------------------------------|----------------------------|
| id          | BIGINT     | PRIMARY KEY, AUTO_INCREMENT       | 리뷰 ID                    |
| content     | VARCHAR    |                                   | 리뷰 내용                   |
| photo       | VARCHAR    |                                   | 리뷰 사진                   |
| score       | INT        |                                   | 리뷰 점수                   |
| user_id     | BIGINT     | FOREIGN KEY (User.id), NOT NULL   | 리뷰 작성자 ID              |
| prodcut_id  | BIGINT     | FOREIGN KEY (Product.id), NOT NULL| 리뷰 대상 상품 ID            |
| created_at  | TIMESTAMP  |                                   | 리뷰 생성 시간 (TimeStamped) |
| modified_at | TIMESTAMP  |                                   | 리뷰 수정 시간 (TimeStamped) |
### order Table
| 컬럼명      | 데이터 타입 | 제약 조건                           | 설명                        |
|-------------|------------|-------------------------------------|----------------------------|
| id          | BIGINT     | PRIMARY KEY, AUTO_INCREMENT         | 주문 ID                     |
| state       | VARCHAR    | NOT NULL                            | 주문 상태 (OrderState 열거형) |
| user_id     | BIGINT     | FOREIGN KEY (User.id), NOT NULL     | 주문 사용자 ID (외래 키)      |
| address_id  | BIGINT     | FOREIGN KEY (Address.id), NOT NULL  | 배송 주소 ID (외래 키)        |
| created_at  | TIMESTAMP  | NOT NULL                            | 주문 생성 시간 (TimeStamped) |
| modified_at | TIMESTAMP  | NOT NULL                            | 주문 수정 시간 (TimeStamped) |

### order_detail Table
| 컬럼명      | 데이터 타입 | 제약 조건                           | 설명                        |
|-------------|------------|-------------------------------------|----------------------------|
| id          | BIGINT     | PRIMARY KEY, AUTO_INCREMENT         | 주문 상세 ID                 |
| product_id  | BIGINT     | NOT NULL                            | 상품 ID                     |
| price       | BIGINT     | NOT NULL                            | 상품 가격                    |
| quantity    | BIGINT     | NOT NULL                            | 상품 수량                    |
| order_id    | BIGINT     | FOREIGN KEY (Order.id), NOT NULL    | 주문 ID (외래 키)            |

### Review entity
```java
@Entity
@Table(name="review")
@Getter
@NoArgsConstructor
public class Review extends TimeStamped {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column
    private String content;
    @Column
    private String photo;
    @Column
    private int score;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, foreignKey = @ForeignKey(ConstraintMode.NO_CONSTRAINT))
    private User user;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "prodcut_id", nullable = false, foreignKey = @ForeignKey(ConstraintMode.NO_CONSTRAINT))
    private Product product;


    public Review(
        ReviewRequest reviewRequest,
        Product product,
        User user
    ){
        this.content = reviewRequest.getContent();
        this.photo = reviewRequest.getPhoto();
        this.score = reviewRequest.getScore();
        this.product = product;
        this.user = user;
    }
    public void updateReview(
        ReviewRequest reviewRequest
    ) {
        this.content = reviewRequest.getContent();
        this.photo = reviewRequest.getPhoto();
        this.score = reviewRequest.getScore();
    }
}

```
* foreignKey = @ForeignKey(ConstraintMode.NO_CONSTRAINT)를 작성해서 데이터베이스 수준에서의 외래 키 제약 조건 생성을 막는다.
### createReview 메서드
```java
    //리뷰 생성
    public void createReview(
        Long productId,
        ReviewRequest reviewRequest,
        Long userId
    ) {
        // 상품 조회 및 예외 처리
        Product product = productRepository.findById(productId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "상품 정보가 존재하지 않습니다."));
        // 상품 상태 검증: 삭제된 상품인 경우 예외 발생
        if (!product.isState()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "삭제된 상품입니다.");
        }
        // 사용자 조회 및 예외 처리
        User user = findUserByIdOrThrow(userId);
        // 리뷰 작성 권한 검증: 주문 내역 확인
        // 위에 작성한 코드블럭 canUserReviewProduct 메서드
        if (!canUserReviewProduct(userId, productId)) {
            throw new IllegalArgumentException("리뷰를 작성할 수 없습니다. 주문 내역을 확인해주세요.");
        }
        // 리뷰 점수 유효성 검사: 1점부터 5점까지 허용 
        if(reviewRequest.getScore()<1||reviewRequest.getScore()>5){
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "1점부터 5점까지 입력해주세요");
        }
        // 리뷰 생성
        Review review = new Review(reviewRequest, product, user);
        // 리뷰를 데이터베이스에 저장
        reviewRepository.save(review);
    }
```


