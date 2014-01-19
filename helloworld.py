from bottle import route, run, error
import yaml
import os, os.path

def config():
  basedir = '/Users/jhogenmiller/devel/devicedb/data'
  dirs = {
    'tagdata': '%s/tags' % basedir,
    'devicedata': '%s/devices' % basedir
  }
  return dirs

@route('/api/v<version:int>/show/<category>/')
@route('/api/v<version:int>/show/<category>/<id>')
def showtags(version, category, id=None):

  if id == None:
    return yaml.dump(getall(category))

  return yaml.dump(getitem(category, id))

def getall(type):
  dirs = config()

  if type == 'tags':
    path = dirs['tagdata']
  elif type == 'devices':
    path = dirs['devicedata']

  items = {
    type: []
  }

  for root, _, files in os.walk(path):
    for f in files:
      if f == '.gitkeep':
        continue
      else:
        items[type].append(f)

  return items


def getitem(type, id):

  dirs = config()

  if type == 'tags':
    filename = '%s/%s' % (dirs['tagdata'], id)
  elif type == 'devices':
    filename = '%s/%s' % (dirs['devicedata'], id)


  dirs = config()
  try:
    datafile = open(filename, 'r')
  except:
    result = {'error': 'bad id'}
    return result

  #datfile = open(filename, 'r')

  data = yaml.load(datafile)
  return data

#@error(403)
def mistake403(code):
    return 'There is a mistake in your url! %s' % code

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

run(host='localhost', port=8080, debug=True)