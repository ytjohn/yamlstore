import sys, os, bottle

sys.path = ['/home/ytjohn/yamldb/'] + sys.path
os.chdir(os.path.dirname(__file__))

import yamldb # This loads your application

application = bottle.default_app()