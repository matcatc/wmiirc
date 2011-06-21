#!/usr/bin/python3
'''
This simple python script deterimines whether CAPS lock is on or not.

Polling based.

TODO: add logging?

TODO: add program options?
    - poll period

@date Jun 21, 2011
@author Matthew Todd
'''

import subprocess
import time

POLL_PERIOD = 1        # number of seconds between polls

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

def decodeLine(line):
    '''
    decodes the data line to determine whether caps is on
    @return True if caps is on
    @date Jun 21, 2011
    @author Matthew Todd
    '''
    return line[-1] == '1'

def isCapsOn():
    '''
    @throws CustException
    @throws Exception
    @return True if caps is on
    @date Jun 21, 2011
    @author Matthew Todd
    '''
    try:
        ret = subprocess.check_output(['xset', 'q'])
    except (subprocess.CalledProcessError, OSError) as e:
        raise CustException('xset q failed', e)

    for line in ret.decode().split('\n'):
        if 'LED' in line:
            return decodeLine(line)

    raise Exception("didn't find the desired line")

def genOutput(bCaps):
    '''
    @param bCaps Boolean True if caps lock is on
    @return String string to be printed
    @date Jun 21, 2011
    @author Matthew Todd
    '''
    if bCaps:
        return "CAPS ON"
    else:
        return "caps off"

def printOutput(output):
    '''
    @throws CustException
    @param output String output to print
    @date Jun 21, 2011
    @author Matthew Todd
    '''
    try:
        p = subprocess.Popen('echo "%s" | wmiir create /rbar/caps' % output, shell=True)
        p.wait()
    except (subprocess.CalledProcessError, OSError) as e:
        raise CustException('wmiir create ... failed', e)

def notify(output):
    '''
    @throws CustException
    @param output String output to print
    @date Jun 21, 2011
    @author Matthew Todd
    '''
    try:
        subprocess.check_call(['notify-send', output])
    except (subprocess.CalledProcessError, OSError) as e:
        raise CustException('notify-send failed, e')

def main():
    previous = ''
    while True:
        output = genOutput(isCapsOn())
        if previous != output:
            printOutput(output)
            notify(output)

        previous = output
        time.sleep(POLL_PERIOD)

if __name__ == '__main__':
    main()

