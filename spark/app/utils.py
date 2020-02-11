from . import spark
from . import config

class CSVFile(object):

    def __init__(self,name):
        self.name = name
        bucket = config.get('AWS', 'bucket')
        self.path = 's3a://{}/{}'.format(bucket, self.name)
    def load(self):
        print(self.path)
        csv = spark.read.csv(self.path, header=True, inferSchema=True)
        #df = spark.read.format('csv').options(header='true', inferSchema='true').load("s3a://wind-toolkit-csv/b'20070122140000'.csv")
        return csv

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

    

#     def load(self, table):
#         return spark.read.format('jdbc').options(**self._opt(table)).load()

#     def query(self, query):
#         return self.load('({}) AS frame'.format(query))
