# 배열 (Array)
배열은 고정된 크기의 연속된 메모리 블록에 데이터를 저장하는 구조다.
### 장점
1. 인덱스 접근: O(1) 시간 복잡도로 특정 인덱스에 접근 가능.
2. 캐시 친화적: 메모리 공간이 연속적이어서 캐시 효율이 높다.
3. 단순 구조: 구조가 단순하여 구현과 이해가 쉽다.

### 단점
1. 고정 크기: 배열의 크기는 생성 시점에 고정되며, 변경이 어렵다.
2. 삽입 및 삭제 비용: 중간에 요소를 넣거나 삭제하는 작업이 비효율적이며, 평균 O(n)의 시간 복잡도를 가진다.
3. 메모리 낭비: 미리 할당한 크기보다 적은 데이터를 저장할 경우 메모리 낭비가 발생한다.

```Java
public class ArrayExample {
    public static void main(String[] args) {
        int[] array = new int[5];
        array[0] = 1;
        array[1] = 2;
        array[2] = 3;
        
        System.out.println("Element at index 1: " + array[1]); // 출력: 2
    }
}

```
