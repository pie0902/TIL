# 링크드 리스트 (Linked List)
링크드 리스트는 각 요소가 노드 형태로 저장되며, 각 노드는 데이터와 다음 노드에 대한 참조를 포함한다.

### 장점:
1. 동적 크기: 필요에 따라 크기를 동적으로 조정할 수 있다.
2. 삽입 및 삭제 효율적: 특정 위치에 요소를 삽입하거나 삭제하는 작업이 O(1) 시간 복잡도로 가능하며, 특히 중간에서의 삽입/삭제가 배열보다 효율적이다.
3. 메모리 효율: 필요한 만큼만 메모리를 사용하므로, 메모리 낭비가 적다.
### 단점:

1. 인덱스 접근 비용: 특정 인덱스에 접근하려면 O(n) 시간이 소요된다.
2. 추가 메모리 사용: 각 노드가 데이터 외에 추가로 포인터를 저장해야 하므로, 추가 메모리 사용이 발생한다. 
3. 캐시 비효율적: 메모리가 불연속적으로 할당되기 때문에 캐시 효율이 떨어진다.


```Java
class Node {
    int data;
    Node next;

    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

public class LinkedListExample {

    Node head;

// 삽입class Node {
int data;
    Node next;

    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

public class LinkedListExample {
    Node head;

    // 리스트에 노드 추가
    public void add(int data) {
        Node newNode = new Node(data);
        if (head == null) {
            head = newNode;
        } else {
            Node temp = head;
            while (temp.next != null) {
                temp = temp.next;
            }
            temp.next = newNode;
        }
    }

    // 리스트의 특정 위치에 노드 삽입
    public void insertAt(int index, int data) {
        Node newNode = new Node(data);
        if (index == 0) {
            newNode.next = head;
            head = newNode;
        } else {
            Node temp = head;
            for (int i = 0; i < index - 1 && temp != null; i++) {
                temp = temp.next;
            }
            if (temp != null) {
                newNode.next = temp.next;
                temp.next = newNode;
            } else {
                System.out.println("Index out of bounds");
            }
        }
    }

    // 리스트 출력
    public void printList() {
        Node temp = head;
        while (temp != null) {
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        LinkedListExample list = new LinkedListExample();
        list.add(1);
        list.add(2);
        list.add(3);

        list.printList(); // 출력: 1 2 3

        list.insertAt(1, 4);
        list.printList(); // 출력: 1 4 2 3

        list.insertAt(0, 5);
        list.printList(); // 출력: 5 1 4 2 3

        list.insertAt(5, 6);
        list.printList(); // 출력: 5 1 4 2 3 6

        list.insertAt(10, 7); // Index out of bounds
    }
}
```
