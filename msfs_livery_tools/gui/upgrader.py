from tkinter import messagebox
import webbrowser
from github3 import GitHub
from github3.repos import Repository
from github3.repos.release import Release
import __main__

class Tag(object):
    """Comparable tags"""
    version:int
    subversion:int
    revision:int
    
    def __init__(self, tag:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tag = tag.strip('v')
        self.version, self.subversion, self.revision = tag.split('.')
    
    def __gt__(self, other)->bool:
        if not isinstance(other, Tag):
            raise NotImplemented
        if self.version > other.version:
            return True
        if self.version == other.version:
            if self.subversion > other.subversion:
                return True
            if self.subversion == other.subversion and self.revision > other.revision:
                return True
        return False
    
    def __eq__(self, other)->bool:
        if not isinstance(other, Tag):
            raise NotImplemented
        if self.version == other.version and self.subversion == other.subversion and self.revision == other.revision:
            return True
        return False
    
    def __ge__(self, other)->bool:
        if self > other or self == other:
            return True
        return False
    
    def __lt__(self, other)->bool:
        if self == other or self > other:
            return False
        return True

    def __le__(self, other)->bool:
        if self == other or self < other:
            return True
        return False
    
    def __str__(self)->str:
        return f'v{self.version}.{self.subversion}.{self.revision}'

class Upgrader(object):
    """Blocking package upgrader. Should be run in another process.
    """
    anonymous:GitHub
    repository:Repository
    current:Tag
    newest:Release
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = Tag(f'v{__main__.VERSION}.{__main__.SUBVERSION}.{__main__.REVISION}')
    
    def run(self):
        print(f'Running version {self.current}')
        self.anonymous = GitHub()
        self.repository = self.anonymous.repository('leandroarndt', 'msfs_livery_tools')
        releases = self.repository.releases()
        newest_tag = Tag('v0.0.0')
        for r in releases:
            if Tag(r.tag_name) > newest_tag:
                newest_tag = Tag(r.tag_name)
                self.newest = r
        if newest_tag > self.current:
            print(f'Found new version {newest_tag}.')
            if messagebox.askokcancel(
                title='New version found!',
                message=f'There is a new MSFS Livery Tools version available ({newest_tag}). Open download page?'
            ):
                webbrowser.open(self.newest.html_url)