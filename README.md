# Auditorium

<img alt="PyPI - License" src="https://img.shields.io/pypi/l/auditorium.svg"> <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/auditorium.svg"> <img alt="PyPI" src="https://img.shields.io/pypi/v/auditorium.svg"> <img alt="Travis (.org)" src="https://img.shields.io/travis/apiad/auditorium/master.svg"> <img alt="Codecov" src="https://img.shields.io/codecov/c/github/apiad/auditorium.svg">

> A Python-powered slideshow creator with steroids.

## What's this about?

Auditorium is a Python-powered slideshow generator.
You write pure Python code, and obtain an HTML+JavaScript slideshow (using the amazing [reveal.js](https://revealjs.com) library).
The awesomeness comes from the fact that your Python backend is connected to the slideshow frontend, which allows your slideshow to dynamically change according to user input or automatically.

This opens the door to a few interesting use cases:
* The slides content itself can be generated by code.
For example, long and repetitive sets of slides can be automatically generated, or tables and graphs embedded in slides can be generated on-the-fly with `matplotlib`, `bokeh`, `altair`, `plotly`, or any visualization package that produces HTML output.
* You can insert components in the slides that respond to user input, and execute a Python code in response.
For example, you can generate an interactive graph that can be modified by moving sliders in a slideshow.
* You can create beautiful animations with simple Python code, that automatically play on a slide, using visualization libraries or simple HTML markup.

**And all of this without writing a single line of HTML or JavaScript.**

## Installation

Simply run:

    pip install auditorium

To see a quick demo run:

    python -m auditorium.demo

And point your browser at [localhost:5050](http://localhost:5050).

## Quick start

In `auditorium` you create a presentation via the `Show` class:

```python
from auditorium import Show
show = Show("My Show")
```

Every slide in your show is a Python method that renders the content and powers the backend logic.
Slides are decorated with the `@show.slide` decorator.

```python
@show.slide
def one_slide():
    # content
```

Then run the show:

```python
show.run('localhost', 5050)
```

The simplest possible form of content is static Markdown.
You can add it with `show.markdown` and/or directly as the docstring of the corresponding slide function:

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

There are several components in `auditorium` to style and layout your presentation, including reactive components that respond to user input.

```python
@show.slide
def interactive():
    show.markdown("Enter your name")
    name = show.text_input(default="World")
    show.markdown(f"> Hello {name}")
```

> The slide code is considered stateless, and will be executed every time the input changes.
You should design your slides with this in mind to, for example, provide sensible default values that will work when your presentation first opens.

Simple stateless animations can be created with `show.animation`, which execute the backend code for every frame.
Combining this with drawing logic from, for example, `matplotlib` allows for very simple animated graphs and visualizations:

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

## What's the catch

Auditorium covers a fairly simple use case that I haven't seen solved for a long time.
I came up with this idea a while trying to make better slideshows for my lectures at the University of Havana.
I need to display complex math stuff, ideally animated, and sometimes make modifications on the fly according to the interaction with students.
They could ask how a function would look if some parameter where changed, etc.

Along that path I grew up from Power Point to JavaScript-based slides (like [reveal.sj](https://revealjs.com)) and sometimes even coded some simple behavior in JS, like changing a chart's parameters.
However, for the most complex stuff I wanted to use Python, because otherwise I would need to redo a lot of coding in JS.
For example, I'm teaching compilers now, and I want to show interactively how a parse tree is built for a regular expression.
I simply cannot rewrite my regex engine in JS just for a slideshow.

Then I discovered [streamlit](https://streamlit.io) and for a while tried to move my slides to streamlit format.
Streamlit is awesome, but is aimed at a completely different use case.
It's quite cumbersome to force it to behave like a slideshow, the flow is not natural, and the styling options are very restrictive.
On the other hand, they handle a lot of complex scenarios which I simply don't need in a slideshow, like caching and a lot of magic with Pandas and Numpy.
Contrary to streamlit, I do want custom CSS and HTML to be easy to inject, because styling is very important in slides.

So I decided to write my own slideshow generator, just for my simple use cases.
That being said, there are some known deficiencies that I might fix, and some others which I probably will not, even in the long run.

### Slides need to be fast

A slide's code is executed completely every time that slide needs to be rendered.
That is, once during loading and then when inputs change or animations tick.
Hence, you slide logic should be fairly fast.
This is particularly true for animations, so don't expect to be able to train a neural network in real time.
The slide logic is meant to be simple, the kind of one-liners you can run every keystroke, like less than 1 second fast.
If you need to interactively draw the loss value of a neural network, either is gonna take a while or you will have to fake it, i.e., compute it offline and then simply animate it.

### All slides are executed on load

For now, on the first load all slides are going to be run, which might increase significantly your loading time if you have complex logic in each slide.
At some point, if I run into the problem, I may add a "lazy" loading option so that only the first few slides are executed.
If this is an issue for a lot of people it might become a priority.

### The show state is global

Right now there is a single `Show` instance running the show, so several people looking at the same slideshow will share the values for the interactive inputs and animation steps.
This might create weird scenarios in which you are typing into an input text box and you see a different result because another viewer is typing on a different browser.
I don't know right now the extent to which this is an important issue, so I might fix it in the future if necessary.

### Watch out for code injection!

It is very tempting to do things like getting a text from an input box and passing it through `eval` in Python, so that you can render different functions interactively.
As long as you serve your presentations on `localhost` and show them yourself, feel free.
However, beware when hosting presentations online.
Since the backend code runs in your computer, a viewer could inject nasty stuff such as importing `os` and deleting your home folder! In the future I might add a `--safe` option that only allows for animations and other interactive behaviors that don't use input directly from the user.
Staying away from `eval` and `exec` should keep you safe in most scenarios, but the basic suggestion is don't do anything you wouldn't do in a regular web application, since all security issues are the same.

## History

### v0.1.4-dev (branch `develop`)

* Added support for `reveal.js` themes via `show.default_theme` and query-string argument `?theme=...`.

### v0.1.3 (latest release and branch `master`)

* Added support for fragments.
* Added support for vertical slides
* Added custom layout options with `show.columns`.
* Added styled block with `show.block`.
* Added parameter `language` for `show.code`, defaulting to `"python"`.
* Better layout for columns, with horizontal centering.
* Better layout for input texts.
* Better example for the `pyplot` support in the demo.
* Fixed some style issues.
* Fixed error reloading on a slide with an animation.
* Updated Readme with some examples.

### v0.1.2

* Refactor custom CSS and JavaScript into `auditorium.css` and `auditorium.js` respectively.

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