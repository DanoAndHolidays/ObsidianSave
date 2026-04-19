# Test your skills: The box model

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts)

The aim of this skill test is to help you assess whether you understand the [CSS box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model).

**Note:** To get help, read our [Test your skills](https://developer.mozilla.org/en-US/docs/Learn_web_development#test_your_skills) usage guide. You can also reach out to us using one of our [communication channels](https://developer.mozilla.org/en-US/docs/MDN/Community/Communication_channels).

## [Interactive challenge](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model#interactive_challenge)

First of all, we are giving you a fun, interactive challenge involving margin shorthand, created by our [learning partner](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Learning_content#partner_links_and_embeds), [Scrimba](https://scrimba.com/home).

Watch the embedded scrim, and complete the tasks on the timeline (the little ghost icons) by following the instructions and editing the code. When you are done, you can resume watching the scrim to check how the teacher's solution matches up with yours.

Clicking will load content from scrimba.com

Toggle fullscreen[

Open on Scrimba](https://scrimba.com/learn-html-and-css-c0p/~01s?via=mdn&embed=)

# Margin shorthand

Load scrim and open dialog.

## [Box model 1](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model#box_model_1)

In this task, there are two boxes below, one is using the standard box model, the other the alternate box model. We'd like you to change the width of the second box by adding declarations to the `.alternate` class, so that it matches the visual width of the first box.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=6db4707d7d2170f6febb7175393f98577fc1827a&state=bY9LcoMwEESvMjVrwCYJG%2Fmzzx20kdAYlIgRJQkHx8XdU8jOt7J90%2FOq%2B4p9GhwK3Bt7htapGA8StZ8lHp9higSpJ4hJsVHBgPYzDN6Qq%2FYbY89HyX%2F%2FQLlEgVWiX4Yv%2Bo8CC2xjRIHamwtcJQOcPCcBdfVAA2ygrhqIimMZKdjTTvIiuVo9Oat9MBQENOMM0TtrIJCmtlXjFEZHu5xR7WsX%2FMSmbL3zQYCzXZ%2B6oC75PipjLHcCnrbjnMmgQmf5B3izJvUCHrefoKdVIaBubmSRLLn6HnovN5fRvmf3rWip%2FT2NBb6ss7HA1NNAKDC3wuUD&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=6db4707d7d2170f6febb7175393f98577fc1827a&state=bY9LcoMwEESvMjVrwCYJG%2Fmzzx20kdAYlIgRJQkHx8XdU8jOt7J90%2FOq%2B4p9GhwK3Bt7htapGA8StZ8lHp9higSpJ4hJsVHBgPYzDN6Qq%2FYbY89HyX%2F%2FQLlEgVWiX4Yv%2Bo8CC2xjRIHamwtcJQOcPCcBdfVAA2ygrhqIimMZKdjTTvIiuVo9Oat9MBQENOMM0TtrIJCmtlXjFEZHu5xR7WsX%2FMSmbL3zQYCzXZ%2B6oC75PipjLHcCnrbjnMmgQmf5B3izJvUCHrefoKdVIaBubmSRLLn6HnovN5fRvmf3rWip%2FT2NBb6ss7HA1NNAKDC3wuUD&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

```
<div class="box">I use the standard box model.</div>
<div class="box alternate">I use the alternate box model.</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=6db4707d7d2170f6febb7175393f98577fc1827a&state=bY9LcoMwEESvMjVrwCYJG%2Fmzzx20kdAYlIgRJQkHx8XdU8jOt7J90%2FOq%2B4p9GhwK3Bt7htapGA8StZ8lHp9higSpJ4hJsVHBgPYzDN6Qq%2FYbY89HyX%2F%2FQLlEgVWiX4Yv%2Bo8CC2xjRIHamwtcJQOcPCcBdfVAA2ygrhqIimMZKdjTTvIiuVo9Oat9MBQENOMM0TtrIJCmtlXjFEZHu5xR7WsX%2FMSmbL3zQYCzXZ%2B6oC75PipjLHcCnrbjnMmgQmf5B3izJvUCHrefoKdVIaBubmSRLLn6HnovN5fRvmf3rWip%2FT2NBb6ss7HA1NNAKDC3wuUD&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

```
body {
  font: 1.2em / 1.5 sans-serif;
}
.box {
  border: 5px solid rebeccapurple;
  background-color: lightgray;
  padding: 40px;
  margin: 40px;
  width: 300px;
  height: 150px;
}

.alternate {
  box-sizing: border-box;
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=ce4b8011a92ab4d10006e270ef6c750448c90dc5&state=jZDLUsMwDEV%2FRaN1kjZAFriPPf%2FgjWOricGRM7ZTUjr5dyZpaYFhwfbo6uhxxjZ1DgVujT2CdirGncTajxL3LzBEgtQSxKTYqGCg9iN03pArtitjj3vJv%2FtAuUSBVaIfhhv9Q4EZ6hhRYO3NCc6SAQ6ek4CyeKAOVlAWFUTFMY8U7GEjeZJczJ4lW%2FtgKAio%2BhGid9ZAoJq0Vv0QekebJaP0WxP8wCbX3vkgwNmmTU1Qp6XeK2MsNwKe1v24kE6FxvI38G5NagU8rr9AS7NCQFldyCRZcnE%2F9LrcmEf7sbgvi%2Ba1v6b%2Fnb0Pf76Nwgxf559hhqmljlDgchJOnw%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

Click here to show the solution

You will need to increase the width of the second block to add the size of the padding and border:

## [Box model 2](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model#box_model_2)

To complete this task, add the following features to the provided box:

- A `5px`, black, dotted border.
- A top margin of `20px`.
- A right margin of `1em`.
- A bottom margin of `40px`.
- A left margin of `2em`.
- Padding on all sides of `1em`.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=f3d7bac820db54360f58db5407f4fcde219caa1a&state=HcxBDoIwEAXQq0z%2BGkswcVORvXfoptBia9ppwlSCIdzd4PJt3o5Qc4JG7%2BJKU7IiD4OxbAbDkz7iqQZPUi07uzgay0a5OJ9U37q4DobRYBKBxljcl3bDRHPhqqlTV5%2BppU7dSCzLRfwS57vhw7BhdU77H2jwPgM0qMFnD40UX6Hi%2BAE%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=f3d7bac820db54360f58db5407f4fcde219caa1a&state=HcxBDoIwEAXQq0z%2BGkswcVORvXfoptBia9ppwlSCIdzd4PJt3o5Qc4JG7%2BJKU7IiD4OxbAbDkz7iqQZPUi07uzgay0a5OJ9U37q4DobRYBKBxljcl3bDRHPhqqlTV5%2BppU7dSCzLRfwS57vhw7BhdU77H2jwPgM0qMFnD40UX6Hi%2BAE%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

```
<div class="box">I use the standard box model.</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=f3d7bac820db54360f58db5407f4fcde219caa1a&state=HcxBDoIwEAXQq0z%2BGkswcVORvXfoptBia9ppwlSCIdzd4PJt3o5Qc4JG7%2BJKU7IiD4OxbAbDkz7iqQZPUi07uzgay0a5OJ9U37q4DobRYBKBxljcl3bDRHPhqqlTV5%2BppU7dSCzLRfwS57vhw7BhdU77H2jwPgM0qMFnD40UX6Hi%2BAE%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

```
body {
  font: 1.2em / 1.5 sans-serif;
}

.box {
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=b7b588b537cf85b9389a59423ce6514058483133&state=NY47bsMwEESvMthakSPBbmjHfe7AhtSuJSb8CCRjKBB8d4MO0r3BA2Zmp6UGT4ou7O6YvCnlQ5NNm6brJ36KoC6CUk1kkxk2bQiJxfeXA7v7VUfqaCqFFNnEv9h1BG4pVoWhHyXggKE%2FoZhY3opkdzvr%2BNBRx7417a%2Fwj4BNmSUrnNYNnGoVhvVm%2Bj43GUyeXVQY39cNgwQcG4wSXnY1zC7Oqpm%2FDeroq%2F2ijuoiQUiRd%2FNS6fEE&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

Click here to show the solution

This task involves using the margin, border, and padding properties correctly. You might choose to use the longhand properties ([`margin-top`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-top), [`margin-right`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-right), etc.); however, when setting a margin and padding on all sides, the shorthand is probably the better choice:

## [Box model 3](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model#box_model_3)

In this task, the inline element has a margin, padding, and border. However, the lines above and below are overlapping it.

To complete this task, update the CSS to cause the size of the margin, padding, and border to be respected by the other lines, while still keeping the element inline.

The starting point of the task looks like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=03b9de98337cc213c7f753f75d352168d636d66c&state=VZGxbtwwEER%2FZcD6rMMFcCNfrgrgNlWqa5bknsSI5ApcUj7b8L8HkuwgqUhghrNvlu9mrCma3px9WOAiqX6%2FGiv3q7lcM3CetwP4xcMQWMEKK7kpFrFBDzjrTPkyFwnZMxZRzKK1RTkfNwWs2hISDUH3pEnGWMgGvHDUEZKDZHgKk2RQokK5jqhUVQKqJKohRkHiuOpvbQqwTHnPGqjE4LqN9Lii%2Fsf83JIVWOaKoTBnhZOSoTIJOPuwMIbNMkgrvsNPKhr5FTpSjFLhpJWBa%2BU97pNpZoLORVpV3GihDQdOYqTivwZ5yp7j2kymQnihiRLvdaTb4378tbjmWrJcwFTqmFvdZsxM63WjfWvOjSGHf5qejz4sl2s2B%2BNUTW%2Bs%2BFe8r4ab5Nrj1H3jhCNO3SOUsj4ol3B7uuaPdU2dlTvWH9qfWHLTUKRl%2F%2BAkSukxhzw9bZIUz6XH43yHSgweNpLbtZm8D3noceK0J5uD%2Bb3SmIOpIyc2vYlhGKv5%2BAM%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

Here's the underlying code for this starting point:

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=03b9de98337cc213c7f753f75d352168d636d66c&state=VZGxbtwwEER%2FZcD6rMMFcCNfrgrgNlWqa5bknsSI5ApcUj7b8L8HkuwgqUhghrNvlu9mrCma3px9WOAiqX6%2FGiv3q7lcM3CetwP4xcMQWMEKK7kpFrFBDzjrTPkyFwnZMxZRzKK1RTkfNwWs2hISDUH3pEnGWMgGvHDUEZKDZHgKk2RQokK5jqhUVQKqJKohRkHiuOpvbQqwTHnPGqjE4LqN9Lii%2Fsf83JIVWOaKoTBnhZOSoTIJOPuwMIbNMkgrvsNPKhr5FTpSjFLhpJWBa%2BU97pNpZoLORVpV3GihDQdOYqTivwZ5yp7j2kymQnihiRLvdaTb4378tbjmWrJcwFTqmFvdZsxM63WjfWvOjSGHf5qejz4sl2s2B%2BNUTW%2Bs%2BFe8r4ab5Nrj1H3jhCNO3SOUsj4ol3B7uuaPdU2dlTvWH9qfWHLTUKRl%2F%2BAkSukxhzw9bZIUz6XH43yHSgweNpLbtZm8D3noceK0J5uD%2Bb3SmIOpIyc2vYlhGKv5%2BAM%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

```
<div class="box">
  <p>
    Veggies es bonus vobis, <span>proinde vos postulo</span> essum magis
    kohlrabi welsh onion daikon amaranth tatsoi tomatillo melon azuki bean
    garlic.
  </p>

  <p>
    Gumbo beet greens corn soko endive gumbo gourd. Parsley shallot courgette
    tatsoi pea sprouts fava bean collard greens dandelion okra wakame tomato.
    Dandelion cucumber earthnut pea peanut soko zucchini.
  </p>
</div>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=03b9de98337cc213c7f753f75d352168d636d66c&state=VZGxbtwwEER%2FZcD6rMMFcCNfrgrgNlWqa5bknsSI5ApcUj7b8L8HkuwgqUhghrNvlu9mrCma3px9WOAiqX6%2FGiv3q7lcM3CetwP4xcMQWMEKK7kpFrFBDzjrTPkyFwnZMxZRzKK1RTkfNwWs2hISDUH3pEnGWMgGvHDUEZKDZHgKk2RQokK5jqhUVQKqJKohRkHiuOpvbQqwTHnPGqjE4LqN9Lii%2Fsf83JIVWOaKoTBnhZOSoTIJOPuwMIbNMkgrvsNPKhr5FTpSjFLhpJWBa%2BU97pNpZoLORVpV3GihDQdOYqTivwZ5yp7j2kymQnihiRLvdaTb4378tbjmWrJcwFTqmFvdZsxM63WjfWvOjSGHf5qejz4sl2s2B%2BNUTW%2Bs%2BFe8r4ab5Nrj1H3jhCNO3SOUsj4ol3B7uuaPdU2dlTvWH9qfWHLTUKRl%2F%2BAkSukxhzw9bZIUz6XH43yHSgweNpLbtZm8D3noceK0J5uD%2Bb3SmIOpIyc2vYlhGKv5%2BAM%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

```
body {
  font: 1.2em / 1.5 sans-serif;
}

.box span {
  background-color: pink;
  border: 5px solid black;
  padding: 1em;
}
```

The updated styling should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=0aed96d849f3de65ba8c52661f25e2ab86d0639f&state=tZG9jtswEIRfZcDaP3CAa3SOqwBpU6VysyTXEiOSK3BJnX0Hv3sgKQmSB0hFAjOc%2FWb5YYaaounM2YcZLpLq56uxcr%2BayzUD52k9gO%2Fc94EVrLCSm2IWG3SHs06UL1ORkD1jFsUkWluU83FVwKotIVEfdEsaZYiFbMAbRx0gOUiGpzBKBiUqlOuASlUloEqiGmIUJI6L%2Ft7GAMuUt6yeSgzusJIeF9R%2FmL%2B2ZAWWuaIvzFnhpGSojALOPsyMfrX00oo%2F4BsVjfyADhSjVDhppedaeYv7xTQxQacirSpuNNOKAycxUvG%2FB3nKnuPSTMZCeKOREm915LDFffljcc21ZLmAqdQht7rOmJiW60r73pwbQg5%2FNT0ffZgv12x2xqmazljxD3wshpvk2uF0%2BMQJR5wOL1DKulcu4fZ6zc9lTQcrdyw%2FtD2x5Ma%2BSMt%2B7yRK6TCFPL6ukhTPpcPLdIdKDB42ktu0ibwPue9w4rQl%2F5dcwAedIj06hBxD5r2Nslqf6wJ%2BLP3NztSBE5vOxNAP1Tx%2FAg%3D%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%2F)

Click here to show the solution

Solving this task requires you to understand when to use different [`display`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display) values. After adding `display: inline-block`, the block direction margin, border and padding will cause the other lines to be pushed away from the element:

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts)

## Help improve MDN

Was this page helpful to you?

YesNo

[Learn how to contribute](https://developer.mozilla.org/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Feb 3, 2026 by [MDN contributors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/learn_web_development/core/styling_basics/test_your_skills/box_model/index.md?plain=1 "Folder: en-us/learn_web_development/core/styling_basics/test_your_skills/box_model (Opens in a new tab)") • [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ftest_your_skills%2Fbox_model%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FTest_your_skills%2FBox_model%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ftest_your_skills%2Fbox_model%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Fa623d4459e2aa00d17dc0fd6b6bc44f56c589950%0A*+Document+last+modified%3A+2026-02-03T12%3A46%3A45.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")

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
    10. _[Test: Box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Box_model)_
    11. [Handling conflicts](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts)
    12. [Test: Cascade](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade)
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