# Cavia

<img
    align="right"
    height="256"
    src="https://raw.github.com/KeyWeeUsr/Cavia/master/cavia/data/logo.png"
/>

Because guinea pigs are kawaii~

Cavia is a free and open source cross-platform tool built with
[Python](https://www.python.org). The tool consists of two parts - console and
GUI (WIP).

The primary use of Cavia is to download content from various websites
("sources") via parsing the website's source code and retrieving URLs for
the particular content according to the `Source` script.

Cavia doesn't host or (re)distribute *any* of the content, nor *cares* what
is its origin, authors, rights or anything. As an ordinary user you can visit
any of the sources Cavia uses through an ordinary Internet browser and do
whatever the Terms of Use for the website allow you. Cavia only saves you
the time consuming process of clicking, waiting, random website errors
and so on. It's recommended to visit each source you want to use directly
and read its conditions for the content viewing or other usage properly.

The only purpose of Cavia is to simplify the access to pictures someone else
uploaded somewhere and are available *publicly* no matter the legality. Each
piece of content this tool aquires at runtime belongs to their rightful
creators, publishers and/or other kind of owners and you as a user are bound
to comply with any of the rules/terms/conditions/... which come with
the content itself.

If you feel Cavia directly by any means breaks the law, you are free to open
an issue. Otherwise look into the code, find the URL for the specific `Source`
you feel breaks the law and you are free to write them. :-)

There is no warranty for the program, it's expected that you either are
an adult or can use a program like an adult. You are free to get a supervision.
Should the program prove defective in any way for example data corruption,
machines exploding, guinea pigs dying, you are on your own.

Installation & Usage
--------------------

First of all you need to install [Python](https://www.python.org) 3.x.
Versions lower than 3.x aren't supported nor any ports are considered right now.

Then you can either install a stable version (WIP):

    pip install cavia

or the latest one from this repository:

    pip install https://github.com/KeyWeeUsr/Cavia/zipball/master

After the package correctly installs, run Cavia from your console:

    python -m cavia

you'll see a simple output with choices for `console` and `gui`.

Contributing
------------

By the license Cavia is distributed under you are free to modify the tool as
long as you track changes/dates (best with a version control system) in source
files, please read the
[`LICENSE.txt`](https://raw.github.com/KeyWeeUsr/Cavia/master/LICENSE.txt) file
for more info.

If you make any changes in the source code, please open a pull request.
Hopefully your change will help this little tool. If your change is a very small
one and you don't want to go through the whole machinery with
[`git`](https://git-scm.com) itself, you can use
[this guide](https://help.github.com/articles/editing-files-in-your-repository)
from GitHub for editing the files online.
