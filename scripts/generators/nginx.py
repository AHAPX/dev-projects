#!/usr/bin/env python
import os
import argparse
from os.path import expanduser

CONF_PATH = '../../conf/'
CONF_NGINX_PATH = os.path.join(CONF_PATH, 'nginx')

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=8000, help='django port')
parser.add_argument('-n', '--name', type=str, default='default', help='project name')
parser.add_argument('-m', '--media', type=str, default='/tmp', help='media path')
parser.add_argument('-s', '--static', type=str, default='/var/www/static/', help='static path')
parser.add_argument('--link', action="store_true", help='create link')

args = parser.parse_args()

replace_data = {
    '[PROJECT]': args.name,
    '[PORT]': str(args.port),
    '[PATH_MEDIA]': args.media,
    '[PATH_STATIC]': args.static,
    '[HOME]': expanduser("~"),
}


conf = open(os.path.join('conf', 'sample.conf')).read()
for k, v in replace_data.iteritems():
    conf = conf.replace(k, v)

file_path = os.path.join(CONF_NGINX_PATH, '{0}.conf'.format(args.name))

f = open(file_path, 'w')
f.write(conf)
f.close()

if args.link:
    os.system('sudo ln -s {0} /etc/nginx/sites-enabled/'.format(os.path.abspath(file_path)))
