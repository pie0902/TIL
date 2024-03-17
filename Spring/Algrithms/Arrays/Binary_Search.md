# 이분탐색

이분 탐색(Binary Search)은 정렬된 배열에서 특정 값을 찾기 위해 사용하는 효율적인 알고리즘이다. 이분 탐색은 배열을 반씩 나누어 검색 범위를 좁혀가는 방식으로 작동한다.
### 이분 탐색의 작동 원리
1. 초기 설정: 배열의 중간 요소를 선택한다.
2. 비교:
- 중간 요소가 찾고자 하는 값과 같다면, 해당 값을 반환한다.
- 중간 요소가 찾고자 하는 값보다 크다면, 검색 범위를 중간 요소의 왼쪽 절반으로 좁힌다.
- 중간 요소가 찾고자 하는 값보다 작다면, 검색 범위를 중간 요소의 오른쪽 절반으로 좁힌다.
3. 반복: 검색 범위가 0이 될 때까지 위 과정을 반복한다.

### 시간 복잡도
이분 탐색의 시간 복잡도는 O(log n)이다. 이는 배열의 크기가 커질수록, 검색해야 하는 범위가 절반씩 줄어들기 때문이다.

```Java
public class BinarySearch {
    public int binarySearch(int[] array, int target) {
        int left = 0;
        int right = array.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            // 중간 요소가 타겟 값인 경우
            if (array[mid] == target) {
                return mid;
            }

            // 중간 요소가 타겟 값보다 큰 경우
            if (array[mid] > target) {
                right = mid - 1;
            }
            // 중간 요소가 타겟 값보다 작은 경우
            else {
                left = mid + 1;
            }
        }

        // 타겟 값을 찾지 못한 경우
        return -1;
    }

    public static void main(String[] args) {
        BinarySearch bs = new BinarySearch();
        int[] array = {1, 3, 5, 7, 9, 11, 13, 15};
        int target = 7;
        int result = bs.binarySearch(array, target);
        System.out.println("Target found at index: " + result); // 출력: Target found at index: 3
    }
}

```
### 요약
- 이분 탐색(Binary Search): 정렬된 배열에서 특정 값을 찾기 위해 배열을 반복적으로 반으로 나누어 검색하는 알고리즘.
- 시간 복잡도: O(log n) – 검색 범위가 반복적으로 절반으로 줄어든다.
