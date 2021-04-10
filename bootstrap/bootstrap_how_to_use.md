# bootstrap how to use

2021.1.5

## Base

### HTML5 doctype

Bootstrap requires the use of the HTML5 doctype. Without it, you’ll see some funky incomplete styling, but including it shouldn’t cause any considerable hiccups.

```html
<!doctype html>
<html lang="en">
  ...
</html>
```

### Responsive meta tag

__Bootstrap is developed mobile first, a strategy in which we optimize code for mobile devices first and then scale up components as necessary using CSS media queries.__ To ensure proper rendering and touch zooming for all devices, add the responsive viewport meta tag to your `<head>`.

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Box-sizing

For more straightforward sizing in CSS, we switch the global box-sizing value from content-box to border-box.

### Reboot

For improved cross-browser rendering, we use Reboot to correct inconsistencies across browsers and devices while providing slightly more opinionated resets to common HTML elements.

## JavaScript

[offical document](https://getbootstrap.com/docs/5.0/getting-started/javascript/)

## Components

### Base classes

## CSS variables

 These provide easy access to commonly used values like our theme colors, breakpoints, and primary font stacks when working in your browser’s inspector, a code sandbox, or general prototyping. __All our custom properties are prefixed with bs- to avoid conflicts with third party CSS.__

## Layout

#### Breakpoints

Breakpoints are the triggers in Bootstrap for how your layout responsive changes across device or viewport sizes.

##### Core Concept

- __Breakpoints are the building blocks of responsive design.__ Use them to control when your layout can be adapted at a particular viewport or device size.

- __Use media queries to architect your CSS by breakpoint.__ Media queries are a feature of CSS that allow you to conditionally apply styles based on a set of browser and operating system parameters. We most commonly use min-width in our media queries.

- __Mobile first, responsive design is the goal.__ Bootstrap’s CSS aims to apply the bare minimum of styles to make a layout work at the smallest breakpoint, and then layers on styles to adjust that design for larger devices. This optimizes your CSS, improves rendering time, and provides a great experience for your visitors.

##### Available breakpoints

These breakpoints are customizable via Sass—you’ll find them in a Sass map in our `_variables.scss` stylesheet.

```css
$grid-breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 992px,
  xl: 1200px,
  xxl: 1400px
);
```

##### Media queries

[Media query](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries) is a CSS technique introduced in CSS3. It uses the @media rule to include a block of CSS properties only if a certain condition is true.

```css
/* If the browser window is 600px or smaller, the background color will be lightblue: */

@media only screen and (max-width: 600px) {
  body {
    background-color: lightblue;
  }
}
```

### Containers

#### How they work

`Containers` are the most basic layout element in Bootstrap and __are required when using our default grid system.__ Containers are used to contain, pad, and (sometimes) center the content within them. While containers can be nested, most layouts do not require a nested container.

Bootstrap comes with three different containers:

- `.container`, which sets a max-width at each responsive breakpoint
- `.container-fluid`, which is width: 100% at all breakpoints
- `.container-{breakpoint},` which is width: 100% until the specified breakpoint

#### Responsive containers

__RESPONSIVE CONTAINERS ALLOW YOU TO SPECIFY A CLASS THAT IS 100% WIDE UNTIL THE SPECIFIED BREAKPOINT IS REACHED, AFTER WHICH WE APPLY MAX-WIDTHS FOR EACH OF THE HIGHER BREAKPOINTS__. For example, .container-sm is 100% wide to start until the sm breakpoint is reached, where it will scale up with `md`, `lg`, `xl`, and `xxl`.

### Grid system

[A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

[Basic concepts of flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox)

[Aligning Items in a Flex Container](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Aligning_Items_in_a_Flex_Container)

- `Grid`支持 6种`breakpoint`。__This means you can control container and column sizing and behavior by each breakpoint.__
- Add any number of unit-less classes for each breakpoint you need and __every column will be the same width__.(在某一`brealpoint`下，所有未指定`class`的列的宽度相同)
- Auto-layout for flexbox grid columns also means __you can set the width of one column and have the sibling columns automatically resize around it__.(在某一`breakpoint`下，所有未指定`class`的列的宽度会根据已指定宽度的列自动调整)
- Use `col-{breakpoint}-auto` classes to size columns based on the natural width of their content.(根据内容长度自适应宽度)
- __For grids that are the same from the smallest of devices to the largest, use the `.col` and `.col-* classes`.__ Specify a numbered class when you need a particularly sized column; otherwise, feel free to stick to .col.(使用`.col`和`.col-*`对于所有`breakpoint`效果相同)
- Using a single set of `.col-sm-*` classes, you can create a basic grid system that starts out stacked and __becomes horizontal at the small breakpoint (`sm`)__.(使用`.col-sm-*`当`breakpoint`达到`sm`时水平展示)
- Mix and match（不同grid `class`可以组合使用）
- Use the responsive `.row-cols-*` classes to quickly set the number of columns. With `.row-cols-auto` you can give the columns their natural width.(`.row-cols-*` 设置列数，多余列数自动换行;`row-cols-auto` 自动根据内容计算列宽度)

[how to change grid config](https://getbootstrap.com/docs/5.0/layout/grid/#sass)

### Columns

#### Alignment

##### Vertical Alignment

`align-items-start` & `align-items-center` & `align-items-end`

##### Horizontal Alignment

`justify-content-start` & `justify-content-center` & `justify-content-end` & `justify-content-around` & `justify-content-between` & `justify-content-evenly`

##### Column Wrapping

If more than 12 columns are placed within a single row, each group of extra columns will, as one unit, wrap onto a new line.(如果一行超过了12列，则会将超过的行放在下一列)

#### Reordering

__Use `.order-` classes for controlling the visual order of your content.__ These classes are responsive, so you can set the order by breakpoint (e.g., `.order-1``.order-md-2`). Includes support for 1 through 5 across all six grid tiers.

#### Offsetting columns

Move columns to the right using `.offset-md-*` classes. These classes increase the left margin of a column by `*` columns.

#### Standalone column classes

The `.col-*` classes can also be used outside a `.row` to give an element a specific width. Whenever column classes are used as non direct children of a row, __the paddings are omitted__.

### Gutters

- __Gutters are the gaps between column content, created by horizontal `padding`__. We set `padding-right` and `padding-left` on each column, and use negative margin to offset that at the start and end of each row to align content.

- Gutters start at `1.5rem (24px)` wide. This allows us to match our grid to the padding and margin spacers scale.

- Gutters can be responsively adjusted. Use breakpoint-specific gutter classes to modify horizontal gutters, vertical gutters, and all gutters.

Horizontal gutters: `.gx-*`

Vertical gutters: `.gy-*`

Horizontal & vertical gutters: `.g-*`

### Z-index

don't know how to use it [link](https://getbootstrap.com/docs/5.0/layout/z-index/)

## Content

### Content Reboot

`Reboot` builds upon `Normalize`, providing many HTML elements with somewhat opinionated styles using only element selectors.Additional styling is done only with classes.(`Reboot` 基于 `Normalize.css` 重新设置了`html`某些属性的样式)

### Typography

Documentation and examples for Bootstrap typography, including global settings, headings, body text, lists, and more.(关于`bootstrap`中关于内容版式的一些使用)

### Img

#### Responsive images

Images in Bootstrap are made responsive with `.img-fluid`. This applies `max-width: 100%;` and `height: auto;` to the image so that it scales with the parent element.（响应式图片，图片随视窗大小改变）

### Image thumbnails

In addition to border-radius utilities, you can use `.img-thumbnail` to give an image a rounded `1px border` appearance.(为图片增加一个1px的边框)

### Aligning images

```html
<img src="..." class="rounded float-start" alt="...">
<img src="..." class="rounded float-end" alt="...">

<img src="..." class="rounded mx-auto d-block" alt="...">
<!-- equip to -->

<div class="text-center">
  <img src="..." class="rounded" alt="...">
</div>
```

### Tables

Add the base class `.table` to any `<table>`, then extend with our optional modifier classes or custom styles.

#### Accented tables

Striped rows: `.table-striped`

Hoverable rows: `.table-hover`

Active tables: `.table-active`

#### Table borders

Bordered tables: `.table-bordered`

Tables without borders: `.table-borderless`

Small tables: Add `.table-sm` to make any `.table` more compact by __cutting all cell padding in half__.

#### Responsive tables

Responsive tables allow tables to be scrolled horizontally with ease. Make any table responsive across all viewports by wrapping a `.table` with `.table-responsive`. Or, pick a maximum breakpoint with which to have a responsive table up to by using `.table-responsive{-sm|-md|-lg|-xl|-xxl}.`

### Figures

Use the included `.figure`, `.figure-img` and `.figure-caption` classes to provide some baseline styles for the HTML5 `<figure>` and `<figcaption>` elements. Images in figures have no explicit size, so be sure to add the `.img-fluid` class to your `<img>` to make it responsive.

## Forms

### Form controls

__Add `form-control` in input.__

__Sizing__: `.form-control-lg` & `.form-control-sm`

__Disabled__: Add the `disabled` boolean attribute on an input to give it a grayed out appearance and remove pointer events.

__Readonly__: Add the `readonly` boolean attribute on an input to prevent modification of the input’s value. Read-only inputs appear lighter (just like disabled inputs), but retain the standard cursor.

__Readonly plain text__: If you want to have `<input readonly>` elements in your form styled as plain text, use the `.form-control-plaintext` class to remove the default form field styling and preserve the correct margin and padding.

__File input__:

```html
<!-- upload file input -->
<div class="mb-3">
  <label for="formFile" class="form-label">Default file input example</label>
  <input class="form-control" type="file" id="formFile">
</div>
<!-- upload files input-->
<div class="mb-3">
  <label for="formFileMultiple" class="form-label">Multiple files input example</label>
  <input class="form-control" type="file" id="formFileMultiple" multiple>
</div>
```

__Color__: `<input type="color" class="form-control form-control-color" id="exampleColorInput" value="#563d7c" title="Choose your color">`(色彩选择器)

__Datalist__: Datalists allow you to create a group of `<option>`s that can be accessed (and autocompleted) from within an `<input>`. These are similar to `<select>` elements, but come with more menu styling limitations and differences. While most browsers and operating systems include some support for `<datalist>` elements, their styling is inconsistent at best.

```html
<!-- how to use datalist -->
<label for="exampleDataList" class="form-label">Datalist example</label>
<input class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Type to search...">
<datalist id="datalistOptions">
  <option value="San Francisco">
  <option value="New York">
  <option value="Seattle">
  <option value="Los Angeles">
  <option value="Chicago">
</datalist>
```

### Select

Add `form-select` to input.

#### Default

Custom `<select>` menus need only a custom class, `.form-select` to trigger the custom styles. Custom styles are limited to the `<select>`’s initial appearance and cannot modify the `<option>`s due to browser limitations.

#### Sizing

`form-select-lg` & `form-select-sm` & `multiple`

#### Disabled

Add the `disabled` boolean attribute on a select to give it a grayed out appearance and remove pointer events.

### Checks and radios

__Add `form-check-input` to input and put it in a `div` with `form-check`.__

#### Approach

use `.form-check` for `check` and `radios`

#### Switches

A switch has the markup of a custom checkbox but uses the `.form-switch` class to render a toggle switch. Switches also support the `disabled` attribute.

```html
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault">
  <label class="form-check-label" for="flexSwitchCheckDefault">Default switch checkbox input</label>
</div>
```

#### Default (stacked)

By default, any number of `checkboxes` and `radios` that are immediate sibling will be vertically stacked and appropriately spaced with `.form-check`.

#### Inline

Group checkboxes or radios on the same horizontal row by adding `.form-check-inline` to any `.form-check`.

#### Toggle buttons

Create button-like checkboxes and radio buttons by using `.btn` styles rather than `.form-check-label` on the `<label>` elements. These toggle buttons can further be grouped in a button group if needed.

#### Outlined styles

```html
<input type="checkbox" class="btn-check" id="btn-check-outlined" autocomplete="off">
<label class="btn btn-outline-primary" for="btn-check-outlined">Single toggle</label><br>

<input type="checkbox" class="btn-check" id="btn-check-2-outlined" checked autocomplete="off">
<label class="btn btn-outline-secondary" for="btn-check-2-outlined">Checked</label><br>
```

### Range

```html
<label for="customRange1" class="form-label">Example range</label>
<input type="range" class="form-range" id="customRange1">
```

#### Min and max

Range inputs have implicit values for `min` and `max—0` and 100, respectively. You may specify new values for those using the `min` and `max` attributes.(每步对应的只能为正数)

#### Steps

By default, range inputs “snap” to integer values. To change this, you can specify a step value. In the example below, we double the number of steps by using `step="0.5"`.(修改每步可为小数)

### Input Group

#### Wrapping

Input groups wrap by default via `flex-wrap: wrap` in order to accommodate custom form field validation within an input group. You may disable this with `.flex-nowrap`.

`input-group` & `input-group-text`

#### Sizing

`input-group-sm` & `input-group-lg`

### Floating labels

[Example](https://getbootstrap.com/docs/5.0/forms/floating-labels/#example)

Wrap a pair of `<input class="form-control">` and `<label>` elements in `.form-floating` to enable floating labels with Bootstrap’s textual form fields. A placeholder is required on each `<input>` as our method of CSS-only floating labels uses the `:placeholder-shown` pseudo-element. Also note that the `<input>` must come first so we can utilize a sibling selector (e.g., ~).

#### Textareas

By default, `<textarea>`s with `.form-control` will be the same height as `<input>`s.

#### Selects

Other than `.form-control`, floating labels are only available on `.form-selects`. They work in the same way, but unlike `<input>`s, they’ll always show the `<label>` in its floated state.

### Form Layout

[some useful example](https://getbootstrap.com/docs/5.0/forms/layout/)

### Validation

#### How it work

- HTML form validation is applied via CSS’s two pseudo-classes, `:invalid` and `:valid`. It applies to `<input>`, `<select>`, and `<textarea>` elements.
- Bootstrap scopes the `:invalid` and `:valid` styles to parent `.was-validated` class, usually applied to the `<form>`. Otherwise, any required field without a value shows up as invalid on page load. This way, you may choose when to activate them (typically after form submission is attempted).(适用于`client-side validation`)
- To reset the appearance of the form (for instance, in the case of dynamic form submissions using AJAX), remove the `.was-validated` class from the `<form>` again after submission.
- As a fallback, `.is-invalid` and `.is-valid` classes may __be used instead of the pseudo-classes for server-side validation__. They do not require a `.was-validated` parent class.(适用于`Server side validation`)
- Due to constraints in how CSS works, we cannot (at present) apply styles to a `<label>` that comes before a form control in the DOM without the help of custom JavaScript.
- All modern browsers support the constraint validation API, a series of JavaScript methods for validating form controls.
- Feedback messages may utilize the browser defaults (different for each browser, and unstylable via CSS) or our custom feedback styles with additional HTML and CSS.
- You may provide custom validity messages with setCustomValidity in JavaScript.

__For custom Bootstrap form validation messages, you’ll need to add the `novalidate` boolean attribute to your `<form>`. This disables the browser default feedback tooltips, but still provides access to the form validation APIs in JavaScript.__(十分重要)

[some useful demo](https://getbootstrap.com/docs/5.0/forms/validation/)

## BS-Components

### Accordion

_Build vertically collapsing accordions in combination with our Collapse JavaScript plugin._

#### Flush

Add `.accordion-flush` to remove the default background-color, some borders, and some rounded corners to render accordions edge-to-edge with their parent container.

### Alerts

#### Link color

Use the `.alert-link` utility class to quickly provide matching colored links within any alert.

#### Dismissing

- Be sure you’ve loaded the alert plugin, or the compiled Bootstrap JavaScript.
Add a close button and the `.alert-dismissible` class, which adds extra padding to the right of the alert and positions the close button.
- On the close button, add the `data-bs-dismiss="alert"` attribute, which triggers the JavaScript functionality. Be sure to use the `<button>` element with it for proper behavior across all devices.
- To animate alerts when dismissing them, be sure to add the `.fade` and `.show` classes.

```html
<div class="alert alert-warning alert-dismissible fade show" role="alert">
  <strong>Holy guacamole!</strong> You should check in on some of those fields below.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
```

### Badges

#### Background colors

Use our background utility classes to quickly change the appearance of a badge. Please note that when using Bootstrap’s default `.bg-light`, you’ll likely need a text color utility like `.text-dark` for proper styling. This is because __background utilities do not set anything but background-color__.

#### Pill badges

Use the `.rounded-pill` utility class to make badges more rounded with a larger border-radius.

### Breadcrumb

#### Dividers

Dividers are automatically added in CSS through `::before` and `content`. They can be changed by modifying a local CSS custom property `--bs-breadcrumb-divider`, or through the `$breadcrumb-divider` Sass variable — and `$breadcrumb-divider-flipped` for its RTL counterpart, if needed. We default to our Sass variable, which is set as a fallback to the custom property. This way, you get a global divider that you can override without recompiling CSS at any time.

#### Accessibility

Since breadcrumbs provide a navigation, it’s a good idea to add a meaningful label such as `aria-label="breadcrumb"` to describe the type of navigation provided in the `<nav>` element, as well as applying an `aria-current="page"` to the last item of the set to indicate that it represents the current page.

### Buttons

#### Disable text wrapping

If you don’t want the button text to wrap, you can add the `.text-nowrap` class to the button. In Sass, you can set `$btn-white-space: nowrap to` disable text wrapping for each button.

#### Button tags

The `.btn` classes are designed to be used with the `<button>` element. However, you can also use these classes on `<a>` or `<input>` elements (though some browsers may apply a slightly different rendering).(`.btn` 为按钮设计，不过也可用于`<a>`和`<input>`， 应用于`<a>`时页面不会跳转)

#### Outline buttons

`.btn-outline-*` remove all background images and colors on any button.

#### Sizes

`.btn-lg` or `.btn-sm` for additional sizes.

#### Disabled state

Make buttons look inactive by adding the `disabled` boolean attribute to any `<button>` element. Disabled buttons have `pointer-events: none` applied to, __preventing hover and active states from triggering.__

Disabled buttons using the `<a>` element behave a bit different:

- `<a>`s don’t support the disabled attribute, so you must add the `.disabled` class to make it visually appear disabled.
- Some future-friendly styles are included to disable all pointer-events on anchor buttons.
- Disabled buttons should include the `aria-disabled="true"` attribute to indicate the state of the element to assistive technologies.

#### Block buttons

使用[grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout)

#### Toggle states

Add `data-bs-toggle="button"` to toggle a button’s `active` state. If you’re pre-toggling a button, you must manually add the .active class and `aria-pressed="true"` to ensure that it is conveyed appropriately to assistive technologies.(button单选框)

### Button group

Wrap a series of buttons with `.btn` in `.btn-group`.

```html
<div class="btn-group" role="group" aria-label="Basic example">
  <button type="button" class="btn btn-primary">Left</button>
  <button type="button" class="btn btn-primary">Middle</button>
  <button type="button" class="btn btn-primary">Right</button>
</div>
```

### Cards

`.card`

body: `.card-body`

title/subtitle: `.card-title` and `.card-subtitle` to a `<h*>` tag

link: `.card-link` to `<a>` tag

img: `.card-img-top` places an image to the top of the card. `.card-img-bottom` places an image to the bottom of the card.

text: `.card-text` text can be added to the card.

header: `.card-header`(`.card-header` can be styled by adding .card-header to `<h*>` elements)

footer: `.card-footer`

image overlays: `.card-img-overlay`(将文字覆盖着图片上)

card group: `.card-group`

### Carousel (旋转木马)

[offcial document](https://getbootstrap.com/docs/5.0/components/carousel/)

### Close button

Provide an option to dismiss or close a component with `.btn-close`. Default styling is limited, but highly customizable. Modify the Sass variables to replace the default background-image. Be sure to include text for screen readers, as we’ve done with `aria-label`.

### Collapse

#### how to work

- `.collapse` hides content
- `.collapsing` is applied during transitions
- `.collapse .show` shows content

You can use a link with the `href` attribute, or a button with the `data-bs-target` attribute. __In both cases, the `data-bs-toggle="collapse"` is required.__

#### Multiple targets

A `<button>` or `<a>` can show and hide multiple elements by referencing them with a selector in its `href` or `data-bs-target` attribute. Multiple `<button>` or `<a>` can show and hide an element if they each reference it with their `href` or `data-bs-target` attribute.

#### Acollapse-ccessibility

`aria-expanded`: true/false. This attribute explicitly conveys the current state of the collapsible element tied to the control to screen readers and similar assistive technologies.(描述坍缩的状态，打开或关闭)

`aria-controls`:  the data-bs-target attribute is pointing to an id selector – you should add the aria-controls attribute to the control element, containing the id of the collapsible element.(包含所有的相关的需要坍缩的部件的`id`)

### Dropdowns

__They’re toggled by clicking, not by hovering; this is an intentional design decision.__

Dropdowns are built on a third party library, Popper, which provides dynamic positioning and viewport detection. __Be sure to include popper.min.js before Bootstrap’s JavaScript or use bootstrap.bundle.min.js / bootstrap.bundle.js which contains Popper__.

`.dropdown`

`.dropdown-toggle`

`.dropdown-menu`

`.dropdown-item`

`.data-bs-toggle="dropdown"`

`.dropdown-header`

`.dropdown-divider`

`.dropdown-toggle-split`

#### Dropdown-Sizing

`btn-lg` & `btn-sm`

#### Dark dropdowns

`.dropdown-menu-dark`

#### Dropup

`.dropup`: Trigger dropdown menus __above__ elements by adding `.dropup` to the parent element.

#### Dropright

`.dropend`: Trigger dropdown menus at the __right__ of the elements by adding `.dropend` to the parent element.

#### Dropleft

`.dropstart`: Trigger dropdown menus at the __left__ of the elements by adding `.dropstart` to the parent element.

#### Some useful

`.active`

`.disable`: Add `.disabled` to items in the dropdown to style them as disabled.

#### Menu alignment

`.dropdown-menu-end` & ``.dropdown-menu-start`

#### Responsive alignment

If you want to use responsive alignment, disable dynamic positioning by adding the `data-bs-display="static"` attribute and use the responsive variation classes.

`.dropdown-menu{-sm|-md|-lg|-xl|-xxl}-end` & `.dropdown-menu{-sm|-md|-lg|-xl|-xxl}-start`

#### Dropdown options

Use `data-bs-offset` or `data-bs-reference` to change the location of the dropdown.

### List group

#### Basic

`list-group` & `list-group-item`

Active items: `.active`

Disabled items: Add `.disabled` to a .list-group-item to make it appear disabled. __Note that some elements with .disabled will also require custom JavaScript to fully disable their click events (e.g., links).__

Flush: Add `.list-group-flush` to __remove some borders and rounded corners to render list group items edge-to-edge in a parent container__ (e.g., cards).(无填充，净凑的列表)

Horizontal: Add `.list-group-horizontal` to change the layout of list group items from vertical to horizontal across all breakpoints. Alternatively, choose a responsive variant `.list-group-horizontal-{sm|md|lg|xl|xxl}` to make a list group horizontal starting at that breakpoint’s min-width.(水平列表，支持`breakpoint`)

Contextual classes: `list-group-item-{primary|secondary|..|}`(修改列表的背景色)

[`data-bs-toggle="list"`](https://getbootstrap.com/docs/5.0/components/list-group/#using-data-attributes)

### Modal

[How it works](https://getbootstrap.com/docs/5.0/components/modal/#how-it-works)

[Live demo](https://getbootstrap.com/docs/5.0/components/modal/#live-demo)

#### Modal components

`modal header` & `modal body` & `modal footer`

We ask that you include modal headers with dismiss actions whenever possible, or provide another explicit dismiss action.

Static backdrop: `data-bs-backdrop="static"`(点击弹窗外部区域，弹窗不会自动消失)

Scrolling long content: __When modals become too long for the user’s viewport or device, they scroll independent of the page itself__. You can also create a scrollable modal that allows scroll the modal body by adding `.modal-dialog-scrollable` to `.modal-dialog`.（弹窗内容长度超过屏幕长度时的解决方案）

Vertically centered: `.modal-dialog-centered`(弹窗居中)

Remove animation: For modals that simply appear rather than fade in to view, remove the `.fade` class from your modal markup.

#### Tooltips and popovers

Tooltips and popovers can be placed within modals as needed. When modals are closed, any tooltips and popovers within are also automatically dismissed.

#### Using the grid

Utilize the Bootstrap grid system within a `modal` by nesting `.container-fluid` within the `.modal-body.` __Then, use the normal grid system classes as you would anywhere else__.

[Varying modal content(修改弹窗的内容)](https://getbootstrap.com/docs/5.0/components/modal/#varying-modal-content)

#### Change animation

The `$modal-fade-transform` variable determines the transform state of `.modal-dialog` before the modal fade-in animation, the `$modal-show-transform` variable determines the transform of `.modal-dialog` at the end of the modal fade-in animation.

[advance usage](https://getbootstrap.com/docs/5.0/components/modal/#dynamic-heights)

### Navs and tabs

#### Base nav

`nav-item` & `nav-link`

Navigation available in Bootstrap share general markup and styles, from the base `.nav` class to the active and disabled states. Swap modifier classes to switch between each style.

The base `.nav` component is built with flexbox and provide a strong foundation for building all types of navigation components. It includes some style overrides (for working with lists), some link padding for larger hit areas, and basic disabled styling.

> The base `.nav` component does not include any `.active` state. To convey the `active` state to assistive technologies, use the `aria-current` attribute — using the page value for current page, or true for the current item in a set.

The `.nav` uses `display: flex`, the nav links behave the same as nav items would, but without the extra markup.

#### Horizontal alignment

__By default, navs are left-aligned__, but you can easily change them to center or right aligned. __Centered with `.justify-content-center`. Right-aligned with `.justify-content-end`__.(导航栏默认左对齐, 可以调整为居中/右对齐)

#### Vertical

Stack your navigation by changing the flex item direction with the `.flex-column` utility.Use the responsive versions (e.g., `.flex-sm-column`) to stack them on some viewports but not others.(垂直方向导航栏)

#### Tabs

Takes the basic nav from above and adds the `.nav-tabs` class to generate a tabbed interface.

#### Fill and justify

Force your `.nav`’s contents to extend the full available width one of two modifier classes. __To proportionately fill all available space with your `.nav-items`, use `.nav-fill`. Notice that all horizontal space is occupied, but not every nav item has the same width__.

For equal-width elements, use `.nav-justified`. __All horizontal space will be occupied by nav links, but unlike the `.nav-fill` above, every nav item will be the same width__.

#### Using dropdowns

[demo](https://getbootstrap.com/docs/5.0/components/navs-tabs/#using-dropdowns)

#### JavaScript behavior

Dynamic tabbed: `role="tablist"`, `role="tab"`, `role="tabpanel"`. Instead, switch to an alternative element (in the example below, a simple `<div>`) and wrap the `<nav>` around it.s

[official document](https://getbootstrap.com/docs/5.0/components/navs-tabs/#javascript-behavior)

### Navbar

#### How it work

- Navbars require a wrapping `.navbar` with `.navbar-expand{-sm|-md|-lg|-xl|-xxl}` for responsive collapsing and color scheme classes.
- __Navbars and their contents are fluid by default__. Change the container to limit their horizontal width in different ways.
- Use our `spacing` and `flex` utility classes for controlling spacing and alignment within navbars.
- __Navbars are responsive by default__, but you can easily modify them to change that. Responsive behavior depends on our Collapse JavaScript plugin.
- Ensure accessibility by using a `<nav>` element or, if using a more generic element such as a `<div>`, add a `role="navigation"` to every navbar to explicitly identify it as a landmark region for users of assistive technologies.
- Indicate the current item by using `aria-current="page"` for the current page or `aria-current="true"` for the current item in a set.

#### Supported content

- `.navbar-brand` for your company, product, or project name.
- `.navbar-nav` for a full-height and lightweight navigation (including support for dropdowns).
- `.navbar-toggler` for use with our collapse plugin and other navigation toggling behaviors.
- `Flex` and `spacing` utilities for any form controls and actions.
- `.navbar-text` for adding vertically centered strings of text.
- `.collapse .navbar-collapse` for __grouping and hiding navbar contents by a parent breakpoint.__

#### Brand

The `.navbar-brand` can be applied to most elements, but an anchor works best, as some elements might require utility classes or custom styles.

Adding images to the `.navbar-brand` will likely always require custom styles or utilities to properly size.

#### Nav

__Navigation in navbars will also grow to occupy as much horizontal space as possible to keep your navbar contents securely aligned.__

Active states—with `.active—to` indicate the current page can be applied directly to `.nav-links` or their immediate parent `.nav-items`.

Please note that you should also add the `aria-current` attribute on the `.nav-link` itself.

And because we use classes for our navs, [you can avoid the list-based approach entirely if you like](https://getbootstrap.com/docs/5.0/components/navbar/#nav)

__You can also use dropdowns in your navbar__. Dropdown menus require a wrapping element for positioning, so be sure to use separate and nested elements for `.nav-item` and `.nav-link` as shown below.

#### Navbar-Forms

Immediate child elements of `.navbar` use flex layout and will default to `justify-content: space-between`. Use additional flex utilities as needed to adjust this behavior.

#### Text

Navbars may contain bits of text with the help of `.navbar-text`. __This class adjusts vertical alignment and horizontal spacing for strings of text.__

#### Color schemes

Theming the navbar has never been easier thanks to the combination of theming classes and background-color utilities. __Choose from `.navbar-light` for use with light background colors, or `.navbar-dark` for dark background colors. Then, customize with `.bg-*` utilities.__

#### Placement

Choose from `fixed to the top`, `fixed to the bottom`, or `stickied to the top` (scrolls with the page until it reaches the top, then stays there). Fixed navbars use `position: fixed`, meaning they’re pulled from the normal flow of the DOM and may require custom CSS (e.g., padding-top on the `<body>`) to prevent overlap with other elements.

Also note that `.sticky-top` uses `position: sticky`, __which isn’t fully supported in every browser.__

#### Responsive behaviors

Navbars can use `.navbar-toggler`, `.navbar-collapse`, and `.navbar-expand{-sm|-md|-lg|-xl|-xxl}` classes to determine when their content collapses behind a button. In combination with other utilities, you can easily choose when to show or hide particular elements.(导航栏坍缩为按钮)

For navbars that never collapse, add the `.navbar-expand` class on the navbar. For navbars that always collapse, don’t add any `.navbar-expand` class.

#### Toggler

[some demo](https://getbootstrap.com/docs/5.0/components/navbar/#toggler)

##### External content

[External content](https://getbootstrap.com/docs/5.0/components/navbar/?#external-content)

### Pagination

`nav` & `pagination` & `page-item` & `page-link`

#### Disabled and active states

Pagination links are customizable for different circumstances. Use `.disabled` for links that appear un-clickable and `.active` to indicate the current page.

While the `.disabled` class uses `pointer-events: none` to try to disable the link functionality of `<a>`s, that CSS property is not yet standardized and doesn’t account for keyboard navigation. __As such, you should always add `tabindex="-1"` on disabled links and use custom JavaScript to fully disable their functionality.__

#### Pagination-Sizing

`.pagination-lg` or `.pagination-sm` for additional sizes.

#### Pagination-Alignment

`justify-content-center` & `justify-content-end`

### Popovers

#### Overview

- Popovers rely on the 3rd party library Popper for positioning. __You must include `popper.min.js` before `bootstrap.js` or use `bootstrap.bundle.min.js` / `bootstrap.bundle.js` which contains `Popper` in order for popovers to work!__
- Popovers require the tooltip plugin as a dependency.
- Popovers are opt-in for performance reasons, so you must initialize them yourself.
- Zero-length title and content values will never show a popover.
- Specify container: 'body' to avoid rendering problems in more complex components (like our input groups, button groups, etc).
- Triggering popovers on hidden elements will not work.
- Popovers for `.disabled` or `disabled` elements __must be triggered on a wrapper element__.
- When triggered from anchors that wrap across multiple lines, popovers will be centered between the anchors' overall width. Use .text-nowrap on your `<a>`s to avoid this behavior.
- Popovers must be hidden before their corresponding elements have been removed from the DOM.
- Popovers can be triggered thanks to an element inside a shadow DOM.

#### Example

```html
<button type="button" class="btn btn-lg btn-danger" data-bs-toggle="popover" title="Popover title" data-bs-content="And here's some amazing content. It's very engaging. Right?">Click to toggle popover</button>
```

#### Four directions

Four options are available: top, right, bottom, and left aligned.

`data-bs-placement="top"|"right"|"bottom"|"left"`

[Usage](https://getbootstrap.com/docs/5.0/components/popovers/#usage)

### Progress

#### How to work

- use the `.progress` as a wrapper to indicate the max value of the progress bar.
- use the inner `.progress-bar` to indicate the progress so far.
- The `.progress-bar` requires __an inline style, utility class, or custom CSS to set their width__.
- The `.progress-bar` also requires some role and aria attributes to make it accessible.

#### Labels

Add labels to your progress bars by __placing text within the `.progress-bar`__.

#### Height

We only set a height value on the `.progress`, so if you change that value the inner .progress-bar will automatically resize accordingly.

#### Backgrounds

Use `background utility classes` to change the appearance of individual progress bars.

#### Multiple bars

```html
<div class="progress">
  <div class="progress-bar" role="progressbar" style="width: 15%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
  <div class="progress-bar bg-success" role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
  <div class="progress-bar bg-info" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
</div>
```

#### Striped

Add `.progress-bar-striped` to any `.progress-bar` to apply a stripe via CSS gradient over the progress bar’s background color.(进度条条纹)

#### Animated stripes

The striped gradient can also be animated. __Add `.progress-bar-animated` to `.progress-bar` to animate the stripes right to left via CSS3 animations__.(进度条动画)

### Scrollspy

Automatically update Bootstrap navigation or list group components based on scroll position to indicate which link is currently active in the viewport.(滑动页面内容时，导航栏或列表自动变换)

#### Scrollspy How to work

- It must be used on a Bootstrap `nav component` or `list group`.
- Scrollspy requires `position: relative;` on the element you’re spying on, usually the `<body>`.
- Anchors (`<a>`) are required and must point to an element with that `id`.

When successfully implemented, your nav or list group will update accordingly, moving the .active class from one item to the next based on their associated targets.

[some deoms](https://getbootstrap.com/docs/5.0/components/scrollspy/#example-in-navbar)

#### Usage

##### Via data attributes

To easily add scrollspy behavior to your topbar navigation, add `data-bs-spy="scroll"` to the element you want to spy on (__most typically this would be the `<body>`__). __Then add the `data-bs-target` attribute with the ID or class of the parent element of any Bootstrap `.nav` component.__

##### Via JavaScript

After adding `position: relative;` in your CSS, call the scrollspy via JavaScript:

```js
var scrollSpy = new bootstrap.ScrollSpy(document.body, {
  target: '#navbar-example'
})
```

### Spinners

__Bootstrap “spinners” can be used to show the loading state in your projects__. They’re built only with `HTML` and `CSS`, meaning you don’t need any `JavaScript` to create them. __You will, however, need some custom JavaScript to toggle their visibility. Their appearance, alignment, and sizing can be easily customized with our amazing utility classes__.(加载图标)

#### Border spinner

`.spinner-border`

```html
<div class="spinner-border" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
```

#### Colors

The border spinner uses `currentColor` for its `border-color`, __meaning you can customize the color with text color utilities__. __You can use any of our text color utilities on the standard spinner.__

#### Growing spinner

`.spinner-grow`

```html
<div class="spinner-grow" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
```

#### Spinner-Placement

[Placement](https://getbootstrap.com/docs/5.0/components/spinners/#placement)

#### Size

Add `.spinner-border-sm` and `.spinner-grow-sm` to make a smaller spinner that can quickly be used within other components. __Or, use custom CSS or inline styles to change the dimensions as needed__.

#### Spinner-Buttons

Use spinners within buttons to indicate an action is currently processing or taking place. __You may also swap the text out of the spinner element and utilize button text as needed.__

### Toasts(提示信息)

__Toasts are lightweight notifications designed to mimic the push notifications that have been popularized by mobile and desktop operating systems.__

#### Toasts-Overview

- Toasts are opt-in for performance reasons, __so you must initialize them yourself__.
- Toasts will automatically hide if you do not specify `autohide: false`.

[Examples](https://getbootstrap.com/docs/5.0/components/toasts/#examples)

#### Toasts-Basic

`toast` & `toast-header` & `toast-body`

#### Stacking

__You can stack toasts by wrapping them in a toast container, which will vertically add some spacing.__

#### Custom content

[link](https://getbootstrap.com/docs/5.0/components/toasts/#custom-content)

[Toasts Color schemes(颜色)](https://getbootstrap.com/docs/5.0/components/toasts/#color-schemes)

[Placement(位置)](https://getbootstrap.com/docs/5.0/components/toasts/#placement)

#### Toasts JavaScript behavior

##### Toasts Usage

Initialize toasts via JavaScript:

```js
var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  return new bootstrap.Toast(toastEl, option)
})
```

### Tooltips

[same to Popovers](https://getbootstrap.com/docs/5.0/components/tooltips/)

## Helpers

### Clearfix(do't understand how to use)

Easily clear floats by adding `.clearfix` to the parent element. Can also be used as a mixin.

[about clear in css](https://developer.mozilla.org/en-US/docs/Web/CSS/clear)

```html
<div class="clearfix">...</div>
```

### Colored links

You can use the `.link-*` classes to colorize links. __Unlike the `.text-*` classes, these classes have a `:hover` and `:focus` state.__

### Ratios

Use generated pseudo elements to make an element maintain the aspect ratio of your choosing. __Perfect for responsively handling video or slideshow embeds based on the width of the parent.__(根据父对象的宽度，按照比例确定长度)

Use the ratio helper to manage the aspect ratios of external content like `<iframe>`s, `<embed>`s, `<video>`s, and `<object>`s. These helpers also can be used on any standard HTML child element (e.g., a `<div>` or `<img>`). Styles are applied from the parent .ratio class directly to the child.

#### Ratios Basic

`ratio` & `ratio-1x1` & `ratio-4x3` & `ratio-16x9` & `ratio-21x9`

#### Sass map

Within `_variables.scss`, you can change the aspect ratios you want to use. Here’s our default `$ratio-aspect-ratios` map. Modify the map as you like and recompile your Sass to put them to use.

### Position

`fixed-top` & `fixed-bottom` & `sticky-top`

#### Responsive sticky top

```html
<div class="sticky-sm-top">Stick to the top on viewports sized SM (small) or wider</div>
<div class="sticky-md-top">Stick to the top on viewports sized MD (medium) or wider</div>
<div class="sticky-lg-top">Stick to the top on viewports sized LG (large) or wider</div>
<div class="sticky-xl-top">Stick to the top on viewports sized XL (extra-large) or wider</div>
```

### Visually hidden(对象隐藏)

Visually hide an element while still allowing it to be exposed to assistive technologies (such as screen readers) with `.visually-hidden`. Use `.visually-hidden-focusable` to visually hide an element by default, but to display it when it’s focused (e.g. by a keyboard-only user). Can also be used as mixins.

### Stretched link

Add `.stretched-link` to a link to make its containing block clickable via a `::after` pseudo element. __In most cases, this means that an element with `position: relative`; that contains a link with the `.stretched-link` class is clickable__.(将一个对象变为可点击的，并且指向对象中的`<a>`标签)

__Most custom components do not have `position: relative` by default, so we need to add the `.position-relative` here to prevent the link from stretching outside the parent element__.

[Identifying the containing block](https://getbootstrap.com/docs/5.0/helpers/stretched-link/#identifying-the-containing-block)

[What is containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block)

### Text truncation(将过长的内容变为省略符)

For longer content, you can add a `.text-truncate` class to truncate the text with an ellipsis. Requires `display: inline-block` or `display: block`.

## Utilities

### Utility API (skip!)

[What is sass](https://sass-lang.com/documentation/values/maps)

[official document](https://getbootstrap.com/docs/5.0/utilities/api/)

### Borders

#### Border

##### Additive

`border` & `border-{top| end| bottom| start}`

##### Subtractive

`border-0` & `border-{top| end| bottom| start}-0`

##### Border color

`border-{primary| success| ..}`

##### Border-width

`border-{1| 2| 3| 4| 5}`

##### Border-radius

`rounded` & `rounded-{top| end| bottom| start| circle| pill}`

##### Border-radius-sizes

Use the scaling classes for larger or smaller rounded corners. __Sizes range from 0 to 3__, and can be configured by modifying the utilities API.

### Uitity About Colors

#### Color

`.text-primary` & `.text-success` & ..

#### Background color

Background utilities do not set color, so in some cases you’ll want to use `.text-*` utilities.

`.bg-{primary| secondary| ..}`

#### Background gradient (do't understand)

[officical document](https://getbootstrap.com/docs/5.0/utilities/colors/#background-gradient)

### Display property

#### Display property How it work

Change the value of the `display property` with our responsive display utility classes. __We purposely support only a subset of all possible values for display. Classes can be combined for various effects as you need.__

#### Notation

As such, the classes are named using the format:

- `.d-{value}` for xs
- `.d-{breakpoint}-{value}` for `sm`, `md`, `lg`, `xl`, and `xxl`.

Where value is one of:

- none
- inline
- inline-block
- block
- grid
- table
- table-cell
- table-row
- flex
- inline-flex

The display values can be altered by changing the $displays variable and recompiling the SCSS.

__The media queries affect screen widths with the given breakpoint or larger__. For example, `.d-lg-none` sets `display: none;` on `lg`, `xl`, and `xxl` screens.

#### Hiding elements

To hide elements simply use the `.d-none class` or one of the `.d-{sm,md,lg,xl,xxl}-none` classes for any responsive screen variation.(响应式隐藏)

To show an element only on a given interval of screen sizes you can combine one `.d-*-none` class with a `.d-*-* class`, for example `.d-none` `.d-md-block` `.d-xl-none` `.d-xxl-none` will hide the element for all screen sizes except on medium and large devices.(隐藏条件组合)

#### Display in print(打印时的内容展示)

__Change the display value of elements when printing with our print display utility classes.__ Includes support for the same display values as our responsive `.d-*` utilities.

- `.d-print-none`
- `.d-print-inline`
- `.d-print-inline-block`
- `.d-print-block`
- `.d-print-grid`
- `.d-print-table`
- `.d-print-table-row`
- `.d-print-table-cell`
- `.d-print-flex`
- `.d-print-inline-flex`

### Flex

`.d-flex` & `.flex-row` & `.flex-column`

#### Direction

`.flex-row-reverse` & `.flex-column-reverse`

#### Justify content

Use `justify-content` utilities on __flexbox containers__ to change the alignment of flex items on the main axis (the `x-axis` to `start`, `y-axis` if `flex-direction: column`). Choose from `start` (browser default), `end`, `center`, `between`, `around`, or `evenly`.

#### Align items

Use `align-items` utilities on __flexbox containers__ to __change the alignment of flex items on the cross axis__ (the `y-axis` to `start`, `x-axis` if `flex-direction: column`). Choose from `start`, `end`, `center`, `baseline`, or `stretch` (browser default).

#### Align self

Use `align-self` utilities on __flexbox items__ to individually change their alignment on the cross axis (the `y-axis` to `start`, `x-axis` if `flex-direction: column`). Choose from the same options as `align-items`: `start`, `end`, `center`, `baseline`, or `stretch` (browser default).

#### Fill

Use the `.flex-fill` class on a series of sibling elements to __force them into widths equal to their content (or equal widths if their content does not surpass their border-boxes) while taking up all available horizontal space__.

#### Grow and shrink

Use `.flex-grow-*` utilities to toggle a flex item’s ability to grow to fill available space.

Use `.flex-shrink-*` utilities to toggle a flex item’s ability to shrink if necessary.

#### Auto margins

`.ms-auto` & `.me-auto` & `.mb-auto` & `.mt-auto`

#### Warp

Change how flex items wrap in a flex container. Choose from no wrapping at all (the browser default) with `.flex-nowrap`, wrapping with `.flex-wrap`, or reverse wrapping with `.flex-wrap-reverse`.

#### Order

Change the visual order of specific flex items with a handful of order utilities. As order takes any integer value from `0 to 5`, __add custom CSS for any additional values needed__.

#### Align content

__Use `align-content` utilities on flexbox containers to align flex items together on the cross axis__. Choose from `start` (browser default), `end`, `center`, `between`, `around`, or `stretch`. To demonstrate these utilities, we’ve enforced `flex-wrap: wrap` and increased the number of flex items.

### Float

#### Float-Overview

__These utility classes float an element to the `left` or `right`, or `disable floating`, based on the current viewport size using the CSS float property.__ `!important` is included to avoid specificity issues. These use the same viewport breakpoints as our grid system. Please be aware float utilities have no effect on flex items.

__Responsive variations also exist for each float value.__

### Interactions

#### Text selection(文字选择)

`.user-select-all` & `.user-select-auto(default)` & `.user-select-none`

#### Pointer events

Bootstrap provides `.pe-none` and `.pe-auto` classes to prevent or add element interactions.

### Overflow(溢出)

Adjust the `overflow` property on the fly with four default values and classes. __These classes are not responsive by default.__

`.overflow-auto` & `.overflow-hidden` & `.overflow-visible` & `.overflow-scroll`

### Utility-Position

[official document](https://getbootstrap.com/docs/5.0/utilities/position/)

[about position](https://developer.mozilla.org/en-US/docs/Web/CSS/position)

### Shadows

`.shadow-none` & `shadow-sm` & `shadow` & `shadow-lg`

### Utility-Sizing

`w-{25| 50| 75| 100| auto}` & `h-{25| 50| 75| 100| auto}`

`mw-100` & `mh-100`

```html
<div class="min-vw-100">Min-width 100vw</div>
<div class="min-vh-100">Min-height 100vh</div>
<div class="vw-100">Width 100vw</div>
<div class="vh-100">Height 100vh</div>
```

### Spacing

#### Spacing-Notation

The classes are named using the format `{property}{sides}-{size}` for `xs` and `{property}{sides}-{breakpoint}-{size}` for `sm`, `md`, `lg`, `xl`, and `xxl`.

Where property is one of:

- `m` - for classes that set `margin`
- `p` - for classes that set `padding`

Where sides is one of:

- `t` - for classes that set `margin-top` or `padding-top`
- `b` - for classes that set `margin-bottom` or `padding-bottom`
- `s` - for classes that set `margin-left` or `padding-left` in LTR, `margin-right` or `padding-right` in RTL
- `e` - for classes that set `margin-right` or `padding-right` in LTR, `margin-left` or `padding-left` in RTL
- `x` - for classes that set both `*-left` and `*-right`
- `y` - for classes that set both `*-top` and `*-bottom`
- blank - for classes that set a `margin` or `padding` on `all 4 sides` of the element

Where size is one of:

- `0` - for classes that eliminate the margin or padding by setting it to 0
- `1` - (by default) for classes that set the margin or padding to `$spacer` * .25
- `2` - (by default) for classes that set the margin or padding to `$spacer` * .5
- `3` - (by default) for classes that set the margin or padding to `$spacer`
- `4` - (by default) for classes that set the margin or padding to `$spacer` * 1.5
- `5` - (by default) for classes that set the margin or padding to `$spacer` * 3
- `auto` - for classes that set the margin to auto

(You can add more sizes by adding entries to the $spacers Sass map variable.)

#### Gap

When using `display: grid`, you can make use of `gap` utilities __on the parent grid container__. This can save on having to add margin utilities to individual grid items (children of a `display: grid` container). __Gap utilities are responsive by default__, and are generated via our utilities API, based on the $spacers Sass map.

`.gap-{0| 1| 2| 3| 4| 5}`

There is no `.gap-auto` utility class as it’s effectively the same as `.gap-0`.

### Utility-Text

#### Text alignment

Easily realign text to components with text alignment classes. For `start`, `end`, and `center` alignment, __responsive classes are available that use the same viewport width breakpoints as the grid system__.

`text-{start| end| center}`

#### Text wrapping and overflow

Wrap text with a `.text-wrap` class.

Prevent text from wrapping with a `.text-nowrap` class.

#### Word break

Prevent long strings of text from breaking your components' layout by using `.text-break`.

#### Text transform

`text-{lowercase| uppercase| capitalize}`

Note how `.text-capitalize` __only changes the first letter of each word, leaving the case of any other letters unaffected__.

#### Font size

`.fs-{1| 2| 3| 4| 5| 6}`

#### Font weight and italics

Quickly change the `font-weight` or `font-style` of text with these utilities. `font-style` utilities are abbreviated as `.fst-*` and `font-weight` utilities are abbreviated as `.fw-*`.

#### Line height

Change the `line height` with `.lh-*` utilities.

`.lh-{1| sm| base| lg}`

#### Monospace

Change a selection to our monospace font stack with `.font-monospace`.

#### Reset color

Reset a text or link’s color with `.text-reset`, __so that it inherits the color from its parent.__

#### Text decoration

```html
<p class="text-decoration-underline">This text has a line underneath it.</p>
<p class="text-decoration-line-through">This text has a line going through it.</p>
<a href="#" class="text-decoration-none">This link has its text decoration removed</a>
```

### Vertical alignment

Change the alignment of elements with the vertical-alignment utilities. Please note that `vertical-align` only affects `inline`, `inline-block`, `inline-table`, and `table cell` elements.

Choose from `.align-baseline`, `.align-top`, `.align-middle`, `.align-bottom`, `.align-text-bottom`, and `.align-text-top` as needed.

### Visibility

__Control the visibility of elements, without modifying their display, with visibility utilities.__

Set the visibility of elements with our visibility utilities. __These utility classes do not modify the display value at all and do not affect layout – `.invisible` elements still take up space in the page.__

Apply `.visible` or `.invisible` as needed.

## Extend

### Extend-Approach

Learn about the guiding principles, strategies, and techniques used to build and maintain Bootstrap so you can more easily customize and extend it yourself.

[link](https://getbootstrap.com/docs/5.0/extend/approach/)

### Extend-Icons

[link](https://getbootstrap.com/docs/5.0/extend/icons/)
