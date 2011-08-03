import os
import webbrowser

from time import sleep

# from mercurial import commands
from mercurial import ui
from mercurial import hg
# from mercurial import verify
# Mercurial changed this after 1.8
try:
    from mercurial.scmutil import matchfiles
except ImportError:
    from mercurial.cmdutil import matchfiles


def start_browser(wiki_port):
    """\
    Waits a second for the server to come up and opens a browser window.
    """
    sleep(1)
    webbrowser.open('http://localhost:%s' % (wiki_port, ))
    
def page_exists(pages_dir, page_name):
    """\
    Checks if wiki page (file) exists and returns True or False
    """
    return os.path.exists(os.path.join(pages_dir, page_name))

def write_to_file(repo_dir, pages_dir, filepath, content):
    """\
    Write content to file.
    """
    abs_path_to_pages = os.path.join(repo_dir, pages_dir)
    if not os.path.isdir(abs_path_to_pages):
        os.mkdir(abs_path_to_pages)
    with(open(filepath, 'w')) as page_file:
        page_file.write(content)

def commit_to_repo(repo_dir, files, name):
    """\
    """
    repo = hg.repository(ui.ui(), repo_dir)
    try:
        # Mercurial <= 1.5
        repo.add(files)
    except:
        # Mercurial >= 1.6
        repo[None].add(files)
    match = matchfiles(repo, files or [])
    repo.commit(match=match,
                text="HGWiki: Changed wiki page %s" % (name, ),
                user="hgwiki")

    