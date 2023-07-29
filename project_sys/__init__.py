import pymysql

# 使得Django的ORM能够识别MySQL的驱动
pymysql.install_as_MySQLdb()
