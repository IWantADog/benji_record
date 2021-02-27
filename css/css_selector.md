# how to use css selector

```
* {}

span {}

.classname {}

#idname {}

[attr] {}

[attr=value] {}

<!-- contain -->
[attr~=value] {} 

<!-- start -->
[attr|=value] {}

<!-- start -->
[attr^=value] {}

<!-- end -->
[attr$=value] {}

<!-- contain -->
[attr*=value] {}

<!-- A and B -->
A, B {}

<!-- all B in A -->
A B {}

<!-- A direct children with B -->
A > B {}

<!-- all b behind A -->
A ~ B {}

<!-- B fellow A (only on element)-->
A + B {}

div:visted {}

p::first-line {}
```

[CSS selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors#grouping_selectors)
