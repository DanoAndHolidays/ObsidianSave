# Test your skills: The Cascade

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles)

The aim of this skill test is to help you assess whether you understand universal property values for [controlling inheritance in CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts).

**Note:** To get help, read our [Test your skills](https://developer.mozilla.org/en-US/docs/Learn_web_development#test_your_skills) usage guide. You can also reach out to us using one of our [communication channels](https://developer.mozilla.org/en-US/docs/MDN/Community/Communication_channels).

## [Cascade 1](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade#cascade_1)

In this task, we want you to use one of the special values we looked at in the [controlling inheritance](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts#controlling_inheritance) section.

To complete the task, write a declaration in a new rule that will reset the background color back to white, without using an actual color value.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=eafeccc2ef72072d95649a8aa7b8f37407621eea&state=jY%2B%2FTsQwDMZfxfKtLYWBJeT6CiyMWdIktOZcp0rTHuh0745SejcwIAbL%2F76fPvuCQx4ZFWpPKzi283w06KJkSxKSQSB%2FNBiXXJrWCMDfShK5KwH0wnsFoJnumNjVYKstDCm8Hw0eDLavEnRjW90w%2FZt5O8dfjG52S914Wlsjt4wVunlGhYftGShfLAwPYlewcClIZ92pT3ERX7vIMSmY4tmH1PESXopgst6T9Aqep89t4Gme2H4pIGGSUHcc3WnbjDb1JHUXc46jgqfHjbgaMVKcSzDdjHe3FLrgnJ2WNHH4UWOFH%2BVorDAPYQyokKkfMl6%2FAQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=eafeccc2ef72072d95649a8aa7b8f37407621eea&state=jY%2B%2FTsQwDMZfxfKtLYWBJeT6CiyMWdIktOZcp0rTHuh0745SejcwIAbL%2F76fPvuCQx4ZFWpPKzi283w06KJkSxKSQSB%2FNBiXXJrWCMDfShK5KwH0wnsFoJnumNjVYKstDCm8Hw0eDLavEnRjW90w%2FZt5O8dfjG52S914Wlsjt4wVunlGhYftGShfLAwPYlewcClIZ92pT3ERX7vIMSmY4tmH1PESXopgst6T9Aqep89t4Gme2H4pIGGSUHcc3WnbjDb1JHUXc46jgqfHjbgaMVKcSzDdjHe3FLrgnJ2WNHH4UWOFH%2BVorDAPYQyokKkfMl6%2FAQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

```
<div class="container" id="outer">
  <div class="container" id="inner">
    <ul>
      <li class="nav"><a href="#">One</a></li>
      <li class="nav"><a href="#">Two</a></li>
    </ul>
  </div>
</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=eafeccc2ef72072d95649a8aa7b8f37407621eea&state=jY%2B%2FTsQwDMZfxfKtLYWBJeT6CiyMWdIktOZcp0rTHuh0745SejcwIAbL%2F76fPvuCQx4ZFWpPKzi283w06KJkSxKSQSB%2FNBiXXJrWCMDfShK5KwH0wnsFoJnumNjVYKstDCm8Hw0eDLavEnRjW90w%2FZt5O8dfjG52S914Wlsjt4wVunlGhYftGShfLAwPYlewcClIZ92pT3ERX7vIMSmY4tmH1PESXopgst6T9Aqep89t4Gme2H4pIGGSUHcc3WnbjDb1JHUXc46jgqfHjbgaMVKcSzDdjHe3FLrgnJ2WNHH4UWOFH%2BVorDAPYQyokKkfMl6%2FAQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

```
#outer div ul .nav a {
  background-color: powderblue;
  padding: 5px;
  display: inline-block;
  margin-bottom: 10px;
}

div div li a {
  color: rebeccapurple;
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=8af4ea8c02144ee562bf521246aa7d633ce247da&state=jZDBTsMwDIZfxfKuHYUDl5D1FbhwzCVNQmvmOlWadqBp747SdTsggThEseP%2F0%2B8%2FZ%2BzzwKhQe1rAsZ2mg0EXJVuSkAwC%2BYPBOOfSNEYA%2FlaSyF0JoGfeKgDNdMfELgYbbaFP4f1gcGeweZWga9vomunfzNsp%2FmB0vVnq2tPSGLndWKGbJlS4W8NASTEzPIhdwMK5IK11xy7FWfzeRY5JwRhPPqSW5%2FBSBKP1nqRT8Dx%2Brg%2BeppHtlwISJgn7lqM7rpPBpo5k38ac46Dg6XElLkaMFOdymG7Gm1sKbXDOjnMaOVzV27K79Vt%2F35OkD4nylcEKP0pQrDD3YQiokKnrM16%2BAQ%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

Click here to show the solution

One possible solution is as follows:

There are two things you need to do in this task. First, write a selector for the `a` element which is more specific than the selector used to turn the background powderblue. In this solution, this is achieved by using the `id` selector, which has very high specificity.

Then you need to remember there are special keyword values for all properties. In this case, using `inherit` sets the background color back to be the same as its parent element.

## [Cascade 2](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade#cascade_2)

To complete this task, manipulate the cascade layer order to color the links `rebeccapurple`. No editing the `lightgreen` declaration!

This task is a stretch goal — it requires knowledge of cascade layers, which we didn't cover in the [Handling conflicts](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts) article. You can find the information you need to attempt this task at [Cascade layers > Determining the precedence based on the order of layers](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Cascade_layers#determining_the_precedence_based_on_the_order_of_layers).

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=95bd478f09680cbff8e4c28c8492ee810e60e262&state=jZBNTsMwEIWvMppuUwILNq4b9QZsWHrjOiYZmIwjx0mJqtwdpUmLKBJiYfln3jfPb85Yp4ZRoS5pAMe26%2FYGXZBkSXw0CFTuDYY%2BzZfCCMDfShK5KQF0z%2BsJQDPdMLGDwUJbqKN%2F2xvcGCxexOvcFjpn%2Bjfzegp3jM5XS52XNBRGrjtm6LoOFR7Yjj7C6JnDKYO2jy37DKroveyMGPkhgPPcbHMZAMzJe4YHsQPYpQLQ2rIkqRQ8t5%2B75amkrmU7KiBhEr89cnAfa62xsSLZHkNKoVHw9LhSk5Hp5r18anGYTefF9O3pAoeoIPqjd84u6t9dLpEW5J5kqup0jXzFMMP3eUKYYap941HhRYfTFw%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=95bd478f09680cbff8e4c28c8492ee810e60e262&state=jZBNTsMwEIWvMppuUwILNq4b9QZsWHrjOiYZmIwjx0mJqtwdpUmLKBJiYfln3jfPb85Yp4ZRoS5pAMe26%2FYGXZBkSXw0CFTuDYY%2BzZfCCMDfShK5KQF0z%2BsJQDPdMLGDwUJbqKN%2F2xvcGCxexOvcFjpn%2Bjfzegp3jM5XS52XNBRGrjtm6LoOFR7Yjj7C6JnDKYO2jy37DKroveyMGPkhgPPcbHMZAMzJe4YHsQPYpQLQ2rIkqRQ8t5%2B75amkrmU7KiBhEr89cnAfa62xsSLZHkNKoVHw9LhSk5Hp5r18anGYTefF9O3pAoeoIPqjd84u6t9dLpEW5J5kqup0jXzFMMP3eUKYYap941HhRYfTFw%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

```
<div class="container" id="outer">
  <div class="container" id="inner">
    <ul>
      <li class="nav"><a href="#">One</a></li>
      <li class="nav"><a href="#">Two</a></li>
    </ul>
  </div>
</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=95bd478f09680cbff8e4c28c8492ee810e60e262&state=jZBNTsMwEIWvMppuUwILNq4b9QZsWHrjOiYZmIwjx0mJqtwdpUmLKBJiYfln3jfPb85Yp4ZRoS5pAMe26%2FYGXZBkSXw0CFTuDYY%2BzZfCCMDfShK5KQF0z%2BsJQDPdMLGDwUJbqKN%2F2xvcGCxexOvcFjpn%2Bjfzegp3jM5XS52XNBRGrjtm6LoOFR7Yjj7C6JnDKYO2jy37DKroveyMGPkhgPPcbHMZAMzJe4YHsQPYpQLQ2rIkqRQ8t5%2B75amkrmU7KiBhEr89cnAfa62xsSLZHkNKoVHw9LhSk5Hp5r18anGYTefF9O3pAoeoIPqjd84u6t9dLpEW5J5kqup0jXzFMMP3eUKYYap941HhRYfTFw%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

```
@layer yellow, purple, green;

@layer yellow {
  #outer div ul .nav a {
    padding: 5px;
    display: inline-block;
    margin-bottom: 10px;
  }
}
@layer purple {
  div div li a {
    color: rebeccapurple;
  }
}
@layer green {
  a {
    color: lightgreen;
  }
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=7627dae20b185b36ca996ecceb28f8ef3f5feb13&state=jZDLTsMwEEV%2FZTTdpgQWbFw34g%2FYsPTGcUwyMBlHjpNSVf13lAcBukAsLD%2FunLlzfcEmtYwKdUUjOLZ9fzTogiRL4qNBoOpoMAxpuhRGAP6uJJGtEkAPvJ4ANNOGiR0NFtpCE%2F3r0eDOYPEsXue20DnTv5mXU7hhdL5a6ryisTDytWOGru9R4RPbs49w9szhlEEdvZcMuiF27A9GfslwmVrt5vgw5R4Y7sSOYBcFoLNVRVIreOw%2BDstTRX3H9qyAhEn8vuTg3lettbEm2ZchpdAqeLhfqauR6%2Ba9zLI4TKbTYvr2dIFDVBB96Z2z2%2BQ3XeZgC3JLMtVNmvUfGGb4Nv0PZpga33pUONfh9RM%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%2F)

Click here to show the solution

One possible solution is as follows:

There is one thing you need to do in this task: change the order of precedence so the declaration for the desired color is in the last declared layer, which is what this solution shows.

You need to remember that unlayered normal styles take precedence over layered normal styles. But, if all styles are within layers — as in the case of this task — styles in later declared layers take precedence over styles declared in earlier layers. Moving the purple layer to the end means it has precedence over the green and yellow layers.

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles)

