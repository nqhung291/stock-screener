from crawler import DataCrawler


def main():
    crawler = DataCrawler.DataCrawler('vcb')
    crawler.crawl()


if __name__ == '__main__':
    main()
