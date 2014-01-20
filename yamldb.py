__author__ = 'jhogenmiller'
from bottle import route, run, error
import yaml
import os, os.path

def config():
  basedir = '/home/ytjohn/yamldb/data'
  dirs = {
    'base': basedir,
    'tagdata': '%s/tags' % basedir,
    'devicedata': '%s/devices' % basedir,
    'ignores': ['.git', '.gitignore', '.gitkeep']
  }
 
  return dirs


# /api/v<version>/<namespace>/<path>
# /api/v<version>/<namespace>/<path>:<key>
# /api/v<version>/_ - restricted namespace starts with _

@route('/api/v<version:int>', method='GET')
@route('/api/v<version:int>/', method='GET')
@route('/api/v<version:int>/<namespace>', method='GET')
@route('/api/v<version:int>/<namespace>/', method='GET')
@route('/api/v<version:int>/<namespace>/<path:path>', method='GET')
#@route('/api/v<version:int>/<namespace>/<category>/<name>', method='GET')
#@route('/api/v<version:int>/<namespace>/<category>/<name>/<key>', method='GET')
def show(version, namespace=None, path=None):
  """

  @param namespace:
  @param category:
  @param name:
  @param key:
  @return:
  """
  

  if namespace == None:
    return shownamespaces()
  elif path == None:
    return shownamespace(namespace)
  else:
    conf = config()
    base = "%s/%s" % (conf['base'], namespace)
    return getItem(base, path)
    
  return "something crazy happened"


def shownamespaces():
  conf = config()
  fullpath = conf['base']
  ignores = conf['ignores']
  
  list = listdirectory(fullpath)
  return list 

def shownamespace(namespace):
    conf = config()
    fullpath = "%s/%s" % (conf['base'], namespace)
    list = listdirectory(fullpath)
    return list
    
def listdirectory(fullpath):
  conf = config()
  ignores = conf['ignores']
  
  items = []
  
  for f in os.listdir(fullpath):
    if f in ignores:
      continue
    else:
      items.append(f)
  
  return yaml.dump(items)
    
def showFile(fullpath):
    """ Simply read in a file and return it straight up"""
    
    f = open(fullpath, 'r')
    content = f.read()
    return content
    
    
def getItem(base, path):
    """ This will walk a path forwards to determine if calling a file, directory, or a key.
        If a directory, show the directory contents.
        If a file, show the contents of the file.
        If a file + something else, hopefully that's a key in the file """
    
    # let's start walking this path
    for item in path.split('/'):
        curpath = "%s/%s" % (base, item)
        if os.path.isdir(curpath):
            # expand base, continue loop
            # We use sourcedir in case there is no file.
            base = curpath
            next
        elif os.path.isfile(curpath):
            # Yay, we have a file, so everything after this is a key.
            # Stop processing this loop.
            break
        else:
            # We get here if there is no file or directory.
            return None
            
    # We'll check this file/directory validity again.
    if os.path.isdir(curpath):
        return listdirectory(curpath)
    elif os.path.isfile(curpath):
        # Of course, we would also like to split this out to show individual keys
        return showFile(curpath)
    else:
        return None
        
            
            
            
    
    return output

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)

