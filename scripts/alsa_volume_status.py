#!/usr/bin/python3
'''
show the volume level in the status bar

@note
assumes alsa

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

@note
TODO: add logging?

@date Jun 14, 2011
@author Matthew Todd
'''
import subprocess

NUM_SEGMENTS = 12

#
## Exception defs
#
class CustException (Exception):
    '''
    Custom exception

    @date Jun 17, 2011
    @author Matthew Todd
    '''
    def __init__(self, description, exception):
        '''
        @param description String describing what went wrong.
        @param exception Exception the exception that was thrown and caught.
        @date Jun 17, 2011
        @author Matthew Todd
        '''
        self.description = description
        self.exception = exception

    def __repr__(self):
        '''
        '''
        return "%s(description=%r, exception=%r)" % (self.__class__, self.description, self.exception)

    def __str__(self):
        '''
        '''
        return "Exception: %s\n%s" % (self.description, self.exception)

#
## Function defs
#

def get_data():
    try:
        ret = subprocess.check_output(['amixer', 'sget', 'Master'])
    except (subprocess.CalledProcessError, OSError) as e:
        raise CustException('amixer failed', e)

    for line in ret.decode().split('\n'):
        if 'Mono: Playback' in line:
            return line

def get_volume_percentage(volume_line):
    '''
    @param String volume_line the line from pacmd that contains the volume data
    @return number indicating volume level
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    temp = volume_line.strip().split(' ')[3]
    perc = temp[1:-2]
    
    return int(perc) / 100

def get_mute(mute_line):
    '''
    @param String mute_line the line from pacmd that contains the mute data
    @return bool True if muted
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    temp = mute_line.strip().split(' ')[-1]
    mute = temp[1:-1]

    return mute == "off"

def generate_output(vol_perc, is_mute):
    '''
    @param Number vol volume level
    @param Bool is_mute True if output muted
    @return String the output to be printed
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    if is_mute:
        return "Vol: muted"
    else:
        num_on = min(int(vol_perc * NUM_SEGMENTS), NUM_SEGMENTS)

        return "Vol: [" + "-"*num_on + " "*(NUM_SEGMENTS-num_on) + "]"

def print_output(output):
    '''
    B/c wmiir create uses stdin, we need a way to either send EOF or just send
    the data. So we use Popen() with shell=True

    @param String output the output
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    try:
        p = subprocess.Popen('echo "%s" | wmiir create /rbar/vol' % output, shell=True)
        p.wait()
    except (subprocess.CalledProcessError, OSError) as e:
        raise CustException('wmiir create ... failed', e)


def main():
    '''
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    data_line = get_data()

    vol_perc = get_volume_percentage(data_line)
    is_mute = get_mute(data_line)

    output = generate_output(vol_perc, is_mute)

    print_output(output)

if __name__ == '__main__':
    main()


