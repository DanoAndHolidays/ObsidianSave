# Test your skills: Sizing

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Sizing)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Backgrounds_and_borders)

The aim of this skill test is to help you assess whether you understand the different ways of [sizing items in CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Sizing).

**Note:** To get help, read our [Test your skills](https://developer.mozilla.org/en-US/docs/Learn_web_development#test_your_skills) usage guide. You can also reach out to us using one of our [communication channels](https://developer.mozilla.org/en-US/docs/MDN/Community/Communication_channels).

## [Sizing 1](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Sizing#sizing_1)

In this task, you have two boxes.

To complete the task:

1. Size the first box so that the height will be at least `100px`, even if there is less content that would cause it to grow to that height. The content should not overflow if it doesn't fit into the box.
2. To test this, remove the content from the HTML to make sure you still get a `100px` tall box even with no content.
3. Size the second box so that it is fixed at `100px` tall. In this case, the content should overflow.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=f22fbe93fcb3887472b0c0aa108f13eb4f114656&state=3ZBBbtwwDEWv8qFlMLHjQbNxJgG66g268kayGJm1JBqi7Ewa5O6FPZsCLdB9VwTIxw%2B8%2F2GmmqLpzcXzhjFa1efBOLnCybUbzMuQgctyDOA7hcCkIIWTvCo2cawnLEU4e8ImikW0rlFAqmtCsoEVs0yxWMd4o6gTJLPkW6K3PEuGTbbYXCdUW1UYVZKtHKMgUdzvP9eZ4chmBFsijw2%2BrckJHFFFKERZb4GjlAyVWUDZ80YIBxdkLb45ZNrd5tJ63l6GPOS%2FiZ%2F%2Ff3FzMqOq6Y0T%2F46PHXiVXHt0zZkSWnTNI9RmvVcq%2FPq0A4v1nnPo0VF6GvLnXl%2BzV3a8OymeSo%2FH5QqVyB4u2nE%2BPt%2FY16nHl4eH5Xoski2B872TWiX9EdjdEts7fPUeWt8jKSYqhLv2N%2Bz8L8yczI%2Fd0ZxMnSiR6U3kMFXz%2BQs%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=f22fbe93fcb3887472b0c0aa108f13eb4f114656&state=3ZBBbtwwDEWv8qFlMLHjQbNxJgG66g268kayGJm1JBqi7Ewa5O6FPZsCLdB9VwTIxw%2B8%2F2GmmqLpzcXzhjFa1efBOLnCybUbzMuQgctyDOA7hcCkIIWTvCo2cawnLEU4e8ImikW0rlFAqmtCsoEVs0yxWMd4o6gTJLPkW6K3PEuGTbbYXCdUW1UYVZKtHKMgUdzvP9eZ4chmBFsijw2%2BrckJHFFFKERZb4GjlAyVWUDZ80YIBxdkLb45ZNrd5tJ63l6GPOS%2FiZ%2F%2Ff3FzMqOq6Y0T%2F46PHXiVXHt0zZkSWnTNI9RmvVcq%2FPq0A4v1nnPo0VF6GvLnXl%2BzV3a8OymeSo%2FH5QqVyB4u2nE%2BPt%2FY16nHl4eH5Xoski2B872TWiX9EdjdEts7fPUeWt8jKSYqhLv2N%2Bz8L8yczI%2Fd0ZxMnSiR6U3kMFXz%2BQs%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

```
<div class="box box1">
  <p>
    Veggies es bonus vobis, proinde vos postulo essum magis kohlrabi welsh onion
    daikon amaranth tatsoi tomatillo melon azuki bean garlic. Gumbo beet greens
    corn soko endive gumbo gourd.
  </p>
</div>

<div class="box box2">
  <p>
    Veggies es bonus vobis, proinde vos postulo essum magis kohlrabi welsh onion
    daikon amaranth tatsoi tomatillo melon azuki bean garlic. Gumbo beet greens
    corn soko endive gumbo gourd.
  </p>
</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=f22fbe93fcb3887472b0c0aa108f13eb4f114656&state=3ZBBbtwwDEWv8qFlMLHjQbNxJgG66g268kayGJm1JBqi7Ewa5O6FPZsCLdB9VwTIxw%2B8%2F2GmmqLpzcXzhjFa1efBOLnCybUbzMuQgctyDOA7hcCkIIWTvCo2cawnLEU4e8ImikW0rlFAqmtCsoEVs0yxWMd4o6gTJLPkW6K3PEuGTbbYXCdUW1UYVZKtHKMgUdzvP9eZ4chmBFsijw2%2BrckJHFFFKERZb4GjlAyVWUDZ80YIBxdkLb45ZNrd5tJ63l6GPOS%2FiZ%2F%2Ff3FzMqOq6Y0T%2F46PHXiVXHt0zZkSWnTNI9RmvVcq%2FPq0A4v1nnPo0VF6GvLnXl%2BzV3a8OymeSo%2FH5QqVyB4u2nE%2BPt%2FY16nHl4eH5Xoski2B872TWiX9EdjdEts7fPUeWt8jKSYqhLv2N%2Bz8L8yczI%2Fd0ZxMnSiR6U3kMFXz%2BQs%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

```
body {
  font: 1.2em / 1.5 sans-serif;
  padding: 1em;
}

.box {
  border: 5px solid black;
  width: 400px;
  margin-bottom: 1em;
}

.box1 {
  /* Add styles here */
}

.box2 {
  /* Add styles here */
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=58b2cd13d8f4c92efd2cf305457bd29500b0911f&state=3ZAxbtwwEEWv8sHS2JWsRdzIawOpcgNXakhxLE1EcgQOJa9t%2BO6BtCmMxED6VARm3jzw%2F3czlhhMa86eV%2FTBqj50xskFTi5NZx67BJzn%2FQGeaBiYFKRwkhbFKo71gDkLJ09YRTGLliUISHWJiHZgxSRjyNYxXijoCEks6Wr0lidJsNFmm8qIYosKo0i0hUMQRArb%2Fm2ZGI5swmBz4L7CjyU6gSMqGDJR0quwl5ygMgkoeV4Jw84NsmRf7WHqLc259rw%2BdqlLXwU%2F%2Ff%2FBzcH0qqY1Tvwr3jfgWVJp0VQniqjRVHdQm%2FSolPn5fgNm6z2noUVD8b5LH1t91VbZfu4ke8ot7uYLVAJ7uGD7ab98YV%2FGFt9ub%2BfLPog2D5yOTkqR%2BJewuRrrG3z3HlpeAylGyoSb%2BhN2%2Bhf2yRU5HUfiYdwi%2Fv7Gn6Iv9uZgfm4tmYMpI0UyrQkbZD5%2BAQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

Click here to show the solution

There are two boxes. The first one should be given a `min-height` so it expands to hold the additional content, but will not shrink below `100px` tall if the content is removed. The second box is given a fixed height, which will cause content to overflow.

## [Sizing 2](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Sizing#sizing_2)

In this task, you have a box that contains another box.

To complete the task:

1. Make the inner box width `60%` of the width of the outer box. The [`box-sizing`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-sizing) property is set to `border-box`, which means that the total width includes any `padding` and `border`.
2. Give the inner box `10%` padding on all sides.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=e26b58542ae0fa3b089cad26380f1a773e02c879&state=VZBbbgIxDEW3YlmqKiHmQVX6EShSF9Ad5CcPM5OSxyjJwFDE3ivCIJUvS9fXx9e%2BYJ%2BdRYZbbY6grEjpk6MME8cd9wBPsvGeIsfdtzgQOIKP9gXCHtwZBhHJ59cEJ6NzX28bbY477h8Vl6hSQoYy6DNcbuB98JnBqn4jBw2s6jUk4VOVKJr95mYYhNbGdwxW5DbcX7nnvpZhuo%2FLEDVFButhghSs0SCtUIcyWTIweG%2FbYSqCE7EzvpIh5%2BCegeWkGSnUoYth9LpSwYbIIJIkpcQwxsFSIc2NU2%2FyXbjnqKLQZkwlzgO9eASdqmR%2ByyWzWYbZ9H97s4AvrSHls6UEPUWCRVNcuMSf2%2B9wibknR8jQmq7PeP0D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=e26b58542ae0fa3b089cad26380f1a773e02c879&state=VZBbbgIxDEW3YlmqKiHmQVX6EShSF9Ad5CcPM5OSxyjJwFDE3ivCIJUvS9fXx9e%2BYJ%2BdRYZbbY6grEjpk6MME8cd9wBPsvGeIsfdtzgQOIKP9gXCHtwZBhHJ59cEJ6NzX28bbY477h8Vl6hSQoYy6DNcbuB98JnBqn4jBw2s6jUk4VOVKJr95mYYhNbGdwxW5DbcX7nnvpZhuo%2FLEDVFButhghSs0SCtUIcyWTIweG%2FbYSqCE7EzvpIh5%2BCegeWkGSnUoYth9LpSwYbIIJIkpcQwxsFSIc2NU2%2FyXbjnqKLQZkwlzgO9eASdqmR%2ByyWzWYbZ9H97s4AvrSHls6UEPUWCRVNcuMSf2%2B9wibknR8jQmq7PeP0D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

```
<div class="box">
  <div class="inner">Make me 60% of my parent's width.</div>
</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=e26b58542ae0fa3b089cad26380f1a773e02c879&state=VZBbbgIxDEW3YlmqKiHmQVX6EShSF9Ad5CcPM5OSxyjJwFDE3ivCIJUvS9fXx9e%2BYJ%2BdRYZbbY6grEjpk6MME8cd9wBPsvGeIsfdtzgQOIKP9gXCHtwZBhHJ59cEJ6NzX28bbY477h8Vl6hSQoYy6DNcbuB98JnBqn4jBw2s6jUk4VOVKJr95mYYhNbGdwxW5DbcX7nnvpZhuo%2FLEDVFButhghSs0SCtUIcyWTIweG%2FbYSqCE7EzvpIh5%2BCegeWkGSnUoYth9LpSwYbIIJIkpcQwxsFSIc2NU2%2FyXbjnqKLQZkwlzgO9eASdqmR%2ByyWzWYbZ9H97s4AvrSHls6UEPUWCRVNcuMSf2%2B9wibknR8jQmq7PeP0D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

```
body {
  font: 1.2em / 1.5 sans-serif;
  padding: 1em;
}

.box {
  border: 5px solid black;
  width: 400px;
  margin-bottom: 1em;
}

.inner {
  background-color: rebeccapurple;
  color: white;
  border-radius: 5px;
}

* {
  box-sizing: border-box;
}
.inner {
  /* Add styles here */
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=5ce5ee561189d5b4e8106c8deaac18b7aeb82d8a&state=ZVBbbsIwELzKaiVUCZEHVeHDUKQeoDfwjx0viRs%2FIttAKOLuFSZIpf1aaXZ2dmYu2CVrkOFW6SM0RsT4zlH6keOOO4AnWDtHgePuU%2FQElmBdz8DvwZ5hEIFceolw0ip15bZS%2Brjj7jFxgU2MyFB6dYbLTXjvXWKwLF%2FJQgXLcgVRuFhECnq%2FuREGoZR2LYMl2Q13V%2B64K6Uf7%2BfSB0WBwWoYIXqjFUgjmj5fZg8M3up6GDNgRWi1K6RPydtnwRxpkhRN3wZ%2FcKpovPGBQSBJTSOGQxgMZaVpcep0ugN3H0UQSh9itvOQnj%2BMjkXU3znJRJZ%2BIv3%2BXs3hQymI6WwoQkeBYF79Y03R1vXsT0cZuOamv25F4wJTR5aQodFtl%2FD6Aw%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

Click here to show the solution

Set the box `width` to `60%`, and give it a `padding` value of `10%`. All elements already have `box-sizing: border-box` set to save you from worrying about calculating the `60%` width value:

## [Sizing 3](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Sizing#sizing_3)

In this task, you have two images in boxes. One image is smaller than the box, while the other is larger, causing it to break out of the box.

To complete the task, imagine that the box is responsive and therefore could grow and shrink. Apply a declaration to the images so that the large image shrinks down into the box, but the small image does not stretch.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=d92b6f96699dd319cf41bb83164798930190d894&state=pY%2FBTsMwEER%2FZbVH1MZtpXAIbSVufIQl5MQb29ReW14DqRD%2FjkLFhRMSpz3MzNuZD%2FQtRRzwaMMbTNGInDSOedF41gxwDMmtF8DEdtL4CCXwBaSZqvEmSJ1OGn1rRQalkuXOheZfxy5kJd5UslsjQk1USMaRKFpMKpFErZTtyns%2B9PfLob%2FvCjuNoM6aj8qGt7NmzX9s9pQbmFBhNDHmzAJzvAZ2EBimSKaCXK4bMGzBwFTzu4U8Q6FcIq2e5gnmXMnV%2FMr2%2F9t%2BanQv5fck3OAkggOO2V7hY%2F00Z24D7LsDJVCw73oQw7IVqmF%2BWA3FWBvYDbCn9KD5U3M35uUWHnO1VAfoywKSY7AwRjNdvnPJVBd4O%2BbWcvpJA7wH2%2FwA%2FW5XlhtOc0juxlN38GgtSLtGEvBUCe7Utwk3%2BLIWxw02T4lwwBicb%2Fj5BQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=d92b6f96699dd319cf41bb83164798930190d894&state=pY%2FBTsMwEER%2FZbVH1MZtpXAIbSVufIQl5MQb29ReW14DqRD%2FjkLFhRMSpz3MzNuZD%2FQtRRzwaMMbTNGInDSOedF41gxwDMmtF8DEdtL4CCXwBaSZqvEmSJ1OGn1rRQalkuXOheZfxy5kJd5UslsjQk1USMaRKFpMKpFErZTtyns%2B9PfLob%2FvCjuNoM6aj8qGt7NmzX9s9pQbmFBhNDHmzAJzvAZ2EBimSKaCXK4bMGzBwFTzu4U8Q6FcIq2e5gnmXMnV%2FMr2%2F9t%2BanQv5fck3OAkggOO2V7hY%2F00Z24D7LsDJVCw73oQw7IVqmF%2BWA3FWBvYDbCn9KD5U3M35uUWHnO1VAfoywKSY7AwRjNdvnPJVBd4O%2BbWcvpJA7wH2%2FwA%2FW5XlhtOc0juxlN38GgtSLtGEvBUCe7Utwk3%2BLIWxw02T4lwwBicb%2Fj5BQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

```
<div class="box">
  <img
    alt="A pink star"
    src="https://mdn.github.io/shared-assets/images/examples/star-pink_256x256.png" />
</div>

<div class="box">
  <img
    alt="Hot air balloons flying in clear sky, and a crowd of people in the foreground"
    src="https://mdn.github.io/shared-assets/images/examples/balloons.jpg" />
</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=d92b6f96699dd319cf41bb83164798930190d894&state=pY%2FBTsMwEER%2FZbVH1MZtpXAIbSVufIQl5MQb29ReW14DqRD%2FjkLFhRMSpz3MzNuZD%2FQtRRzwaMMbTNGInDSOedF41gxwDMmtF8DEdtL4CCXwBaSZqvEmSJ1OGn1rRQalkuXOheZfxy5kJd5UslsjQk1USMaRKFpMKpFErZTtyns%2B9PfLob%2FvCjuNoM6aj8qGt7NmzX9s9pQbmFBhNDHmzAJzvAZ2EBimSKaCXK4bMGzBwFTzu4U8Q6FcIq2e5gnmXMnV%2FMr2%2F9t%2BanQv5fck3OAkggOO2V7hY%2F00Z24D7LsDJVCw73oQw7IVqmF%2BWA3FWBvYDbCn9KD5U3M35uUWHnO1VAfoywKSY7AwRjNdvnPJVBd4O%2BbWcvpJA7wH2%2FwA%2FW5XlhtOc0juxlN38GgtSLtGEvBUCe7Utwk3%2BLIWxw02T4lwwBicb%2Fj5BQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

```
body {
  font: 1.2em / 1.5 sans-serif;
  padding: 1em;
}
.box {
  border: 5px solid black;
  margin-bottom: 1em;
  width: 500px;
}

img {
  /* Add styles here */
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=fb636b16c188a8b6cdee1a4280c8c68f6d53b6d5&state=pY%2FBauQwDIZfRQj2UibxzEB6SGcGeutDGIoTK447tmwst81Q%2Bu4lzXYPe1rYkw76%2Fk%2F6P3CuMWCPJ%2BvfYAxG5KxxSIvGi2aAk49unQAm1LPGR8ieryDVFI3bQsp41jjXmqVXKlpuna%2Fz69D6pGQ2hWxjRKiK8tE4EkWLiTmQqNXSrL7nY3e%2FHLv7NrPTCOqi%2BaSsf7to1vyPnz2lCsYXGEwIKbHAFG6eHXiGMZApINfbDgxbMDCW9G4hTZAp5UArU2eCKRVyJb2y%2Ff9uP2%2B0L%2FnvSrjDUQR7HJK9wcd6aUpcezi0R4qg4NB2IIalESp%2BeliBbKz17Ho4UHzQ%2FKm5HdKyhYdULJUeuryApOAtDMGM1%2B9cNMV5boZUa4o%2FaYB3b%2BvcQ7ff52XTafbRbT51B4%2FWgtRbIIGZCsGd%2Bob%2BINEszW%2FHYb%2F%2FtSlwhy9rLdxhnSkS9hi8myt%2BfgE%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%2F)

Click here to show the solution

Set the images' `max-width` property to `100%` to contain the large image inside its box. If you use `width: 100%`, the small image will stretch.

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Sizing)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Backgrounds_and_borders)

## Help improve MDN

Was this page helpful to you?

YesNo

[Learn how to contribute](https://developer.mozilla.org/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Feb 3, 2026 by [MDN contributors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Sizing/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/learn_web_development/core/styling_basics/test_your_skills/sizing/index.md?plain=1 "Folder: en-us/learn_web_development/core/styling_basics/test_your_skills/sizing (Opens in a new tab)") • [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ftest_your_skills%2Fsizing%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FSizing%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ftest_your_skills%2Fsizing%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Fa623d4459e2aa00d17dc0fd6b6bc44f56c589950%0A*+Document+last+modified%3A+2026-02-03T12%3A46%3A45.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")

Filter sidebar

1. [Learn web development](https://developer.mozilla.org/en-US/docs/Learn_web_development)
2. [MDN curriculum](https://developer.mozilla.org/en-US/curriculum/)
3. [Getting started modules](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started)
4. [Environment setup](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Environment_setup)
5. [Your first website](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Your_first_website)
6. [Web standards](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards)
7. [Soft skills](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Soft_skills)
8. [Core modules](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core)
9. [Structuring content with HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content)
10. [CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
    
    1. [What is CSS?](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/What_is_CSS)
    2. [CSS getting started](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Getting_started)
    3. [Challenge: Biography page](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Styling_a_bio_page)
    4. [Basic selectors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors)
    5. [Attribute selectors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Attribute_selectors)
    6. [Pseudo-classes and elements](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Pseudo_classes_and_elements)
    7. [Combinators](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Combinators)
    8. [Test: Selectors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Selectors)
    9. [Box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)
    10. [Test: Box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model)
    11. [Handling conflicts](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts)
    12. [Test: Cascade](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade)
    13. [Challenge: Fixing blog styles](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles)
    14. [Values and units](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units)
    15. [Test: Values and units](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Values)
    16. [Sizing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Sizing)
    17. _[Test: Sizing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Sizing)_
    18. [Backgrounds and borders](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Backgrounds_and_borders)
    19. [Test: Backgrounds and borders](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Backgrounds_and_borders)
    20. [Overflow](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Overflow)
    21. [Test: Overflow](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Overflow)
    22. [Challenge: Sizing and decorating](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Size_decorate_content_panel)
    23. [Images, media, forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Images_media_forms)
    24. [Test: Images and forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Images)
    25. [Styling tables](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Tables)
    26. [Challenge: Styling color scheme search](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Home_color_scheme_search)
    27. [Debugging CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Debugging_CSS)
    28. [Test: Styling basics tests index](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills)
    29. Additional tutorials
    
11. [CSS text styling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Text_styling)
12. [CSS layout](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout)
13. [Dynamic scripting with JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting)
14. [JavaScript frameworks and libraries](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Frameworks_libraries)
15. [Accessibility](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility)
16. [Design for developers](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Design_for_developers)
17. [Version control](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Version_control)
18. [Extension modules](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions)
19. [Advanced JavaScript objects](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects)
20. [Client-side web APIs](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_APIs)
21. [Asynchronous JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS)
22. [Web forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms)
23. [Understanding client-side tools](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_tools)
24. [Server-side websites](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side)
25. [Web performance](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance)
26. [Testing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing)
27. Further resources
28. [How to solve common problems](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto)
29. [About](https://developer.mozilla.org/en-US/docs/Learn_web_development/About)
30. [Resources for educators](https://developer.mozilla.org/en-US/docs/Learn_web_development/Educators)
31. [Changelog](https://developer.mozilla.org/en-US/docs/Learn_web_development/Changelog)

[![MongoDB Atlas](https://developer.mozilla.org/pimg/aHR0cHM6Ly9zdGF0aWM0LmJ1eXNlbGxhZHMubmV0L3V1LzIvMTczOTc1LzE3NzQyODE2NzEtTUROXy1fMTQ1NngxODAucG5n.FxNud8HsbSMmNNOG1%2FNiQimNF2bptd1qCinx6cZcuH8%3D)](https://developer.mozilla.org/pong/click?code=aHR0cHM6Ly9zcnYuYnV5c2VsbGFkcy5jb20vYWRzL2NsaWNrL3gvR1RORDQyN1VDWUJJUDVRTkM2N0xZS1FVQ0FTSTQyN0lGVEJES1ozSkNBU0k1S0o3RlRCRDQyN0tDNjdJNDJRTENLQUQ0S1FMQ0E3SVAyN0lGNlNJS0szTkhFWUk1MjdOQ1lZSVQ1M0VDVE5DWUJaNTJL.WM0EQ9YqNUV%2FD0PTxDGGzfFIBPriRD0qR8VuXKwMg2g%3D&version=2)[Ad](https://developer.mozilla.org/en-US/advertising)

[](https://developer.mozilla.org/)

Your blueprint for a better internet.

- [](https://github.com/mdn/)
- [](https://bsky.app/profile/developer.mozilla.org)
- [](https://x.com/mozdevnet)
- [](https://mastodon.social/@mdn)
- [](https://developer.mozilla.org/en-US/blog/rss.xml)

MDN

- [About](https://developer.mozilla.org/en-US/about)
- [Blog](https://developer.mozilla.org/en-US/blog/)
- [Mozilla careers](https://www.mozilla.org/en-US/careers/listings/) 
- [Advertise with us](https://developer.mozilla.org/en-US/advertising)
- [MDN Plus](https://developer.mozilla.org/en-US/plus)
- [Product help](https://support.mozilla.org/products/mdn-plus) 

Contribute

- [MDN Community](https://developer.mozilla.org/en-US/community)
- [Community resources](https://developer.mozilla.org/en-US/docs/MDN/Community)
- [Writing guidelines](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines)
- [MDN Discord](https://developer.mozilla.org/discord) 
- [MDN on GitHub](https://github.com/mdn) 

Developers

- [Web technologies](https://developer.mozilla.org/en-US/docs/Web)
- [Learn web development](https://developer.mozilla.org/en-US/docs/Learn_web_development)
- [Guides](https://developer.mozilla.org/en-US/docs/MDN/Guides)
- [Tutorials](https://developer.mozilla.org/en-US/docs/MDN/Tutorials)
- [Glossary](https://developer.mozilla.org/en-US/docs/Glossary)
- [Hacks blog](https://hacks.mozilla.org/) 

[](https://www.mozilla.org/)

- [Website Privacy Notice](https://www.mozilla.org/privacy/websites/)
- [Telemetry Settings](https://www.mozilla.org/en-US/privacy/websites/data-preferences/)
- [Legal](https://www.mozilla.org/about/legal/terms/mozilla)
- [Community Participation Guidelines](https://www.mozilla.org/about/governance/policies/participation/)

Visit [Mozilla Corporation’s](https://www.mozilla.org/) not-for-profit parent, the [Mozilla Foundation](https://foundation.mozilla.org/).  
Portions of this content are ©1998–2026 by individual mozilla.org contributors. Content available under [a Creative Commons license](https://developer.mozilla.org/docs/MDN/Writing_guidelines/Attrib_copyright_license).