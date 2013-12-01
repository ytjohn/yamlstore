from bottle import route, run
import yaml

def config():
  basedir = '/Users/jhogenmiller/devel/devicedb/data'
  dirs = {
    'tagdata': '%s/tags' % basedir,
    'devicedata': '%s/devices' % basedir
  }
  return dirs

@route('/hello')
def hello():
  dirs = config()
  tag1file = open('%s/tag1' % dirs['tagdata'], 'r')
  test1file = open('%s/test1' % dirs['devicedata'], 'r')
  tag1data = load(tag1file)
  print tag1data

  return tag1data['members']

@route('/api/v<version:int>/show/<category>/')
@route('/api/v<version:int>/show/<category>/<id>')
def showtags(version, category, id=None):
  if id == None:
    return "show all %s" % category

  return yaml.dump(getitem(category, id))


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


run(host='localhost', port=8080, debug=True)