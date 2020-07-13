# JQuery Effect

## Changing Display Based on Current Visibility State

.toggle(): 将可见的元素隐藏，将隐藏的元素显示。可以输入参数，控制动画的时间。

.fadeToggle() & .slideToggle()

## Doing Something After an Animation Completes

当启动一个动画后，函数会直接返回JQuery对象，并不会等待动画完成之后再执行紧接着的链式操作。

如果需要等待动画完成之后，启动某个函数。则需要将该函数作为回调函数传入。