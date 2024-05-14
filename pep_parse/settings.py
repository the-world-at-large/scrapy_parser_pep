from pep_parse.constants import RESULTS_DIR

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'


ROBOTSTXT_OBEY = True

FEEDS = {
    f'{RESULTS_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'overwrite': True,
        'encoding': 'utf8',
        'fields': ['number', 'name', 'status'],
    }
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
