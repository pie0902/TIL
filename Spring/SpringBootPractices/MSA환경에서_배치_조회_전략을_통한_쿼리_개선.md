## **배치 조회 전략** 을 사용한 쿼리 개선
>  관리자 페이지에서 상품마다 생긴 주문 상세를 조회 할 때 N+1 문제가 발생 했다.<br>
>  상품을 불러오고 주문서를 불러오고 주문 상세를 불러올 때마다 데이터베이스에서 관련 데이터들을  계속 조회 하면서 데이터를 가져온다.



### productService 에서 관리자의 상품 조회 코드

#### productAdminDto
```java
@Getter  
public class ProductAdminResponse {  
    private Long id;  
    private String name;  
    private Long price;  
    private Long stock;  
    private List<OrderDetailAdminResponse> orderDetails;  
  
    public ProductAdminResponse(Product product,List<OrderDetailAdminResponse> orderDetails) {  
        this.id = product.getId();  
        this.name = product.getName();  
        this.price = product.getPrice();  
        this.stock = product.getStock();  
        this.orderDetails = orderDetails;  
    }  
}
```
#### 관리자 페이지에서 상품들을 조회하는 메서드
```java
public List<ProductAdminResponse> getAdminProducts(User user, Pageable pageable) {  
    Page<Product> productPage = productRepository.findAllByUserIdAndStateTrue(user.getId(),  
        pageable);  
    return getPageResponse2(productPage);  
}
```
#### 상품마다 주문한 주문상세를 표시하는 메서드
```java
//상품을 주문한 사람들의 상세주문서 조회  
private List<ProductAdminResponse> getPageResponse2(Page<Product> productPage) {  
    return productPage.getContent().stream()  
        .map(product -> {  
            List<OrderDetail> orderDetails = orderAdminService.findOrderDetailsByProductId(  
                product.getId());  
            List<OrderDetailAdminResponse> orderDetailResponseDtos = new ArrayList<>();  
            for (OrderDetail orderDetail : orderDetails) {  
                Order order = orderRepository.getById(orderDetail.getOrderId());  
                orderDetailResponseDtos.add(new OrderDetailAdminResponse(orderDetail, order));  
            }  
            return new ProductAdminResponse(product, orderDetailResponseDtos);  
        })  
        .collect(Collectors.toList());  
}
```

### 코드의 구조
1. productPage.getContent():page 객체에서 product 객체의 리스트를 추출한다.
```java
return productPage.getContent().stream() .map(product -> {
```
2. 그 상품에 해당되는 주문 상세정보를 리스트로 가져온다.
```java
List<OrderDetail> orderDetails = orderAdminService.findOrderDetailsByProductId(product.getId());
```
3. 조회된 주문 상세정보 리스트를 순회하며 각 주문의 상세정보들을 가져온다.
```java
List<OrderDetailAdminResponse> orderDetailResponseDtos = new ArrayList<>();
for (OrderDetail orderDetail : orderDetails) {
    Order order = orderRepository.getById(orderDetail.getOrderId());
    orderDetailResponseDtos.add(new OrderDetailAdminResponse(orderDetail, order));
}
```
### 문제점
1. 데이터가 한 두 개면 크게 문제없지만, 상품 수가 200개, 1000개처럼 많아지면 처리해야 할 데이터베이스 조회량이 엄청나게 늘어나서, 시스템 전체의 성능이 많이 떨어질 수 있다.
2. 각 상품에 대해 주문 상세 정보를 가져오고, 각 주문 상세 정보마다 주문 정보를 다시 조회해야 해서 매 상품마다 발생하는 추가적인 데이터베이스 호출이 많아져서 처리 속도가 현저히 떨어진다.
3. 여러 데이터베이스 호출이 필요한데, 각 호출이 의존성을 갖고 순차적으로 이뤄져야 하므로, 하나의 호출에서 지연이 발생하면 전체 응답 시간이 길어질 수 있다. 이러한 연쇄적인 지연은 사용자 경험을 저하시킬 수 있다.

