"""
The flask application package.
"""

from flask import Flask, session
#from flask_kvsession import KVSessionExtension
#from simplekv.memory.redisstore import RedisStore

app = Flask(__name__)
#store = RedisStore(redis.StrictRedis())
#KVSessionExtension(store, app)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.jinja_env.globals.update(str=str)

SESSION_TYPE = 'filesystem'

import TestFlaskJadeWeb.views
