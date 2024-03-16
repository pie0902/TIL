# Merge Sort
병합 정렬은 "분할 정복(Divide and Conquer)" 전략을 사용한다.
1. 분할(Divide):
- 배열을 반으로 나누어 두 개의 하위 배열로 분할한다.
- 이 과정을 각 하위 배열이 길이가 1이 될 때까지 재귀적으로 반복한다.
- 작은 조각으로 나누는 과정이 재귀적으로 이루어진다.
2. 정복(Conquer):
- 이제 길이가 1인 배열은 이미 정렬된 상태다.
- 인접한 두 배열을 비교하여 정렬된 하나의 배열로 병합한다.
- 이 과정을 모든 하위 배열이 하나의 정렬된 배열이 될 때까지 반복한다.
3. 병합(Merge):
- 병합 과정에서는 두 정렬된 배열을 하나의 정렬된 배열로 합치는데, 각 배열의 첫 번째 요소를 비교하여 더 작은 요소를 새로운 배열에 추가하는 방식으로 진행된다.
```Java
public class MergeSort {
    public void mergeSort(int[] array) {
        if (array.length > 1) {
            int mid = array.length / 2;

            // 왼쪽과 오른쪽 부분 배열로 분할
            int[] left = new int[mid];
            int[] right = new int[array.length - mid];

            System.arraycopy(array, 0, left, 0, mid);
            System.arraycopy(array, mid, right, 0, array.length - mid);

            // 재귀적으로 분할
            mergeSort(left);
            mergeSort(right);

            // 병합
            merge(array, left, right);
        }
    }

    private void merge(int[] result, int[] left, int[] right) {
        int i = 0, j = 0, k = 0;

        // 왼쪽과 오른쪽 배열을 비교하여 병합
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }

        // 남은 요소 추가
        while (i < left.length) {
            result[k++] = left[i++];
        }

        while (j < right.length) {
            result[k++] = right[j++];
        }
    }

    public static void main(String[] args) {
        MergeSort ms = new MergeSort();
        int[] array = {38, 27, 43, 3, 9, 82, 10};
        ms.mergeSort(array);
        System.out.println(Arrays.toString(array)); // [3, 9, 10, 27, 38, 43, 82]
    }
}

```
### 병합 정렬의 장점
- 효율성: 병합 정렬은 항상 O(n log n)의 시간 복잡도를 가지며, 이는 큰 데이터셋을 처리할 때 매우 효율적이다.
- 안정성: 같은 값의 요소들이 정렬 후에도 원래의 순서를 유지한다.
- 예측 가능성: 최악의 경우에도 일관된 성능을 제공한다.