### 해결 방법
#### ID 리스트 기반의 배치 조회 최적화
* ID 리스트 기반의 배치(batch) 조회 최적화: OrderDetail과 Order를 각각의 ID 리스트를 기반으로 한 배치 조회로 처리하면, 데이터베이스 호출 횟수를 크게 줄일 수 있다. 이는 OrderDetail을 조회한 후, 이들에서 파생된 Order ID들로 Order를 한 번에 조회하는 방식으로 진행될 수 있다.

### 코드 수정
#### orderDataService Class 생성
* 우리팀의 서버는 msa 방식으로 운영되기 때문에 다른 도메인에서 필요한 메서드들을 feign을 이용해서 주입받아야 한다.
* orderService에서 productService를 주입받고 있기 때문에 순환참조를 방지하고 의존성을 낮추기 위해 orderDataService class를 생성해서 필요한 메서드들을 작성한다.
#### 개선된 코드
##### ProductService
```java
private List<ProductAdminResponse> getAdminPageResponse(
Page<Product> productPage
){  
    // Product List ID 리스트 추출  
    List<Long> productIds = productPage.getContent().stream().map(Product::getId).collect(Collectors.toList());  
    List<OrderDetail> orderDetails = orderDataService.getOrderDetailListUseProductIdList(productIds);  
    // OrderDetail 배치 조회  
    List<Long> orderIds = orderDataService.getOrderIdList(orderDetails);  
    // Order 배치 조회  
    Map<Long,Order> orderMap = orderDataService.getOrderMap(orderIds);  
    //productAdminResponse 생성  
    Map<Long,List<OrderDetailAdminResponse>> orderDetailsMap = orderDataService.getOrderDetailAdminResponse(orderMap,orderDetails);  
    return productPage.getContent().stream()  
        .map(product -> new ProductAdminResponse(product, orderDetailsMap.getOrDefault(product.getId(), Collections.emptyList())))  
        .collect(Collectors.toList());  
}
```
##### OrderDataService
```java
@Service  
@RequiredArgsConstructor  
public class OrderDataService {  
    private final OrderRepository orderRepository;  
    private final OrderDetailRepository orderDetailRepository;  
    //**********************productService에서 필요한 메서드**************************//  
    public List<OrderDetail> getOrderDetailListUseProductIdList(List<Long> productIds){  
        List<OrderDetail> orderDetails = orderDetailRepository.findByProductIdIn(productIds);  
        return orderDetails;  
    }  
  
    public List<Long> getOrderIdList(List<OrderDetail> orderDetails){  
        List<Long> orderIds = orderDetails.stream()  
            .map(OrderDetail::getOrderId)  
            .distinct()  
            .collect(Collectors.toList());  
        return orderIds;  
    }  
    public Map<Long, Order> getOrderMap(List<Long> orderIds) {  
        List<Order> orders = orderRepository.findByIdIn(orderIds);  
        Map<Long,Order> orderMap = orders.stream().collect(Collectors.toMap(Order::getId,order -> order));  
        return orderMap;  
    }  
    public Map<Long, List<OrderDetailAdminResponse>> getOrderDetailAdminResponse(Map<Long,Order> orderMap,List<OrderDetail> orderDetails) {  
        Map<Long, List<OrderDetailAdminResponse>> orderDetailsMap = orderDetails.stream()  
            .collect(Collectors.groupingBy(OrderDetail::getProductId,  
                Collectors.mapping(od -> new OrderDetailAdminResponse(od, orderMap.get(od.getOrderId())), Collectors.toList())));  
        return orderDetailsMap;  
  
    }  
}
```

#### OrderRepository&OrderDetailRepository
```java
//오더 아이디 리스트로 오더를 한번에 가져오는 쿼리  
List<Order> findByIdIn(List<Long> orderIds);
//프로덕트 아이디들의 주문서들을 한번에 가져오는 쿼리  
List<OrderDetail> findByProductIdIn(List<Long> productIds);
```

