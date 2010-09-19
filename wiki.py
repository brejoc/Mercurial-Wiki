#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import sys
import codecs
import thread
import webbrowser


from juno import *

from creole import Parser
from creole.html_emitter import HtmlEmitter 

from mercurial import commands
from mercurial import ui
from mercurial import hg
from mercurial import verify
from mercurial import cmdutil


init(dict(
    use_database=False,
))

file_path = os.path.dirname(os.path.realpath(__file__))

config(dict(
    use_static=True,
    static_url='/static/*:file/',
    static_root=os.path.join(file_path, 'static/'),
    template_root=os.path.join(file_path, 'templates/',
))


REPO_DIR = os.getcwdu()
PAGES_DIR = ".hgwiki"


def page_exists(page_name):
    return os.path.exists(os.path.join(PAGES_DIR, page_name))


@route('/')
def index_page(web):
    redirect('/start')


@route('/edit/:name')
def edit_page(web, name):
    content = ""
    if(page_exists(name)):
        page = codecs.open(os.path.join(PAGES_DIR, name), 'r', 'utf8')
        content = ''.join(page.readlines())
        page.close()
    template('create.html',
             name = name,
             content = content)


@get('/*:name')
def page(web, name):
    if(page_exists(name)):
        page = open(os.path.join(PAGES_DIR, name), 'r')
        document = Parser(
            unicode(''.join(page.readlines()), 'utf-8', 'ignore')).parse()
        template('page.html',
                 name=name,
                 content=HtmlEmitter(document).emit())
    else:
        redirect('/edit/' + name)


@post('/:name')
def update_page(web, name):
    abs_path_to_pages = os.path.join(REPO_DIR, PAGES_DIR)
    if not os.path.isdir(abs_path_to_pages):
        os.mkdir(abs_path_to_pages)
    with(open(os.path.join(PAGES_DIR, name), 'w')) as page_file:
        page_file.write(web.input('content'))
    repo = hg.repository(ui.ui(), REPO_DIR)
    file_list = [os.path.join(PAGES_DIR, name)]
    try:
        # Mercurial <= 1.5
        repo.add(file_list)
    except:
        # Mercurial >= 1.6
        repo[None].add(file_list)
    match = cmdutil.matchfiles(repo, file_list or [])
    repo.commit(match=match,
                text="HGWiki: Changed wiki page %s" % (name, ),
                user="hgwiki")
    redirect(name)

def start_browser():
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    thread.start_new_thread(start_browser, ())
    run()
