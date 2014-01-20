__author__ = 'jhogenmiller'
from bottle import route, run, error
import yaml
import sys
import os, os.path
from dulwich.repo import Repo

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
def show(version, namespace=None, path=None):
  """
  Show a yaml item.
  @param version: version of api to use (future proofing)
  @param namespace: namespace item to show resides in
  @param path: path to yaml item
  @return:
  """
  
  conf = config()
  base = conf['base']

  if path == None:
      return getItem(base, namespace)
  else:
      base = "%s/%s" % (conf['base'], namespace)
      return getItem(base, path)
    
  return "something crazy happened"

@route('/api/v<version:int>/<namespace>', method='POST')
@route('/api/v<version:int>/<namespace>/', method='POST')
@route('/api/v<version:int>/<namespace>/<path:path>', method='POST')
def update(version, namespace=None, path=None):
    """Here we are going to update a yaml item.
    @param version: version of api to use (future proofing)
    @param namespace: namespace that item resides in
    @param path: path to yaml item
    @return: 
    """
    
    # This is going to be a bit tricker than just showing a file. We have to walk
    # the path, find the last valid directory and then create directories until we get
    # to the last entry, the filename itself. If we were doing filename/keys, then we would
    # have a trickier conundrum, which is why I think the final form should be filename:key
    # instead of just filename/key.
    
    if namespace == None:
        # We can't do anything without a namespace, so let's fail.
        return "Failure: Must specify a namespace!"
    elif path == None:
        # We want to create the namespace.
        return makenamespace(namespace)[1]
    else:
        # No we update the file, or try to.
        return updatefile(namespace, path)[1]
    
    return None
    
def updatefile(namespace, path, data="filler: blank"):
    """ Make/Update a file within a namespace. If necessary, create all preceeding directories
    leading up to that file.
    @param: namespace: namespace to create within
    @param: path: file path to create
    @return: [0] True/False on success, [1] String describing success/failure
    """
    
    conf = config()
    base = conf['base']
    namespacepath = "%s/%s" % (base, namespace)
    fullpath = "%s/%s" % (namespacepath, path)
  
    # Let's make sure the namespace is there.
    checknamespace = makenamespace(namespace)
    if not checknamespace[0]:
        return (False, 'Namespace creation failure: %s' % checknamespace[1])
    
    # Is it already a file?
    if os.path.isfile(fullpath):
        return (True, 'Already a file. Just need to update it!')
    elif os.path.isdir(fullpath):
        return (False, 'This is a directory, can not update!')
    
    # Now we are left with a non-file or directory that we have to create.
    elements = fullpath.split('/')
    # pop the filename off the list, and then re-create the path without it
    target = elements.pop(-1)
    pre = '/'.join(elements)
    if not makedir(pre):
        return (False, 'Could not create preceding directory %s' % pre)
    
    # Now all we have to do is create the file with whatever data was sent up.
    return writefile(namespacepath, path, data)
    
def writefile(namespacepath, path, data):
    """ Writes data to a file. 
    @param fullpath: fullpath to a file
    @return: True or False
    """
    
    fullpath = "%s/%s" % (namespacepath, path)
    
    # Write the data to the file
    try:
        f = open(fullpath, 'w')
        f.write(data)
        f.close()
    except:
        return (False, "Could not write file %s" % fullpath)
    
    # Now add it to git.
    try:
        repo = Repo(namespacepath)
        repo.stage(path)
        # Obviously, we'll want to get this commit info from somewhere else.
        commit_id = repo.do_commit(
             "An API commit", committer="API Committer <api@example.com>")
    except:
        return (False, "Could not commit file %s to namespace %s" % (path, namespace))
    
    return (True, "Commited as %s" % commit_id)
    
    
def makenamespace(namespace):
    """ make a namespace and initialize as git repo.
    @param namespace: The namespace directory to create.
    @return: Array: [0]: True/False on success (boolean)
                    [1]: Status detail message (string)
    """
    
    conf = config()
    base = conf['base']
    fullpath = "%s/%s" % (base, namespace)
    
    if os.path.isdir(fullpath):
        # Namespace already exists
        return (True, "namespeace %s already exists, no action taken" % namespace)
    
    # Try to make the directory
    if not makedir(fullpath):
        return (False, "Cold not create directory %s" % fullpath)
    
    # Try to initialize a git repository
    if not creategit(fullpath):
        return (False, "Could not initialize git repo in %s" % fullpath)

    return (True, "Namespace %s created in %s" % (namespace, fullpath))
    
def creategit(fullpath):
    """ Initializes a git repository within a directory.
    @param: fullpath: The full directory name to use.
    @return: True if success, False if not.
    """
    try:
        repo = Repo.init(fullpath)
    except:
        # get the error code:
        e = sys.exc_info()[1][0]
        # 2 = no directory, 17 = .git already exists
        if e == 17:
            pass
        else:
            return False
    
    return True
    
        
def makedir(fullpath):
    """ Attempts to make a directory
    @param fullpath: full filesystem path to create
    @return: return True if success, False if failure.
    """
    
    try:
        os.makedirs(fullpath)
    except OSError:
        if os.path.isdir(fullpath):
            # Someone else made the directory in our absence. 
            return True
        else:
            # There was an error on creation, so make sure we know about it
            return False
        
    return True
    
def listdirectory(fullpath):
  conf = config()
  
  
  if not os.path.isdir(fullpath):
      return None
      
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
    
    # I do a yaml.load and yaml.dump in order to parse the content and
    # (in theory) return only valid yaml.
    content = yaml.load(f.read())
    f.close()
    
    return yaml.dump(content)
    

def getItem(base, path):
    """ This will walk a path forwards to determine if calling a file, directory, or a key.
        If a directory, show the directory contents.
        If a file, show the contents of the file.
        If a file + something else, hopefully that's a key in the file """
    
    if path == None:
        return listdirectory(base)
        
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
            break
            
    # We'll check this file/directory validity again.
    if os.path.isdir(curpath):
        return listdirectory(curpath)
    elif os.path.isfile(curpath):
        # Of course, we would also like to eventually split this out to show individual keys
        return showFile(curpath)
    else:
        return None
        
    return None

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)