#### 개선되기 전 코드의 쿼리
```
Hibernate: 
    /* <criteria> */ select
        p1_0.id,
        p1_0.created_at,
        p1_0.description,
        p1_0.image_url,
        p1_0.modified_at,
        p1_0.name,
        p1_0.price,
        p1_0.state,
        p1_0.stock,
        p1_0.user_id 
    from
        product p1_0 
    where
        p1_0.user_id=? 
        and p1_0.state 
    limit
        ?, ?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    select
        o1_0.id,
        o1_0.kakao_tid,
        o1_0.address_id,
        o1_0.created_at,
        o1_0.modified_at,
        o1_0.state,
        o1_0.user_id 
    from
        orders o1_0 
    where
        o1_0.id=?
Hibernate: 
    select
        o1_0.id,
        o1_0.kakao_tid,
        o1_0.address_id,
        o1_0.created_at,
        o1_0.modified_at,
        o1_0.state,
        o1_0.user_id 
    from
        orders o1_0 
    where
        o1_0.id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id=?
```

1. **페이징 처리된 상품들을 조회**: 데이터베이스에서 특정 조건(여기서는 `user_id`와 상품의 `state`)에 맞는 상품들을 페이징 처리하여 조회한다.
2. **상품 ID를 사용하여 모든 `OrderDetail` 조회**: 단계 1에서 조회된 각 상품 ID를 기반으로 해당 상품들과 관련된 모든 `OrderDetail`을 데이터베이스에서 조회한다. 이 과정은 각 상품에 대한 주문 상세 정보를 가져오기 위해 수행된다.
3. **`OrderDetail`에서 얻은 `Order` ID를 사용하여 모든 `Order` 조회**: 조회된 `OrderDetail`들이 갖고 있는 `Order` ID를 사용하여 해당 주문들의 전체 정보를 데이터베이스에서 조회한다.
#### 개선된 코드의 쿼리 (수가 현저히 줄어든 것을 확인 할 수 있다.)
```
Hibernate: 
    /* <criteria> */ select
        p1_0.id,
        p1_0.created_at,
        p1_0.description,
        p1_0.image_url,
        p1_0.modified_at,
        p1_0.name,
        p1_0.price,
        p1_0.state,
        p1_0.stock,
        p1_0.user_id 
    from
        product p1_0 
    where
        p1_0.user_id=? 
        and p1_0.state 
    limit
        ?, ?
Hibernate: 
    /* <criteria> */ select
        od1_0.id,
        od1_0.order_id,
        od1_0.price,
        od1_0.product_id,
        od1_0.product_name,
        od1_0.quantity,
        od1_0.reviewed 
    from
        order_detail od1_0 
    where
        od1_0.product_id in (?, ?, ?, ?, ?, ?, ?, ?)
Hibernate: 
    /* <criteria> */ select
        o1_0.id,
        o1_0.kakao_tid,
        o1_0.address_id,
        o1_0.created_at,
        o1_0.modified_at,
        o1_0.state,
        o1_0.user_id 
    from
        orders o1_0 
    where
        o1_0.id in (?, ?)

```
1. **페이징 처리된 상품들을 조회**: 이 쿼리는 특정 사용자(`user_id`)가 소유하고 있는 활성 상태(`state`)의 상품들을 조회한다. 결과는 페이징 처리를 통해 제한된다. 이는 일반적으로 사용자의 상품 목록을 보여줄 때 사용된다.
2. **주문 상세 조회 쿼리**: 이 쿼리는 특정 상품 ID들에 대한 모든 주문 상세 정보를 조회한다. `product_id` 필드를 기준으로 여러 상품에 대한 주문 상세를 한 번의 쿼리로 불러온다. 이는 상품 ID 리스트를 기반으로 해당 상품들이 포함된 주문들의 상세 정보를 가져올 때 사용된다.
3. **주문 조회 쿼리**: 이 쿼리는 특정 주문 ID 리스트를 기반으로 해당 주문들의 상세 정보를 조회한다. 주문 상세 정보에서 얻은 `order_id`들을 사용하여 연관된 주문의 모든 정보를 한 번에 가져온다. 이는 주문 처리 시스템에서 특정 주문들에 대한 상세 정보를 보여줄 필요가 있을 때 사용된다.
