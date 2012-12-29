# -*- coding:utf-8 -*- 
'''
Created on Oct 10, 2012

@author: ray
'''
import os
import urllib
import urlparse
import subprocess
import tempfile


#==============================================================================
# Data Download Helper
#==============================================================================
def wget(url, filename=None, retries=5, wait=1):
    """ use wget to retrieve data """

    result = urlparse.urlparse(url)
    local_filename = os.path.join(tempfile.gettempdir(), 
        os.path.split(result.path)[1])

    if not result:
        raise ValueError('invalid url %s' % url)

    options = ['-t', str(int(retries)),
               '-w', str(float(wait)),
               '-O', local_filename,
               ]

    command = ['wget', ] + options + [url, ]
    
    subprocess.check_call(command, stdout=subprocess.PIPE)

    if not os.path.exists(local_filename):
        raise RuntimeError('Download failed.')

    if filename: 
        os.rename(local_filename, filename)

if __name__ == '__main__':
    #wget('http://tdds.cr.usgs.gov/ned/13arcsec/float/float_zips/n38w121.zip')
    wget('http://img02.taobaocdn.com/tps/i2/T1ws_QXbhkXXb1ZJrl-250-250.jpg', '/tmp/hello.html')
