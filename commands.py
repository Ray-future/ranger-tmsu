from ranger.api.commands import *
import os

from tmsu import Tmsu
tmsu = Tmsu.findTmsu()

class tmsu_tag(Command):
    """:tmsu_tag

    Tags the current file with tmsu
    """

    def execute(self):
        cf = self.fm.thisfile
        tmsu.tag(cf.basename, self.rest(1))

    def tab(self, tabnum):
            """ Complete with tags"""
            results=[]
            if self.arg(0) == self.arg(-1):
                input_tag=""
                index=1
            else:
                input_tag=self.arg(-1)
                index=-1

            if "=" in input_tag:
                 split_value=input_tag.split("=")[1]
                 split_tag=input_tag.split("=")[0]
                 for value in tmsu.values(split_tag):
                    if value.startswith(split_value):
                        results.append(split_tag + "=" + value)
            else:
                for tag in tmsu.tags():
                    if tag.startswith(input_tag):
                        results.append(tag)
            return (self.start(index) + result for result in results)

class tmsu_untag(Command):
    """:tmsu_untag

    Untags the current file with tmsu
    """

    def execute(self):
        cf = self.fm.thisfile
        tmsu.untag(cf.basename, self.rest(1))

    def tab(self, tabnum):
            """ Complete with tags"""
            results=[]
            if self.arg(0) == self.arg(-1):
                input_tag=""
                index=1
            else:
                input_tag=self.arg(-1)
                index=-1
            cf = self.fm.thisfile

            for tag in tmsu.tags(fileName=cf.basename):
                if tag.startswith(input_tag):
                    results.append(tag)
            return (self.start(index) + result for result in results)

class tmsu_ls(Command):
    """:tmsu_ls

    List tags of the current file with tmsu
    """

    def execute(self):
        cf = self.fm.thisfile
        tags=tmsu.tags(cf.basename)
        self.fm.notify(tags)


import ranger.api
import ranger.core.linemode

@ranger.api.register_linemode     # It may be used as a decorator too!
class MyLinemode(ranger.core.linemode.LinemodeBase):
    name = "tmsu_linemode"

    uses_metadata = False

    def filetitle(self, file, metadata):
        return file.relative_path + str(tmsu.tags(file))

    def infostring(self, file, metadata):
        return file.user
