
BOT_NAME = 'freshnews'

SPIDER_MODULES = ['freshnews.spiders']
NEWSPIDER_MODULE = 'freshnews.spiders'

ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'freshnews.pipelines.MySQLPipeline': 2
}

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'helloworld'
DB_DB = 'khmergoo_sequelize'
