#! /usr/bin/env python
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


REPO_DIR = os.getcwdu()
PAGES_DIR = ".hgwiki"
WIKI_PORT = 8001

init(dict(
    use_database=False,
))

file_path = os.path.dirname(os.path.realpath(__file__))

config(dict(
    mode='dev',
    dev_port=WIKI_PORT,
    use_static=True,
    static_url='/static/*:file/',
    static_root=os.path.join(file_path, 'static/'),
    template_root=os.path.join(file_path, 'templates/')
))



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
    webbrowser.open('http://localhost:%s' % (WIKI_PORT, ))

if __name__ == '__main__':
    thread.start_new_thread(start_browser, ())
    run()
