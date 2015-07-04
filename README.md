## Mercurial Wiki

Mercurial Wiki is a wiki with the sole purpose to be embedded into a Mercurial repository. Everyone who clones the repository will automatically get the wiki documentation with all the information needed to get started or the latest changes for the project or branch. 

Regardless if you are sitting in a plane or travel in nature without internet connection, all the important information are stored right in the repository just with the code.

The [Markdown](https://pypi.python.org/pypi/markdown2/) markup is used to format and layout the wiki pages. Up until version 1.2 [creole markup](http://en.wikipedia.org/wiki/Creole_(markup)) was used.

### Dependencies 

Mercurial Wiki requires bottle.py, Jinja2, markdown2 and of course Mercurial. You can install the dependencies with `pip install -r requirements.txt`. But you should create a virtualenv first: `virtualenv --distribute --no-site-packages env`. And don't forget to activate it with `. env/bin/activate`.

### Usage

Download Mercurial Wiki und extract anywhere. Now cd to your ~/bin or /usr/local/bin folder and create a symlink (ln -s <path> hgwiki) to the hgwiki.py. Now you can change to a local Mercurial repository (only base path works for now) and enter hgwiki. A browser window opens and shows the start page.

### Installation for Ubuntu 12.04 Precise 

A ready to install [package for Ubuntu 12.04](https://bitbucket.org/brejoc/mercurial-wiki/downloads/python-mercurial-wiki_0.1~hg20130319-precise1_all.deb) Precise can be found in [Downloads](https://bitbucket.org/brejoc/mercurial-wiki/downloads).

The [fpm makefile](https://bitbucket.org/brejoc/fpm-makefiles/src/tip/ubuntu/12.04/hgwiki/Makefile?at=default) for this package can be found in my [fpm makefiles repository](https://bitbucket.org/brejoc/fpm-makefiles).
