# 11 Stream
> Last Format Time：9/16/2026 19:24:55

先得到一条stream流，并把数据放上去

```java
        ArrayList<String> strings = new ArrayList<>();  
        strings.add("44444");  
        strings.add("444");  
        strings.add("4");  
        strings.add("44");  
  
        strings  
                .stream()  
                .filter(string -> string.startsWith("4"))  
                .filter(string -> string.length() >= 2)  
                .forEach(stirng -> System.out.println(stirng));  
  
//        44444  
//        444  
//        44
```

![[Pasted image 20260910125854.png]]

```java
Map<String, String> map = new HashMap<>();  
map.put("k1", "v1");  
map.put("k2", "v2");  
map.put("k3", "v3");  
  
map.entrySet().stream().forEach(string -> System.out.println(string));  
// k1=v1  
// k2=v2  
// k3=v3  
  
int[] arr = {1, 2, 3};  
Arrays.stream(arr).forEach(num -> System.out.println(num));  
  
String[] arr2 = {"1", "2", "3"};  
Arrays.stream(arr2).forEach(num -> System.out.println(num));  
  
Stream.of("1", "2", "3").forEach(num -> System.out.println(num));
```

---
## 中间方法
- 不影响原数据
- 可以链式调用
- 但是流只能链式嗲用一次，你保存下来之后，用了一次流后，再用流就会报错，这和 `js` 很不一样

![[Pasted image 20260910153452.png]]

```java
ArrayList<String> list = new ArrayList<>();  
Collections.addAll(list, "1", "22", "333", "4", "8", "8");  
  
list.stream()  
        .filter(s -> s.length() == 1).skip(1)  
        .limit(3)  
        .forEach(string -> System.out.println(string));  
  
list.stream()  
        .distinct().forEach(string -> System.out.println(string));  
  
Stream.concat(list.stream(), list.stream())  
        .forEach(string -> System.out.println(string));  
  
list.stream()  
        .map((s)->s.length())  
        .forEach(string -> System.out.println(string));
```


---
## 终结流方法
![[Pasted image 20260910155821.png]]

```java
ArrayList<String> list = new ArrayList<>();  
Collections.addAll(list, "1", "22", "333", "7", "8");  
  
System.out.println(list.stream().map((s) -> s.length()).count());  
// 6  
  
System.out.println(Arrays.toString(list.stream().toArray(value -> new String[value])));  
  
System.out.println(list.stream().map((s) -> s.length()).collect(Collectors.toList()).toString());  
  
System.out.println(list.stream().collect(Collectors.toMap(new Function<String, String>() {  
    @Override  
    public String apply(String s) {  
        return "k" + s;  
    }  
}, new Function<String, String>() {  
    @Override  
    public String apply(String s) {  
        return "v" + s;  
    }  
})));  
  
System.out.println(list.stream().collect(Collectors.toMap(s -> "k" + s, s -> "v" + s)));
```