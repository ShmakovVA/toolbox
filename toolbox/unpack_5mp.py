#!/usr/bin/env python2.7
import json
import base64

MIMETYPES = {
    'application/pacsoft': '.xml',
    'application/pdf': '.pdf',
    'application/postscript': '.ps',
    'application/unifaun': '.xml',
    'text/zpl': '.zpl',
}


def unpack(file):
    '''
    Unpack files from a 5mp (monkey-print) file.

    e.g.:
        unpack("order-1647560-1453821576.5mp")

        creates:
            order-1657861-1453897053.5mp_0.xml
            order-1657861-1453897053.5mp_1.xml
            order-1657861-1453897053.5mp_2.pdf
            order-1657861-1453897053.5mp_3.ps

        with data from order-1647560-1453821576.5mp
    '''
    with open(file, 'r') as f:
        data = json.loads(f.read())
    for i, d in enumerate(data):
        if d['type'] not in ['FILE', 'DIRECT']:
            continue

        if 'mime_type' in d and d['mime_type'] in MIMETYPES:
            file_ext = MIMETYPES[d['mime_type']]
        else:
            file_ext = '.xml'

        new_file = file + "_%s%s" % (i, file_ext)
        with open(new_file, 'w') as f:
            f.write(base64.decodestring(d['data']))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "usage: %s <5mp_file>" % sys.argv[0]
        sys.exit()
    unpack(sys.argv[1])
    sys.exit()

