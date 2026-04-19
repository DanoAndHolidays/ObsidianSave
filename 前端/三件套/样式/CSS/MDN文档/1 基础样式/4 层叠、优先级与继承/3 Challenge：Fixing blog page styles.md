# Challenge: Fixing blog page styles

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units)

In this challenge we give you a basic blog page example that is partially styled. We need you to fix some problems with the existing CSS and add some styles to finish it off. Along the way we will test your knowledge of selectors, the box model, and conflicts/cascade.

## [Starting point](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles#starting_point)

To begin, click the **Play** button in one of the code panels below to open the provided example in the MDN Playground. You'll then follow the instructions in the [Project brief](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles#project_brief) section to style the page appropriately.

htmlCopy[Play](https://developer.mozilla.org/en-US/play?uuid=25b19198ef6a80728d5a3b6be0d2c464c2fb8536&state=lVhdbiPHEb5KZYIAyUIkRSGLGPSIgO1sYBvJeoEF8sSXYk9xpqz%2BGXVXU5SNPUPOkRvkORfKFYLu%2BeGMJGrXD4I0093VVV999VWNfi0aMbrYFOXvKqfksSVIL7Y7W6bfoNHWt7uC7K7Y7ixA2RBW%2BS%2BA0pAgqAZ9ILndFVEOi692BayGdWHRtP3Iv7CtAWGvXQ0t1pTOaE22pnLV7ekPaLZ30Hg63O6KII%2BaliqEXQGe9PAmNEQyXlKuRn%2FKvaseB0PpLfn%2BKT2vt9%2BAcUGATorS3ZLdKVfN%2BrzL4nF8ACijnjxl77YlDu79fldsv3eGyhVuy5Xmz2z9Nl%2F2RVu%2F2bsoX7j3O2cF1Uu7y9XE%2FXJ1Dq2DbASnNMj2vDGQEnYWuLrdFWzFuyrmN7sClMYQbndFw3WjuW6k58SA8c32p%2BjB0gMFgdYFKVfNzXRHO4vm7%2Bg8kYB2ngyo6JFAk5IYYK%2FRViygnI17RjiShkCmJQ%2B6P6WcrSNN7aGAoGLh5QyzGV4fGgykdQzQoEo2Urwk0QOjipoDVJETmhCwZbLD66nFdDJq8ayYAmSfYvJ6CR9jUNyygEERDqBRxTA4zhZa5wWnptrRneC0ZsUSK7bAbYgGDuQNWYlmui17tYQfrKJW3MwvEkYDrUZFHiVfJizOw4Et72MAjCo9pjWNQggN2cqTZwEkS2in1gacSfOQIlexW04Z1k4I1hPnGZOeMOTdKWXI1gl7Ifs5iuR7Ozgqp52HkJw1JFez5GHFLQeV7CZ%2FryBQBZWbocMxGFeBkGldyobiiqtoBaKAxr3zBCTdLQQGa4uAmu8jLuGDdzwDR5xPSLbRx%2FCEYT20yU%2BKwFUmk%2BXAoFMyEDTvybsZR9%2FTfSQ4Rt1GQaEutPuIAqhytICxjjSWhcETm5TQ5B%2FJ1FRXFkv40KAn8al0gvA%2B6kQjFyJ5AucterpcJAeMKhPmEIMiqFhJNCGLDDivuGdLiu%2BAijUHDhBnbhydjtJiKlNjXOUgkO1Ku8OsYUMWyQU4oElV5NlwSN4fUacyTIhd4NrLyvyMKi%2Bq50WkX9x9VotzLRrUFCJW%2BOKJ76LHPSdK9lV%2FJEsWhcOL2%2F8ak0r0wCRx6JXjNS1%2FViSvejnRDkvpmi6bQwoHtZhVSk1BMGTivSKlP2UW9ZI7hNsVqXgOkqiZKWOc3%2FMSPpIBTbOalFyFqQZ7Jg9mKA6oBEWaPIeUtvvISWSx5qyuRz6iiTMJNG4kz%2FA3WZ5KaS9rl6nV3Gz%2FkbXgNwnV5bwPgRz5SN4j0GksKLBRaxyqeQb1h64ehqZEmnr%2Fh454oFgzyuSeDvpOKFBNjQ2yka8zSVOeSNZIEYm%2BTezD7XhBB%2BPMuUusBU6hV0wy5KZ3Z1C%2B7gh6FWf2foxBXNLU%2B5jmsnaUrkFEsBpj2POebBXNZV6iUtEEtGBJdd1Leexi6vr0IDadVtQej1zNunKecwYlvUiUOQH%2BSQ2rqLHvwueEDc0387BKyA3IDtJ4bl4vtJh5bH3zSlGlgJbwbkjQrB02iYtoZ1XdpXYwe6F5noWxY1OfsReGoLNSn48v4T2a81BxOUUV15ZD4EzninukMjuV81lHGM1ZPJIkPe1yo%2FtpKknDVeh14TdPKN2sG6Ix6B%2B%2FaMz92O19XRLeSWb6gHg3QqEa2IcKQgwt2YpDGAffXKJL%2BP6FBJ41bA6mJjdpw9rtnZe%2Bhj2HeH41E8p%2BgujZv4R3kfN41LVjg6TI4rSihwZ%2BOaup3rLy5oml7b6yKCv3gXTv0pEFaTKUTM2xFarJ58KVLEhLeOddGAcXjYotpxrr13NLGH2WJ0GmxXS7weg5nCdj3zirsg6QcDR5WJww6nKEI%2Blz8X0Zz8rV5AOrPDgn5F%2BlWNlu%2F%2Fvv%2F%2F3nX3BzffMW3rv0WXu%2BoFx1Jvqv3%2F6bt1z1H%2B3FVaFCKDbF6g18i4EV5E96tGnwPQm8We3szqZT8GuycHBWNrBe3pCBFayXbyE8BiGziPx1Wn%2FgSppN8te0f%2FzzV9ft6Qr%2Bcv2HK1hfX1%2B3pz%2FlTQZ9zXYD14BR3Nc7%2Byld0qzPVywC%2F0IbuCEzrt48W10v357XsVtWSYY24KkaFzaNO5LvllNMi4qU85gg34B1loadqzfwHo9gyMY%2B7qi7YxWHVuPjBg6aTjmEFquKbb2B6%2FyoOcgi%2F7thkfAb7QL8HIPw4XHRTwUbCC0qWuxJHohs3lJju4H1dXsaHNHcx6rptIH1kxAvxTAGv9eo7vKLPaq72rtoq0W%2F9khau4faD3dnY6i5thtQqfz8PLypWzMkn5uuna7IeldN8Pwh%2FUMgs6mXyx7Y5UjkzlrHiIW4dkD0uf0K%2FV1IH0u1x8dpvMp5G1jfDfdOjM9Z0Ubf6mm6%2F9ZVV%2BdTX2rP%2FLnpIPhcyD2WocHKPWxg3Z7GnyEhn3K9%2FZzKrbgqpCFDxabInhaf%2Fg8%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FFixing_blog_styles%2F)

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Sizing a blog page challenge</title>
    <link href="style.css" rel="stylesheet" />
  </head>
  <body>
    <header>
      <h1>A most excellent blog</h1>
      <nav>
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">Blog</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
    </header>
    <main>
      <section id="introduction" class="highlight">
        <h2>Our newest post</h2>
        <p>
          Laoreet lorem curae lectus blandit conubia vel semper laoreet congue
          at taciti.
          <a href="#">Phasellus hac consectetur iaculis dui</a> sapien iaculis
          hac ultricies per luctus. Suscipit mattis lacus semper in porta
          phasellus sollicitudin ipsum fermentum phasellus sapien. Inceptos
          etiam placerat porttitor finibus auctor at platea hendrerit aenean
          laoreet elit lorem odio.
        </p>
      </section>
      <section>
        <h2>Exciting content</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Proin
          tortor purus <a href="#">platea sit eu id</a> nisi litora libero.
          Neque vulputate consequat ac amet augue blandit maximus aliquet
          congue. Pharetra vestibulum posuere ornare
          <a href="#">faucibus fusce dictumst</a> orci aenean eu facilisis ut
          volutpat commodo senectus purus himenaeos fames primis convallis nisi.
        </p>
        <ul>
          <li>Lorem ipsum dolor</li>
          <li>Neque vulputate consequat</li>
          <li>Phasellus fermentum malesuada</li>
          <li>Curabitur semper venenatis</li>
          <li>Duis lectus porta mattis</li>
        </ul>
        <p>
          Phasellus fermentum malesuada phasellus netus dictum aenean placerat
          egestas amet.
          <a href="#">Ornare taciti semper dolor tristique</a> morbi. Sem leo
          tincidunt aliquet semper eu lectus scelerisque quis. Sagittis vivamus
          mollis nisi mollis enim fermentum laoreet.
        </p>
        <h2>More exciting content</h2>
        <p>
          Curabitur semper venenatis lectus viverra ex dictumst nulla maximus.
          Primis iaculis elementum conubia feugiat venenatis dolor augue ac
          blandit nullam ac <a href="#">phasellus turpis</a> feugiat mollis.
          Duis lectus porta mattis imperdiet vivamus augue litora lectus arcu.
          Justo torquent pharetra volutpat ad blandit bibendum
          <a href="#">accumsan nec elit cras</a> luctus primis ipsum gravida
          class congue.
        </p>
        <p>
          Vehicula etiam elementum finibus enim duis feugiat commodo adipiscing
          tortor <a href="#">tempor elit</a>. Et mollis consectetur habitant
          turpis tortor consectetur adipiscing vulputate dolor lectus iaculis
          convallis adipiscing. Nam hendrerit
          <a href="#">dignissim condimentum ullamcorper diam</a> morbi eget
          consectetur odio in sagittis.
        </p>
      </section>
      <section id="summary" class="highlight">
        <h2>Summary</h2>
        <p>
          Et arcu tortor lorem ac primis ac suspendisse lectus nulla. Habitant
          fermentum <a href="#">leo facilisis lobortis</a> risus lobortis
          maximus gravida. Euismod fames maecenas imperdiet senectus
          <a href="#">nec nisi amet pellentesque felis</a> vitae vestibulum
          integer nec tellus. Eros posuere lacinia et tellus quis fames mattis
          quisque mauris placerat rhoncus pretium sed consectetur
          <a href="#">convallis</a>.
        </p>
      </section>
    </main>
    <footer class="highlight">
      <p>©️ 2025 Nobody</p>
    </footer>
  </body>
</html>
```

cssCopy[Play](https://developer.mozilla.org/en-US/play?uuid=25b19198ef6a80728d5a3b6be0d2c464c2fb8536&state=lVhdbiPHEb5KZYIAyUIkRSGLGPSIgO1sYBvJeoEF8sSXYk9xpqz%2BGXVXU5SNPUPOkRvkORfKFYLu%2BeGMJGrXD4I0093VVV999VWNfi0aMbrYFOXvKqfksSVIL7Y7W6bfoNHWt7uC7K7Y7ixA2RBW%2BS%2BA0pAgqAZ9ILndFVEOi692BayGdWHRtP3Iv7CtAWGvXQ0t1pTOaE22pnLV7ekPaLZ30Hg63O6KII%2BaliqEXQGe9PAmNEQyXlKuRn%2FKvaseB0PpLfn%2BKT2vt9%2BAcUGATorS3ZLdKVfN%2BrzL4nF8ACijnjxl77YlDu79fldsv3eGyhVuy5Xmz2z9Nl%2F2RVu%2F2bsoX7j3O2cF1Uu7y9XE%2FXJ1Dq2DbASnNMj2vDGQEnYWuLrdFWzFuyrmN7sClMYQbndFw3WjuW6k58SA8c32p%2BjB0gMFgdYFKVfNzXRHO4vm7%2Bg8kYB2ngyo6JFAk5IYYK%2FRViygnI17RjiShkCmJQ%2B6P6WcrSNN7aGAoGLh5QyzGV4fGgykdQzQoEo2Urwk0QOjipoDVJETmhCwZbLD66nFdDJq8ayYAmSfYvJ6CR9jUNyygEERDqBRxTA4zhZa5wWnptrRneC0ZsUSK7bAbYgGDuQNWYlmui17tYQfrKJW3MwvEkYDrUZFHiVfJizOw4Et72MAjCo9pjWNQggN2cqTZwEkS2in1gacSfOQIlexW04Z1k4I1hPnGZOeMOTdKWXI1gl7Ifs5iuR7Ozgqp52HkJw1JFez5GHFLQeV7CZ%2FryBQBZWbocMxGFeBkGldyobiiqtoBaKAxr3zBCTdLQQGa4uAmu8jLuGDdzwDR5xPSLbRx%2FCEYT20yU%2BKwFUmk%2BXAoFMyEDTvybsZR9%2FTfSQ4Rt1GQaEutPuIAqhytICxjjSWhcETm5TQ5B%2FJ1FRXFkv40KAn8al0gvA%2B6kQjFyJ5AucterpcJAeMKhPmEIMiqFhJNCGLDDivuGdLiu%2BAijUHDhBnbhydjtJiKlNjXOUgkO1Ku8OsYUMWyQU4oElV5NlwSN4fUacyTIhd4NrLyvyMKi%2Bq50WkX9x9VotzLRrUFCJW%2BOKJ76LHPSdK9lV%2FJEsWhcOL2%2F8ak0r0wCRx6JXjNS1%2FViSvejnRDkvpmi6bQwoHtZhVSk1BMGTivSKlP2UW9ZI7hNsVqXgOkqiZKWOc3%2FMSPpIBTbOalFyFqQZ7Jg9mKA6oBEWaPIeUtvvISWSx5qyuRz6iiTMJNG4kz%2FA3WZ5KaS9rl6nV3Gz%2FkbXgNwnV5bwPgRz5SN4j0GksKLBRaxyqeQb1h64ehqZEmnr%2Fh454oFgzyuSeDvpOKFBNjQ2yka8zSVOeSNZIEYm%2BTezD7XhBB%2BPMuUusBU6hV0wy5KZ3Z1C%2B7gh6FWf2foxBXNLU%2B5jmsnaUrkFEsBpj2POebBXNZV6iUtEEtGBJdd1Leexi6vr0IDadVtQej1zNunKecwYlvUiUOQH%2BSQ2rqLHvwueEDc0387BKyA3IDtJ4bl4vtJh5bH3zSlGlgJbwbkjQrB02iYtoZ1XdpXYwe6F5noWxY1OfsReGoLNSn48v4T2a81BxOUUV15ZD4EzninukMjuV81lHGM1ZPJIkPe1yo%2FtpKknDVeh14TdPKN2sG6Ix6B%2B%2FaMz92O19XRLeSWb6gHg3QqEa2IcKQgwt2YpDGAffXKJL%2BP6FBJ41bA6mJjdpw9rtnZe%2Bhj2HeH41E8p%2BgujZv4R3kfN41LVjg6TI4rSihwZ%2BOaup3rLy5oml7b6yKCv3gXTv0pEFaTKUTM2xFarJ58KVLEhLeOddGAcXjYotpxrr13NLGH2WJ0GmxXS7weg5nCdj3zirsg6QcDR5WJww6nKEI%2Blz8X0Zz8rV5AOrPDgn5F%2BlWNlu%2F%2Fvv%2F%2F3nX3BzffMW3rv0WXu%2BoFx1Jvqv3%2F6bt1z1H%2B3FVaFCKDbF6g18i4EV5E96tGnwPQm8We3szqZT8GuycHBWNrBe3pCBFayXbyE8BiGziPx1Wn%2FgSppN8te0f%2FzzV9ft6Qr%2Bcv2HK1hfX1%2B3pz%2FlTQZ9zXYD14BR3Nc7%2Byld0qzPVywC%2F0IbuCEzrt48W10v357XsVtWSYY24KkaFzaNO5LvllNMi4qU85gg34B1loadqzfwHo9gyMY%2B7qi7YxWHVuPjBg6aTjmEFquKbb2B6%2FyoOcgi%2F7thkfAb7QL8HIPw4XHRTwUbCC0qWuxJHohs3lJju4H1dXsaHNHcx6rptIH1kxAvxTAGv9eo7vKLPaq72rtoq0W%2F9khau4faD3dnY6i5thtQqfz8PLypWzMkn5uuna7IeldN8Pwh%2FUMgs6mXyx7Y5UjkzlrHiIW4dkD0uf0K%2FV1IH0u1x8dpvMp5G1jfDfdOjM9Z0Ubf6mm6%2F9ZVV%2BdTX2rP%2FLnpIPhcyD2WocHKPWxg3Z7GnyEhn3K9%2FZzKrbgqpCFDxabInhaf%2Fg8%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FFixing_blog_styles%2F)

```
/* Basic type and text */

body {
  font: 1.2em / 1.5 system-ui;
  width: clamp(480px, 70%, 1000px);
  margin: 0 auto;
}

h1 {
  font-size: 2em;
}

h2 {
  font-size: 1.5em;
}

a {
  color: red;
}

a:hover {
  text-decoration: none;
}

/* Nav menu */

ul {
  display: flex;
  padding: 0;
  list-style-type: none;
  justify-content: space-between;
  gap: 10px;
}

li {
  flex: 1;
}

a {
  text-decoration: none;
  color: black;
  background-color: yellowgreen;
  text-align: center;
  padding: 10px;
}

a:hover {
  background-color: goldenrod;
}

/* Intro and summary */

.highlight {
  margin-top: 0;
  background-color: darkslategray;
  color: cornsilk;
}

.highlight a {
  color: purple;
}

/* Footer */

footer {
  margin-top: 20px;
  background-color: goldenrod;
  text-shadow: 1px 1px 1px black;
}
```

[Play](https://developer.mozilla.org/en-US/play?uuid=25b19198ef6a80728d5a3b6be0d2c464c2fb8536&state=lVhdbiPHEb5KZYIAyUIkRSGLGPSIgO1sYBvJeoEF8sSXYk9xpqz%2BGXVXU5SNPUPOkRvkORfKFYLu%2BeGMJGrXD4I0093VVV999VWNfi0aMbrYFOXvKqfksSVIL7Y7W6bfoNHWt7uC7K7Y7ixA2RBW%2BS%2BA0pAgqAZ9ILndFVEOi692BayGdWHRtP3Iv7CtAWGvXQ0t1pTOaE22pnLV7ekPaLZ30Hg63O6KII%2BaliqEXQGe9PAmNEQyXlKuRn%2FKvaseB0PpLfn%2BKT2vt9%2BAcUGATorS3ZLdKVfN%2BrzL4nF8ACijnjxl77YlDu79fldsv3eGyhVuy5Xmz2z9Nl%2F2RVu%2F2bsoX7j3O2cF1Uu7y9XE%2FXJ1Dq2DbASnNMj2vDGQEnYWuLrdFWzFuyrmN7sClMYQbndFw3WjuW6k58SA8c32p%2BjB0gMFgdYFKVfNzXRHO4vm7%2Bg8kYB2ngyo6JFAk5IYYK%2FRViygnI17RjiShkCmJQ%2B6P6WcrSNN7aGAoGLh5QyzGV4fGgykdQzQoEo2Urwk0QOjipoDVJETmhCwZbLD66nFdDJq8ayYAmSfYvJ6CR9jUNyygEERDqBRxTA4zhZa5wWnptrRneC0ZsUSK7bAbYgGDuQNWYlmui17tYQfrKJW3MwvEkYDrUZFHiVfJizOw4Et72MAjCo9pjWNQggN2cqTZwEkS2in1gacSfOQIlexW04Z1k4I1hPnGZOeMOTdKWXI1gl7Ifs5iuR7Ozgqp52HkJw1JFez5GHFLQeV7CZ%2FryBQBZWbocMxGFeBkGldyobiiqtoBaKAxr3zBCTdLQQGa4uAmu8jLuGDdzwDR5xPSLbRx%2FCEYT20yU%2BKwFUmk%2BXAoFMyEDTvybsZR9%2FTfSQ4Rt1GQaEutPuIAqhytICxjjSWhcETm5TQ5B%2FJ1FRXFkv40KAn8al0gvA%2B6kQjFyJ5AucterpcJAeMKhPmEIMiqFhJNCGLDDivuGdLiu%2BAijUHDhBnbhydjtJiKlNjXOUgkO1Ku8OsYUMWyQU4oElV5NlwSN4fUacyTIhd4NrLyvyMKi%2Bq50WkX9x9VotzLRrUFCJW%2BOKJ76LHPSdK9lV%2FJEsWhcOL2%2F8ak0r0wCRx6JXjNS1%2FViSvejnRDkvpmi6bQwoHtZhVSk1BMGTivSKlP2UW9ZI7hNsVqXgOkqiZKWOc3%2FMSPpIBTbOalFyFqQZ7Jg9mKA6oBEWaPIeUtvvISWSx5qyuRz6iiTMJNG4kz%2FA3WZ5KaS9rl6nV3Gz%2FkbXgNwnV5bwPgRz5SN4j0GksKLBRaxyqeQb1h64ehqZEmnr%2Fh454oFgzyuSeDvpOKFBNjQ2yka8zSVOeSNZIEYm%2BTezD7XhBB%2BPMuUusBU6hV0wy5KZ3Z1C%2B7gh6FWf2foxBXNLU%2B5jmsnaUrkFEsBpj2POebBXNZV6iUtEEtGBJdd1Leexi6vr0IDadVtQej1zNunKecwYlvUiUOQH%2BSQ2rqLHvwueEDc0387BKyA3IDtJ4bl4vtJh5bH3zSlGlgJbwbkjQrB02iYtoZ1XdpXYwe6F5noWxY1OfsReGoLNSn48v4T2a81BxOUUV15ZD4EzninukMjuV81lHGM1ZPJIkPe1yo%2FtpKknDVeh14TdPKN2sG6Ix6B%2B%2FaMz92O19XRLeSWb6gHg3QqEa2IcKQgwt2YpDGAffXKJL%2BP6FBJ41bA6mJjdpw9rtnZe%2Bhj2HeH41E8p%2BgujZv4R3kfN41LVjg6TI4rSihwZ%2BOaup3rLy5oml7b6yKCv3gXTv0pEFaTKUTM2xFarJ58KVLEhLeOddGAcXjYotpxrr13NLGH2WJ0GmxXS7weg5nCdj3zirsg6QcDR5WJww6nKEI%2Blz8X0Zz8rV5AOrPDgn5F%2BlWNlu%2F%2Fvv%2F%2F3nX3BzffMW3rv0WXu%2BoFx1Jvqv3%2F6bt1z1H%2B3FVaFCKDbF6g18i4EV5E96tGnwPQm8We3szqZT8GuycHBWNrBe3pCBFayXbyE8BiGziPx1Wn%2FgSppN8te0f%2FzzV9ft6Qr%2Bcv2HK1hfX1%2B3pz%2FlTQZ9zXYD14BR3Nc7%2Byld0qzPVywC%2F0IbuCEzrt48W10v357XsVtWSYY24KkaFzaNO5LvllNMi4qU85gg34B1loadqzfwHo9gyMY%2B7qi7YxWHVuPjBg6aTjmEFquKbb2B6%2FyoOcgi%2F7thkfAb7QL8HIPw4XHRTwUbCC0qWuxJHohs3lJju4H1dXsaHNHcx6rptIH1kxAvxTAGv9eo7vKLPaq72rtoq0W%2F9khau4faD3dnY6i5thtQqfz8PLypWzMkn5uuna7IeldN8Pwh%2FUMgs6mXyx7Y5UjkzlrHiIW4dkD0uf0K%2FV1IH0u1x8dpvMp5G1jfDfdOjM9Z0Ubf6mm6%2F9ZVV%2BdTX2rP%2FLnpIPhcyD2WocHKPWxg3Z7GnyEhn3K9%2FZzKrbgqpCFDxabInhaf%2Fg8%3D&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FFixing_blog_styles%2F)

## [Project brief](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles#project_brief)

The basic blog example you've been given isn't finished, and the existing code has some problems. Follow the steps below to complete the project.

1. We want every element on this page to use the alternative box model. Add a rule to the stylesheet that does this.
    
2. There is a problem with the rules for the nav menu — the styles are mostly OK, but they are affecting the other unordered list and content links, making them look bad! Can you adjust the selectors for these rules so that they only target the nav menu?
    
3. Actually, there is another problem with the nav menu — the `<a>` elements are not spanning the full width of their `<li>` element parents like they are meant to. Can you adjust the way they are displaying so that they span the full width?
    
4. For both the nav menu links and the regular content links, we are setting a different style on hover so that mouse users can see which link they are hovering over. This presents an accessibility issue for keyboard users, who won't be able to see those styles. Can you alter the selectors in the relevant rules so that these styles are also applied when a keyboard user tabs to the links?
    
5. We want the introduction, summary, and footer to have `20px` of padding on all sides. Make this happen by adding a single declaration somewhere in the stylesheet.
    
6. Add a rule that selects the first line of every paragraph that appears right after a second-level heading, and turns it bold.
    
7. As a follow-on from the previous question, can you think of a way to bold the first line in every paragraph following a second-level heading, but only when the parent element is not the introduction, summary, or footer? You can do this in a few different ways, some more concise than others.
    
8. Further down, you'll see that we are using `.highlight a` to select the `<a>` elements inside the introduction and summary, and coloring them `purple` inside the associated rule. But this is no good — the color contrast is terrible. Assuming you are not allowed to change or remove that rule, can you add another rule above it in the source order that colors the `<a>` elements `yellow`? Being above it in the source order, it will have to have a higher specificity.
    
9. You'll see that we are trying to select the `<footer>` at the bottom of the stylesheet and give it a text shadow, some margin to move it away from the summary, and a different background color to make it stand out. However, it is not getting the desired margin and background color styles because the `.highlight` rule has a higher specificity, so its declarations win. Can you alter the selector to make sure those styles get applied?
    

## [Hints and tips](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles#hints_and_tips)

- Use the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) to catch unintended mistakes in your CSS — mistakes you might have otherwise missed — so that you can fix them.
- You don't need to alter the HTML in any way.

## [Example](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles#example)

The finished project should look like this:

[Play](https://developer.mozilla.org/en-US/play?uuid=033e6c796e7adc22db56642516edfffb2e889b0d&state=zVhdjhvHEb5KhUYAWVmSu4sYMWhqAdlWYAWJLEBJnvhS01OcKW9P96h%2FuGQEnyHnyA3ynAvlCkF1z%2B8uuZbf8qAVZ7q7uvqrr76qnk%2BLOjR6sVlsf1NaFU4tgby425mt%2FA8aTfVqtyCzW9ztDMC2JizTL4BtQwFB1eg8hVe7RQz75de7Baz78cBB090H%2FgebChAKbStosSJZozWZirbrPKdboNncQ%2B1o%2F2q38OGkaaW83y3Ake7f%2BJooDJts14M%2F28KWp96QvCXXPcnzzd1raKwPQEdFsndI7mzX9c04y%2BBheADYRj15St7dbbF374vd4u4H29B2jXfbteZfmPpt2uyzpr4ubAyfOfc7awKqc7O364n72%2FV4tAzZAM62QTbjRE8qsDXA5avdgk1wtozpzW4BSqP3r3aLmqtac1WHjhM9xrd3P0YHhh7IB2itD9t1fTud0c5O82e0jiiAto4aUNEhgSYVoodCoyk5gLImFoxwIA2empYc6G6VsqaKNLWHAQIqDryaYTbD632NnrSOHmpUYkPOSyE6YFRRs4cysqAJHlsm07%2BeWpSVUQfHislD8imK1yv4EL3ilgM0GAJ70Kii7x1nA611Aaem2sEdb7VmxSGWbIBbHxvYk2vIhNhMpyWvVvDWKGqDnflFgbGBVqMihyFtFjhYB3s2XEQPGJU8ypjGQAg1mdKR4wBIhtBMrfU4k%2BY%2BRLZku5oyrJ0QrCPOEyY9Ysibo0TIVIJ9IPNLFEn7ZjhKq60DL842FK5mwcOSW%2FZK7Iq%2FV%2BCphNLO0OHoG1tCoKa1Eg3FJZfRBIgBNBbWEVDIuxA0WBkE1Pwx4greO8szcIJ1gmQbXfSPGNZBK35SBC4TmQx7Bi3BQNBckLMzjr6jj5HgEHUbAwbKR%2FsYMQCqdFrAWEUa0qLBIzcSUPGPwtRUTosVvK%2FRUXCSOj5wEbXQyPpIjsA6g44uJ8keo0qE2UevCEpWITY%2BiQxYp7hji5xvj4o1e%2FYQZ24crI6hRUnTprGlBU8mp3bGrOaGDJL1sMdGsshxw168P6CWNBTELnDtvDI%2FocpZ9byI9NnZo1qMudigJh%2BxxLMrvosOCxZKdll%2FIEMGA%2Fuz07%2BPohIdMCIOnXI8p%2BVPkuRZLyfaYUi2ydHsQ9irxSxTKvIBfSLeM1L6Y2JRJ7n9cXOSBsc%2BCDUTZRrrCl7BB2pA0ywnQ8pCycGOyb0Zij0qXpEmx17C9jGyiCxWnNT1wAds4kwCGzuQp%2F9NhqdS2snaZWrVt3d%2FSVrwq4Tqctz7gxz4QM4h0HFIKDBRa%2ByzeQb1%2B5wPfVEiTZ3%2FfUXcU6wYw2SfDH0WClRTY71spO0a0ZRHkjVQJETXCvvwbtggwzhz7hJrgeXoJVPoY9O50ytfXoJOxZm9P0UfrGjqxyh9WTtIVy8iWA5nKLggU8bmMi9Rqdh4NGBI5eqlHOYz5Trdi03WisrhgctZVU59Tq%2BkF4kyJ8DfqWYVNXZVeAxYX3wTD0tBrke2l8axeJ0pMfOzdcVLTiUHWsGbPkCzclgLF9HMsjqHtjd7oXiOwpjZ1EXsTBM0KvW4fAXvsBmbisshKrky7D0nOpfcIZXYqaxLOsLYjOIhkvS4yg3uS1cizZXvdOFXdyi51%2FWxadCdPqvN%2FZDnPi8Jb0Jieo94bqFQ9exDBT76lkzJ3g%2BNb0rRFfxwJoCjhs3B1GQnZVjbwrrQ5bBjH8dXM6HsOoiO%2FSt4Ezm1R7kcN0iKDE4zui%2Fgl6Mq%2BZaUN3Usbb5lUVLuPenOpQMHpElTMjXHJlBFLiVuSIK0gjfO%2BqFx0ajYsORYN55KwuBzeHRIGZTdG4yO%2FdgZu9oalXSAAscmNYsTRl0%2B4UD6lHyfx7PtenLB2u6tDeSepdi2vfvPv%2F7773%2FC7fXtV%2FDOyrV23GC7zia62293592uu0v74mqhvF9sFuuX8C16VpCu9Gik8T0GeLnemZ1Zv4QPoq1szQY%2BSHupAzkpIweCwh6hsSVpsAZQ617LfFr8Ej7JzoU9Ln2612%2BgsK4ktyzs8Zud%2BVnsi1d53t6asIGb1S01sIab1VfgTz5Qs4z8jYw%2FcBnqjeDRtC9%2B%2F%2FV1e7yCP1z%2F9gpurq%2Bv2%2BOXaVKDrmKzgWvAGGy%2FSX0zbiG%2B0AZuqRlGb5%2BM3qy%2BGscxDyuRuQ04KvuBGTZ%2Fa0sRw01tD%2BQgf3%2BAYAG1t4Btq08C0mZvlSSGtxBqDHBPp8KiKyF6ch4UGvBEEGqCmAyWvamHmszOhJpOELAQy%2FIFJCONedcr%2BZU2yB5LGJclKesw%2B2isobPOF1aXsNns2fmw1GwI7B4IVQ0tOqwctnX2F9uW0PmdcUJFwL1QFMGTqPNSk9y%2B5ZsBm%2BoKihjAGn1KvqcztehIpKrjCUgDZkMamn5AuIJOYq9A7qSJxTvzInqCjbHhxWpIhi8FCN%2BS4v0JQs2%2BcwUKDl8mbLoUe7KuvoXfQTs788iCB5JJGZcRMPn7ekJ%2F6URqAizsgeRWPgVTsoGND2gUeUibXKXwGXDUyAIOsHe2gVBbL8f3XEr29TkEDxzqZH%2FMfJPbjYT6A7rSi0d9afrVBxrR%2BLy1xroGdb96kId3eICGTDwnGK%2FLn6I0r3gAFzWBJyle1qXMEGrsTEBXUaZA%2Bqg2tSXros6ulOxbjacN7DUdU663WJZJVa7To2YflilZliJkA9sBxAfen5Zde74B36KiZUHhgcikKRW2G7i5bgddkq01dyhoOm7gZjqEz2fYoBaFRnWfXhSo7itnoymX3diJtLYPlet9eCK1stEW70ZVDXaEodBW3UPSETrJidJXB4FxH7XOailZHGpil26QA7NyFmbpgEcWvxmOhZorswElldnNAZ8C9X8jgiksgxDmp4kYPsW%2Fsrok4%2BxUz9%2BKCqUa2ClQx8RJrnwa68wy2Lan31P7Jbp7L594KoenKSmUdcazvj8f9dvr9iiB69DuS6vIg%2B8CKusu6KW4ngVzBX8VnGRtjQfq140HyWLiSURaRpuOEEOYby%2BF%2BXVZJjsS46S98jnylFM8q%2BFuMUEMd4udSYOS9XK3FalT%2BSMdhXR1fvH2%2B4k6JIex22NnppuEGs3gejc%2FK%2F0XU0gAr3bmiz6I8xKeE%2B%2BMDM6ntdG1elov%2F5g7sjM699YoR%2Bipg74Tu4nXxQm6cE6REVz6JODgJ6xKcXxMqT4L5FuKJBNTmZzp4v0MRbtI%2FlIWdJnvayztwwZu2uPwrxeyn1Pj%2BJP0jYurhbCGFptF2nbx8%2F8A&srcPrefix=%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FFixing_blog_styles%2F)

Click here to show the solution

The finished CSS looks like so:

- [Previous](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Test_your_skills/Cascade)
- [Overview: CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
- [Next](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units)

## Help improve MDN

Was this page helpful to you?

YesNo

[Learn how to contribute](https://developer.mozilla.org/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Oct 16, 2025 by [MDN contributors](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/learn_web_development/core/styling_basics/fixing_blog_styles/index.md?plain=1 "Folder: en-us/learn_web_development/core/styling_basics/fixing_blog_styles (Opens in a new tab)") • [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FFixing_blog_styles&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ffixing_blog_styles%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FLearn_web_development%2FCore%2FStyling_basics%2FFixing_blog_styles%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Flearn_web_development%2Fcore%2Fstyling_basics%2Ffixing_blog_styles%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F50a1895c9c499b1b9207f7af945a0fe45de58cca%0A*+Document+last+modified%3A+2025-10-16T22%3A10%3A02.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")

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
    13. _[Challenge: Fixing blog styles](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Fixing_blog_styles)_
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

[![MongoDB Atlas](https://developer.mozilla.org/pimg/aHR0cHM6Ly9zdGF0aWM0LmJ1eXNlbGxhZHMubmV0L3V1LzIvMTczOTc1LzE3NzQyODE2NzEtTUROXy1fMTQ1NngxODAucG5n.FxNud8HsbSMmNNOG1%2FNiQimNF2bptd1qCinx6cZcuH8%3D)](https://developer.mozilla.org/pong/click?code=aHR0cHM6Ly9zcnYuYnV5c2VsbGFkcy5jb20vYWRzL2NsaWNrL3gvR1RORDQyN1VDWUJJUDVRTkM2N0xZS1FVQ0FTSTQyN0lGVEJES1ozSkNBU0k1S0o3RlRCRDQyN0tDQUJJSzUzTENWU0Q0SzNVQ1dBRFYyM1dGNlNETDIzS0M2U0k1MkpOQzZZREVLM0VISk5DTFNJWg%3D%3D.9qhi%2FSSGFEYtEHuEyzgBM4Si71K9wHquuQvz0FaKLnE%3D&version=2)[Ad](https://developer.mozilla.org/en-US/advertising)

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