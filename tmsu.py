#!/usr/bin/python3
#
# Copyright 2017 Hasan Yavuz Ozderya
#
# This program is free software: you can redistribute it and/or modify
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
#

import sys, os, enum
import subprocess as sp

class Tmsu:
    def __init__(self, tmsu):
        self.tmsu = tmsu

    def info(self):
        try:
            r = self._cmd('info')
        except sp.CalledProcessError as e:
            if e.returncode == 1: # database doesn't exist
                return None
        lines = r.splitlines()
        def psplit(l): return map(lambda x: x.strip(), l.split(':'))
        d = dict(map(psplit, lines))

        return {'root': d['Root path'],
                'size': d['Size'],
                'database':d['Database']}

    def tags(self, fileName=None):
        """Returns a list of tags. If fileName is provided, list item is a tuple of
        (tagname, value) pair."""
        if fileName:
            # Note: tmsu behaves differently for 'tags' command when used
            # interactively and called from scripts. That's why we add '-n'.
            #r = self._cmd('tags -n "{}"'.format(fileName))
            r = self._cmd('tags -1 -n never "{}"'.format(fileName))
            tag_value = []
            tag_value = r.splitlines()
            #for tag in r.splitlines():
            #    tv = tag.split("=")
            #    if len(tv) > 1:
            #        tag_value.append((tv[0], tv[1]))
            #    else:
            #        tag_value.append((tv[0], ""))
            return tag_value
        else:
            return self._cmd('tags').splitlines()

    def tag(self, fileName, tagName, value=None):
        try:
            self._cmd('tag "{}" {}{}'.format(fileName, tagName,
                                             "="+value if value else ""))
            return True
        except sp.CalledProcessError as e:
            print("Failed to tag file.")
            return False

    def untag(self, fileName, tagName, value=None):
        try:
            self._cmd('untag "{}" {}{}'.format(fileName, tagName,
                                               "="+value if value else ""))
            return True
        except sp.CalledProcessError as e:
            print("Failed to untag file.")
            return False

    def rename(self, tagName, newName):
        try:
            self._cmd('rename {} {}'.format(tagName, newName))
            return True
        except sp.CalledProcessError as e:
            print("Failed to rename tag.")
            return False

    def values(self, tagName=None):
        try:
            r = self._cmd('values {}'.format(tagName if tagName else ""))
            return r.splitlines()
        except sp.CalledProcessError as e:
            print("Failed to get value list.")
            return False

    def delete(self, tagName):
        try:
            self._cmd('delete {}'.format(tagName))
            return True
        except sp.CalledProcessError as e:
            print("Failed to delete tag: {}".format(tagName))
            return False

    def _cmd(self, cmd):
        return sp.check_output('tmsu ' + cmd, shell=True, stderr=sp.DEVNULL).decode('utf-8')

    @staticmethod
    def findTmsu():
        import shutil
        tmsu =  shutil.which("tmsu")
        if tmsu:
            return Tmsu(tmsu)
        else:
            return None
