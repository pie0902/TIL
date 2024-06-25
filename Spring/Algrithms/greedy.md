# 그리디 알고리즘

## 거스름돈
>예를들어, 거스름돈으로 1260원을 줘야 하고, 500원 100원 50원 10원짜리 동전이 있다고 가정했을때. 그리디 알고리즘을 적용하면 가장 큰 금액부터 최대한 많이 거슬러 주는 것이 최적의 해답이 된다.


```Java
public class ChangeExample{
	public static void main(String[] args){
		int[] coinType = {500,100,50,10};
		int change = 1260;
		int[] coinCounts = new int[4];

		for(int i = 0; i<coinType.length;i++){
			coinCounts[i] = change/coinTypes[i];
			change %= cointypes[i]
		}
		System.out.println("거스름돈 개수:"); 
		for (int i = 0; i < coinTypes.length; i++) {
			 System.out.println(coinTypes[i] + "원: " + coinCounts[i] + "개"); 
		}
	}
}
```
### 코드해석
- 1. coinTypes 배열에는 동전의 종류를 큰 금액부터 순서대로 저장한다.
- 2. change 변수에는 거슬러 줘야 할 금액인 1260을 저장한다.
- 3. coinCounts 배열은 각 동전 종류별로 사용된 개수를 저장할 배열이다.
- 4. 반복문을 사용하여 coinTypes 배열을 순회한다.
    - 현재 동전 종류로 거슬러 줄 수 있는 최대 계수를 계산하여 coinCounts 배열에 저장한다.
    - 거슬러 준 금액만큼 change에서 차감한다.
* 5. 마지막으로 각 동전 종류별로 사용된 개수를 출력한다.
