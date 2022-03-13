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

`git-uff` has a few other available options. Here is its `--help` output:

<!-- [[[cog
import subprocess
result = subprocess.run(["git-uff", "--help"], capture_output=True, text=True)
cog.outl("```")
cog.out(result.stdout)
cog.outl("```")
]]]-->
```
usage: git-uff [-h] [-b BRANCH] [-p] [-c] [-l LINE] path

Prints the forge URL for a given file or path of a Git repository checkout.

positional arguments:
  path                  File for which we want the URL

optional arguments:
  -h, --help            show this help message and exit
  -b BRANCH, --branch BRANCH
                        Use branch BRANCH instead of the current one
  -p, --permalink       Replace the branch in the URL with the commit it
                        points to
  -c, --copy            Copy the result to the clipboard
  -l LINE, --line LINE  Line to point to

New forges can be declared in git configuration. You can do so using
`git config`, like this:

    git config --global uff.<forge_base_url>.forge <forge>

Where <forge> must be one of: cgit, github, gitlab, sourcehut.

For example to declare that example.com uses GitLab:

    git config --global uff.example.com.forge gitlab
```
<!--[[[end]]] -->

## What if my code is not on GitHub?

`git-uff` is not tied to GitHub. It supports GitLab, SourceHut and CGit forges.

To declare a new forge, add it to your git configuration with:

    git config --global uff.<forge_base_url>.forge <forge>

For example to declare that example.com uses GitLab:

    git config --global uff.example.com.forge gitlab

See the output of `git uff --help` for the valid `<forge>` values.

## Installation

The recommended method to install `git-uff` is to use [pipx][]:

```
pipx install git-uff
```

[pipx]: https://github.com/pipxproject/pipx

But you can also install it with `pip`:

```
pip install --user git-uff
```

## License

Apache 2.0
