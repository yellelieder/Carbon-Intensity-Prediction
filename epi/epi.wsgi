#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/epi/")
from epi import APP as application
application.secret_key = 'epi_key'
application.run(debug=False)

