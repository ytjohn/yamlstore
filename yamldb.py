__author__ = 'jhogenmiller'
from bottle import route, run, error
import yaml
import os, os.path

def config():
  basedir = '/Users/jhogenmiller/devel/devicedb/data'
  dirs = {
    'base': basedir,
    'tagdata': '%s/tags' % basedir,
    'devicedata': '%s/devices' % basedir
  }
  return dirs


# /api/v<version>/<namespace>/<path>
# /api/v<version>/<namespace>/<path>:<key>
# /api/v<version>/_ - restricted namespace starts with _

@route('/api/v<version:int>/', method='GET')
@route('/api/v<version:int>/<namespace>', method='GET')
@route('/api/v<version:int>/<namespace>/<category>', method='GET')
@route('/api/v<version:int>/<namespace>/<category>/<name>', method='GET')
@route('/api/v<version:int>/<namespace>/<category>/<name>/<key>', method='GET')
def show(version, namespace=None, category=None, name=None, key=None):
  """

  @param namespace:
  @param category:
  @param name:
  @param key:
  @return:
  """

  if namespace == None:
    return shownamespaces()
  else:
    return "version: %s, namespace: %s, category: %s, name: %s, key: %s" % (version, namespace, category, name, key)


def shownamespaces():
  conf = config()
  fullpath = conf['base']

  list = listdirectory(fullpath)
  return yaml.dump(list)

def listdirectory(fullpath):

  items = []

  for f in os.listdir(fullpath):
    if f in ['.gitkeep', '.gitignore', '.git']:
      continue
    else:
      items.append(f)

  return items

run(host='localhost', port=8080, debug=True)

