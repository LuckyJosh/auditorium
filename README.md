# Auditorium

<img alt="PyPI - License" src="https://img.shields.io/pypi/l/auditorium.svg"> <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/auditorium.svg"> <img alt="PyPI" src="https://img.shields.io/pypi/v/auditorium.svg"> <img alt="Travis (.org)" src="https://img.shields.io/travis/apiad/auditorium/master.svg"> <img alt="Codecov" src="https://img.shields.io/codecov/c/github/apiad/auditorium.svg">

> A Python-powered slideshow creator with steroids.

## What's this about?

Auditorium is a Python-powered slideshow generator. You write pure Python code, and obtain an HTML+JavaScript slideshow (using the amazing [reveal.js](https://revealjs.com) library). The awesomeness comes from the fact that your Python backend is connected to the slideshow frontend, which allows your slideshow to dynamically change according to user input or automatically.

This opens the door to a few interesting use cases:
* The slides content itself can be generated by code. For example, long and repetive sets of slides can be automatically generated, or tables and graphs embedded in slides can be generated on-the-fly with `matplotlib`, `bokeh`, `altair`, `plotly`, or any visualization package that produces HTML output.
* You can insert components in the slides that respond to user input, and execute a Python code in response. For example, you can generate an interactive graph that can be modified by moving sliders in a slideshow.
* You can create beautiful animations with simple Python code, that automatically play on a slide, using visualization libraries or simple HTML markup.

**And all of this without writing a single line of HTML or Javascript.**

## Demo

> If you to see a demo of `auditorium` in action, visit [auditorium-demo.apiad.net](https://auditorium-demo.apiad.net), or embedded below.

<iframe src="https://auditorium-demo.apiad.net"></iframe>

## Quick start

In `auditorium` you create a presentation via the `Show` class:

```python
from auditorium import Show
show = Show("My Show")
```

Every slide in your show is a Python method that renders the content and powers the backend logic. Slides are decorated with the `@show.slide` decorator.

```python
@show.slide
def one_slide():
    # content
```

Then run the show:

```python
show.run('localhost', 5050)
```

The simplest possible form of content is static Markdown. You can add it with `show.markdown` and/or directly as the docstring of the corresponding slide function:

```python
@show.slide
def static_content():
    """
    ## Static content

    Can be added very simply with:

    * Method _docstrings_
    * Calling `show.markdown`
    """

    show.markdown("> Like this")
```

There are several components in `auditorium` to style and layout your presention, including reactive components that respond to user input.

```python
@show.slide
def interactive():
    show.markdown("Enter your name")
    name = show.text_input(default="World")
    show.markdown(f"> Hello {name}")
```

> The slide code is considered stateless, and will be executed everytime the input changes. You should design your slides with this in mind to, for example, provide sensible default values that will work when your presentation first opens.

Simple stateless animations can be created with `show.animation`, which execute the backend code for every frame. Combining this with drawing logic from, for example, `matplotlib` allows for very simple animated graphs and visualizations:

```python
@show.slide
def pyplot():
    with show.animation(steps=50, time=0.33, loop=True) as anim:
        # Every 0.33 seconds the graph will move
        step = anim.current * 2 * math.pi / 50
        x = np.linspace(0, 2 * math.pi, 100)
        y = np.sin(x + step) + np.cos(x + step)
        plt.plot(x, y)
        plt.ylim(-2,2)
        show.pyplot(plt, fmt='png', height=350)
```

> See a full demo of `auditorium` at [auditorium-demo.apiad.net](https://auditorium-demo.apiad.net).

## History

### v0.1.3

* Added custom layout options with `show.columns`.
* Fixed some style issues.
* Updated Readme with some examples.

### v0.1.2

* Refactor custom CSS and Javascript into `auditorium.css` and `auditorium.js` respectively.

### v0.1.1

* Added basic binding for variables
* Added support for simple animations with `show.animation`.
* Added support for `pyplot` rendering.

### v0.1.0

* Initial version with basic functionality

## Collaboration

License is MIT, so you know the drill: fork, develop, add tests, pull request, rinse and repeat.

> MIT License
>
> Copyright (c) 2019 Alejandro Piad
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
