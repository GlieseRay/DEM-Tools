# -*- coding:utf-8 -*- 
'''
Created on Oct 10, 2012

@author: ray
'''
import os
import urllib
import urlparse
import subprocess


#==============================================================================
# Data Download Helper
#==============================================================================
def wget(url, filename=None, retries=5, wait=1):
    """ use wget to retrieve data """

    result = urlparse.urlparse(url)
    local_filename = os.path.split(result.path)[1]
    if not result:
        raise ValueError('invalid url %s' % url)

    options = ['-t', str(int(retries)),
               '-w', str(float(wait)),
               ]

    command = ['wget', ] + options + [url, ]

    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    popen.communicate()

    if not os.path.exists(local_filename):
        raise RuntimeError('downloading failed.')

    if filename:
        if os.path.exists(filename):
            os.remove(filename)
        os.rename(local_filename, filename)


if __name__ == '__main__':
    #wget('http://tdds.cr.usgs.gov/ned/13arcsec/float/float_zips/n38w121.zip')
    wget('http://img02.taobaocdn.com/tps/i2/T1ws_QXbhkXXb1ZJrl-250-250.jpg', '/tmp/hello.html')
