import platform
import pymysql
separator = '\\' if platform.system() == 'Windows' else '/'


pymysql.install_as_MySQLdb()