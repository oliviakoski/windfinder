from . import spark
from . import config

class Database(object):

    def __init__(self):
        self.username = config.get('PostgreSQL', 'username')
        self.password = config.get('PostgreSQL', 'password')

        instance = config.get('PostgreSQL', 'instance')
        database = config.get('PostgreSQL', 'database')
        self.url = 'jdbc:postgresql://{}:5432/{}'.format(instance, database)

    def save(self, data, table, mode='append'):
        data.write.format('jdbc') \
        .option("url", self.url) \
        .option("dbtable",table) \
        .option("user", self.username) \
        .option("password",self.password) \
        .option("driver", "org.postgresql.Driver") \
        .mode(mode).save()
