# J-Chess: Play chess in the console!

<h1 align="center">
<img src="image.png" width="900">
</h1>

A simple project allowing you to play chess within your console.

## Usage

Requires `python 3.10`
or later. The package is available on `pypi` so to play simply install with
`pip install jchess` and then play with `jchess` or `python -m jchess`.

The project was developed primarily alongside `powershell` but the project should be
compatible with generic Windows and Linux consoles.

If you have any feedback please feel free to share it!

## Features

J-Chess fully implements chess logic and rules - including castling, en-passant, promotion and check/checkmate.

It is primarily designed to be played by 2 people at the same computer but it does
feature a "VS Dumb Bot" mode where you can play against an opponent who's moves are
random.

For demonstration purposes there is also a "Two Dumb Bots" mode where an entire game is
played with no user input.


## Motivation

This was simply a project to better familiarize myself with programming in python and
other lifecycle practices & tools.

I was able to practice using useful tools like `git`, `github` and `wsl` as well as
useful concepts including OOP programming patterns, regular expressions, testing,
documentation, packaging and managing dependencies.

The python tooling modules I used were `mypy`, `pylint`, `black`, `isort`,
`pytest`, `pydocstyle` and `coverage`.

Python code features I experimented with and used in the final project include
dataclasses, generators, type annotations and context managers.

## Scope

The goal of the project was to practice pure python programming so by design there are
minimal 3rd party package dependencies - in fact there is only one: `colorama`.

The scope of the project was intentionally minimal, but some fun ideas if I return to
this project would be:
* Implementing different guis - maybe through a web app or `tkinter`
* Implement a genuine AI
* Implement a non-local multiplayer mode


## Project Structure

Not counting recursively, there are currently 8 sub-modules/packages which are
published in the `jchess` whl (plus one module used only for testing). The project
structure can be thought of as follows:

```
+-----------------------------------------------------+
|          pieces ---- board       display ------ run |
|         /                  \    /                   |
| geometry                    game                    |
|         \                  /    \                   |
|          terminal -- action      (testutils)        |
+-----------------------------------------------------+
```