## Help improve MDN

Was this page helpful to you?

YesNo

[Learn how to contribute](https://developer.mozilla.org/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Feb 3, 2026 by [MDN contributors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/learn_web_development/core/styling_basics/test_your_skills/cascade/index.md?plain=1 "Folder: en-us/learn_web_development/core/styling_basics/test_your_skills/cascade (Opens in a new tab)") • [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ftest_your_skills%2Fcascade%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FCascade%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ftest_your_skills%2Fcascade%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Fa623d4459e2aa00d17dc0fd6b6bc44f56c589950%0A*+Document+last+modified%3A+2026-02-03T12%3A46%3A45.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")

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
    12. _[Test: Cascade](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade)_
    13. [Challenge: Fixing blog styles](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles)
    14. [Values and units](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units)
    15. [Test: Values and units](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Values)
    16. [Sizing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Sizing)
    17. [Test: Sizing](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Sizing)
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

[![MongoDB Atlas](https://developer.mozilla.org/pimg/aHR0cHM6Ly9zdGF0aWM0LmJ1eXNlbGxhZHMubmV0L3V1LzIvMTczOTc1LzE3NzQyODE2NzEtTUROXy1fMTQ1NngxODAucG5n.FxNud8HsbSMmNNOG1%2FNiQimNF2bptd1qCinx6cZcuH8%3D)](https://developer.mozilla.org/pong/click?code=aHR0cHM6Ly9zcnYuYnV5c2VsbGFkcy5jb20vYWRzL2NsaWNrL3gvR1RORDQyN1VDWUJJUDVRTkM2N0xZS1FVQ0FTSTQyN0lGVEJES1ozSkNBU0k1S0o3RlRCRDQyN0tDV1NJQzI3SUZUWURWSzNKQ1ZTRENLM1dDV1NERUtKS0M2U0k1MkpOQzZZREVLM0VISk5DTFNJWg%3D%3D.NV%2BIh%2FIo8pznmZG5xwnQLOhBM1OtEpWh5iekrlPIQWE%3D&version=2)[Ad](https://developer.mozilla.org/en-US/advertising)

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