#!/usr/bin/python3
'''
show the volume level in the status bar

@note
assumes pulse audio

@par
assumes only one output (sink) line

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

@date Jun 14, 2011
@author Matthew Todd
'''
import subprocess

MAX_VOL = 0x10000
NUM_SEGMENTS = 10

def get_data():
    try:
        ret = subprocess.check_output(['pacmd', 'dump'])
    except (subprocess.CalledProcessError, OSError) as e:
        # TODO: handle
        raise

    for line in ret.decode().split('\n'):
        if line.startswith('set-sink-volume'):
            volume_line = line
        elif line.startswith('set-sink-mute'):
            mute_line = line

    return (volume_line, mute_line)

def get_volume(volume_line):
    '''
    @param String volume_line the line from pacmd that contains the volume data
    @return number indicating volume level
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    vol = volume_line.split(' ')[-1]
    
    print("DEBUG: vol = %s" % vol)

    return int(vol, 16)

def get_mute(mute_line):
    '''
    @param String mute_line the line from pacmd that contains the mute data
    @return bool True if muted
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    mute = mute_line.split(' ')[-1]

    print("DEBUG: mute = %s" % mute)

    return mute == "yes"

def generate_output(vol, is_mute):
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
        segment_width = MAX_VOL / NUM_SEGMENTS
        num_on = min(int(vol / segment_width), NUM_SEGMENTS)

        print("DEBUG: vol = %d, segment_width = %f, num_on = %d\n" %(vol, segment_width, num_on))

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
        # TODO: handle
        raise


def main():
    '''
    @date Jun 14, 2011
    @author Matthew Todd
    '''
    volume_line, mute_line = get_data()

    vol = get_volume(volume_line)
    is_mute = get_mute(mute_line)

    output = generate_output(vol, is_mute)

    print_output(output)
    
    # TODO: delete when done debugging
#    try:
#        subprocess.check_call(['notify-send', output])
#    except (subprocess.CalledProcessError, OSError) as e:
#        raise


if __name__ == '__main__':
    main()


