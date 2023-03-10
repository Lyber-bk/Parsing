from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from parser_job.spiders.hh_ru import HhRuSpider
from parser_job.spiders.superjob_ru import SuperjobRuSpider


if __name__ == '__main__':
    query = 'Менеджер'

    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    
    runner.crawl(HhRuSpider,     query=query)
    runner.crawl(SuperjobRuSpider,     query=query)

    reactor.run()