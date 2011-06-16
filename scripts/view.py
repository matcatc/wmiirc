#!/usr/bin/python3
'''
Select the next/previous view.

If input is "next", go to next; if input is "previous", go to previous.

@license
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

@date Jun 13, 2011
@author Matthew Todd
'''

import sys
import subprocess


def usage():
    print("usage: ", sys.argv[0], " <next/previous>")

def get_tags():
    '''
    @return a list of the tags currently in use, in the order the appear naturally (alphabetical)
    @date Jun 13, 2011
    @author Matthew Todd
    '''
    try:
        ret = subprocess.check_output(['wmiir', 'ls', '/tag/'])
    except (subprocess.CalledProcessError, OSError) as e:
        # TODO: handle
        raise

    tags = [x.rstrip('/ ') for x in ret.decode().split('\n') if x != '']
    tags.remove('sel')

    return tags


def get_current_tag():
    '''
    @return the currently selected tag
    @date Jun 13, 2011
    @author Matthew Todd
    '''
    try:
        ret = subprocess.check_output(['wmiir', 'read', '/tag/sel/ctl'])
    except (subprocess.CalledProcessError, OSError) as e:
        # TODO: handle
        raise

    return ret.decode().split('\n')[0]


def view_tag(tag):
    '''
    sets the current tag to be the given one

    @throws TODO
    @date Jun 13, 2011
    @author Matthew Todd
    '''
    print("DEBUG: switching to tag: ", tag)

    try:
        subprocess.check_call(['wmiir', 'xwrite',  '/ctl', 'view', tag])
    except (subprocess.CalledProcessError, OSError) as e:
        # TODO: handle
        raise


def main():
    '''
    @date Jun 13, 2011
    @author Matthew Todd
    '''
    if len(sys.argv) != 2:
        return usage()

    tags = get_tags()
    current_tag = get_current_tag()

    index = tags.index(current_tag)
    num_tags = len(tags)
    dir = sys.argv[1]
    if dir == 'next' or dir == 'n':
        next_index = (index + 1) % num_tags
    elif dir == 'previous' or dir == 'p' or dir == 'prev':
        next_index = (index - 1) % num_tags
    else:
        next_index = index

    view_tag(tags[next_index])


if __name__ == '__main__':
    main()
