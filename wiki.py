#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import sys
import codecs

from juno import *

from creole import Parser
from creole.html_emitter import HtmlEmitter 

from mercurial import commands
from mercurial import ui
from mercurial import hg
from mercurial import verify


init(dict(
    use_database=False,
))

config(dict(
    use_static=True,
    static_url='/static/*:file/',
    static_root='./static/',
))


def page_exists(page_name):
    return os.path.exists('pages/' + page_name)


@route('/')
def index_page(web):
    redirect('/start')


@route('/edit/:name')
def edit_page(web, name):
    content = ""
    if(page_exists(name)):
        page = codecs.open(os.path.join('pages', name), 'r', 'utf8')
        content = ''.join(page.readlines())
        page.close()
    template('create.html',
             name = name,
             content = content)


@get('/*:name')
def page(web, name):
    if(page_exists(name)):
        page = open(os.path.join('pages', name), 'r')
        document = Parser(
            unicode(''.join(page.readlines()), 'utf-8', 'ignore')).parse()
        template('page.html',
                 name=name,
                 content=HtmlEmitter(document).emit())
    else:
        redirect('/edit/' + name)


@post('/:name')
def update_page(web, name):
    with(open(os.path.join('pages', name), 'w')) as page_file:
        page_file.write(web.input('content'))
    # TODO: If the file is new, it needs to be added
    # TODO: A changed file needs to be commited
    redirect(name)

if __name__ == '__main__':
    run()
