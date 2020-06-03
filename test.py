from crawler import DataCrawler


def main():
    crawler = DataCrawler.DataCrawler('vcb', '01/03/2020')
    crawler.crawl()


if __name__ == '__main__':
    main()
