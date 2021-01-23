# git-uff

Prints the forge URL for a given file of a Git repository checkout.

## Intro

Have you ever been discussing with colleagues over IRC/Slack/Matrix/whatever about source code and found yourself needing to point them to a particular file in a git repository?

This is tedious to do.

One solution is to tell them the path in their checkout, hoping they are on the same branch as you.

Another solution is to point your browser to the forge hosting your git repository, select the right branch, navigate the file hierarchy, find your file and copy the file URL.

A better (in my opinion 😉) solution is to use `git-uff`. This tool adds an `uff` (short for "URL for file") git sub-command, which takes the path to a file in your repository checkout and prints the matching forge URL.

For example to print the URL of the `src/linux/nanonote.desktop` file from my [Nanonote][] project:

```
$ git uff src/linux/nanonote.desktop
https://github.com/agateau/nanonote/blob/master/src/linux/nanonote.desktop
```

[Nanonote]: https://github.com/agateau/nanonote

You can also point them to a specific line with the `-l` argument:

```
$ git uff src/linux/nanonote.desktop -l 10
https://github.com/agateau/nanonote/blob/master/src/linux/nanonote.desktop#L10
```

## But my code is not on GitHub...

`git-uff` is not tied to GitHub. It supports GitLab, SourceHut and a few others. For now the supported forges are hard-coded in the code, but making it configurable should be easy.

## Installation

The simplest solution is to use [pipx][]:

```
pipx install git-uff
```

[pipx]: https://github.com/pipxproject/pipx

## License

Apache 2.0
