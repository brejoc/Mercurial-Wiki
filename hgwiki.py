#! /usr/bin/python
# -*- coding: utf-8 -*-

# hgwiki, Copyright (c) 2010, Jochen Breuer <brejoc@gmail.com>
#
# This file is part of hgwiki.
#
# hgwiki is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement

import os
import codecs
import thread

from bottle import TEMPLATE_PATH
from bottle import route, run, redirect, request, debug, static_file
from bottle import jinja2_template as template

from creole import Parser
from creole.html_emitter import HtmlEmitter 

from util import start_browser
from util import page_exists
from util import write_to_file
from util import commit_to_repo

debug(False)
file_path = os.path.dirname(os.path.realpath(__file__))

REPO_DIR = os.getcwdu()
PAGES_DIR = ".hgwiki"
WIKI_PORT = 8001
TEMPLATE_PATH.append(os.path.join(file_path, 'views/'))



# Bottle routes

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root=os.path.join(file_path, 'static/'))

@route('/favicon.ico')
def favicon():
    return ""

@route('/')
def index_page():
    redirect('/start')


@route('/edit/:name')
def edit_page(name):
    content = ""
    action = "Create"
    if(page_exists(PAGES_DIR, name)):
        page = codecs.open(os.path.join(PAGES_DIR, name), 'r', 'utf8')
        content = ''.join(page.readlines())
        page.close()
        action = "Edit"
    return template('edit.html',
             name = name,
             content = content,
             action=action)


@route('/:name')
def page(name):
    if(page_exists(PAGES_DIR, name)):
        page = open(os.path.join(PAGES_DIR, name), 'r')
        document = Parser(
            unicode(''.join(page.readlines()), 'utf-8', 'ignore')).parse()
        return template('page.html',
                 name=name,
                 content=HtmlEmitter(document).emit())
    elif(name == "start"):
        start_text = """\
**A Mercurial Wiki**

This is a wiki built on top of Mercurial. You can use the [[http://www.wikicreole.org/wiki/|creole markup]] to layout your wiki pages. 

Start creating some content!"""
        write_to_file(REPO_DIR,
                      PAGES_DIR,
                      os.path.join(PAGES_DIR, name),
                      start_text)
        commit_to_repo(REPO_DIR, [os.path.join(PAGES_DIR, name), ], name)
        document = Parser(start_text).parse()
        return template('page.html',
                 name=name,
                 content=HtmlEmitter(document).emit())
    else:
        redirect('/edit/' + name)


@route('/:name', method='POST')
def update_page(name):
    write_to_file(REPO_DIR,
                  PAGES_DIR,
                  os.path.join(PAGES_DIR, name),
                  request.forms.get('content'))
    file_list = [os.path.join(PAGES_DIR, name)]
    commit_to_repo(REPO_DIR, file_list, name)
    redirect(name)


if __name__ == '__main__':
    thread.start_new_thread(start_browser, (WIKI_PORT, ))
    run(host='localhost', port=WIKI_PORT, reloader=False)
