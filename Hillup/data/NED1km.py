""" Starting point for DEM retrieval utilities.
"""
import os
from sys import stderr
from math import floor, ceil, log
from os import unlink, close, write, makedirs, chmod
from os.path import basename, exists, isdir, join
from httplib import HTTPConnection
from urlparse import urlparse
from StringIO import StringIO
from gzip import GzipFile
from hashlib import md5

from TileStache.Geography import SphericalMercator

from osgeo import gdal, osr
from .download import wget

ideal_zoom = 7 ### log(3 * 36*360 / 256) / log(2) # ~7.2

osr.UseExceptions() # <-- otherwise errors will be silent and useless.

sref = osr.SpatialReference()
sref.ImportFromProj4('+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs')

def quads(minlon, minlat, maxlon, maxlat):
    """ Generate a list of northwest (lon, lat) for 1-degree quads of NED 10m data.
    """
    lon = floor(minlon)
    while lon <= maxlon:

        lat = ceil(maxlat)
        while lat >= minlat:

            yield lon, lat

            lat -= 1

        lon += 1

def datasource(lat, lon, source_dir):
    """ Return a gdal datasource for a NED 10m lat, lon corner.
    
        If it doesn't already exist locally in source_dir, grab a new one.
    """
    # FIXME for southern/western hemispheres
    fmt = 'http://ned.stamen.com/1km/n%02dw%03d.tif.gz'
    url = fmt % (abs(lat), abs(lon))

    #
    # Create a local filepath
    #
    s, host, path, p, q, f = urlparse(url)

    local_dir = 'ned1000m'
    local_dir = join(source_dir, local_dir)

    local_base = join(local_dir, basename(path)[:-7])
    local_path = local_base + '.tif'
    local_temp = local_base + '.temp.tif'
    local_none = local_base + '.404'

    #
    # Check if the file exists locally
    #
    if exists(local_path):
        return gdal.Open(local_path, gdal.GA_ReadOnly)

    if exists(local_none):
        return None

    if not exists(local_dir):
        makedirs(local_dir)
        chmod(local_dir, 0777)

    assert isdir(local_dir)

    #
    # Grab a fresh remote copy
    #
    print >> stderr, 'Retrieving', url, 'in DEM.NED1km.datasource().'

    try:
        wget(url, local_temp)
    except Exception:
        with open(local_none, 'w') as fp:
            fp.write(url)
        return None

    zipped = GzipFile(filename=local_temp, mode='r')
    with open(local_path, 'w') as fp:
        fp.write(zipped.read())

    os.remove(local_temp)

    #
    # The file better exist locally now
    #
    return gdal.Open(local_path, gdal.GA_ReadOnly)

def datasources(minlon, minlat, maxlon, maxlat, source_dir):
    """ Retrieve a list of SRTM1 datasources overlapping the tile coordinate.
    """
    lonlats = quads(minlon, minlat, maxlon, maxlat)
    sources = [datasource(lat, lon, source_dir) for (lon, lat) in lonlats]
    return [ds for ds in sources if ds]
