"""
PyMySQL acts as a drop-in replacement for mysqlclient on Windows.
Required when USE_MYSQL=true in .env.
"""

import pymysql

pymysql.install_as_MySQLdb()
