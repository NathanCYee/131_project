from distutils.log import debug
from app import webapp


webapp.run(host='0.0.0.0', port=80, debug=True)
