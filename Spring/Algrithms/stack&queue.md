# Stack & Queue

### Stacck
스택은 데이터 저장과 접근에 LIFO(Last In, First Out) 원칙을 따르는 자료 구조다.즉 마지막에 삽입된 데이터가 가장 먼저 삭제된다.

### 주요 연산
1. push: 스택의 맨 위에 데이터를 추가한다.
2. pop: 스택의 맨 위에 있는 데이터를 제거하고 반환한다.
3. peek: 스택의 맨 위에 있는 데이터를 제거하지 않고 반환한다.
4. isEmpty: 스택이 비어 있는지 확인한다.
```Java
import java.util.Stack;

public class StackExample {
    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();
        stack.push(1);
        stack.push(2);
        stack.push(3);

        System.out.println("Top element: " + stack.peek()); // 3
        System.out.println("Removed element: " + stack.pop()); // 3
        System.out.println("Top element after pop: " + stack.peek()); // 2
    }
}
```

### Queue
큐는 데이터 저장과 접근에 FIFO(First In, First Out) 원칙을 따른다. 즉 저츰에 삽입된 데이터가 가장 먼저 삭제된다.

### 주요 연산
1. enqueue: 큐의 맨 뒤에 데이터를 추가한다.
2. dequeue: 큐의 맨 앞에 있는 데이터를 제거하고 반환한다.
3. peek: 큐의 맨 앞에 있는 데이터를 제거하지 않고 반환한다.
4. isEmpty: 큐가 비어 있는지 확인한다.
```Java
import java.util.LinkedList;
import java.util.Queue;

public class QueueExample {

    public static void main(String[] args) {
        Queue<Integer> queue = new LinkedList<>();
        queue.add(1);
        queue.add(2);
        queue.add(3);

        System.out.println("Front element: " + queue.peek()); // 1
        System.out.println("Removed element: " + queue.poll()); // 1
        System.out.println("Front element after dequeue: " + queue.peek()); // 2
    }
}
```

### 요약
#### 스택 (Stack):
- LIFO 구조 (Last In, First Out)
- 주요 연산: push, pop, peek, isEmpty
- 사용 예: 함수 호출 스택, 후위 표기법 계산
### 큐 (Queue):
- FIFO 구조 (First In, First Out)
- 주요 연산: enqueue, dequeue, peek, isEmpty
- 사용 예: 작업 스케줄링, 너비 우선 탐색 (BFS)

