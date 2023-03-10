import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [
            f"https://www.superjob.ru/vacancy/search/?={kwargs.get('query')}"
        ]
    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        vacancy_links = response.xpath('//div[@class="_3zucV _1fMKr undefined _1NAsu"]/*/*/*/*/*/*/a/@href').extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_job = response.xpath('//h1/text()').extract_first()
        salary_job = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        location_job = response.xpath('//div[@class="f-test-address _3AQrx"]//text()').extract()
        position_link = response.url
        company_job = response.xpath('//span[@class="_3mfro _1hP6a _2JVkc _2VHxz"]/text() |'
                                     ' //h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract_first()
        yield ParserJobItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)    

    # def parse(self, response: HtmlResponse):
    #     next_page = response.css('a.f-test-link-dalshe::attr(href)') \
    #     .extract_first()

    #     yield response.follow(next_page, callback=self.parse)

    #     vacancy_items  = response.css(
    #         'div.f-test-vacancy-item \
    #         a[class*=f-test-link][href^="/vakansii"]::attr(href)'
    #     ).extract()

    #     for vacancy_link in vacancy_items:
    #         yield response.follow(vacancy_link, self.vacancy_parse)

    # def vacancy_parse(self, response: HtmlResponse):
    #     name = response.css('h1 ::text').extract()

    #     salary = response.css(
    #         'div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"] ::text'
    #     ).extract()

    #     vacancy_link = response.url

    #     site_scraping = self.allowed_domains[0]

    #     yield ParserJobItem(
    #         name=name, \
    #         salary=salary, \
    #         vacancy_link=vacancy_link, \
    #         site_scraping=site_scraping
    #     )

    