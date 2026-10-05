# 19 CompletableFuture
> Last Format Time：10/6/2026 02:27:25

Java 版 Promise，而且功能非常丰富

```text
Java                     JavaScript

CompletableFuture         Promise

supplyAsync()             new Promise(...)

thenApply()               .then(x => return ...)

thenAccept()              .then(x => ...)

exceptionally()           .catch(...)
```