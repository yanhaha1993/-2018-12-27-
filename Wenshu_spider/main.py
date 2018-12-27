from scrapy import cmdline
# cmdline.execute("scrapy crawl wenshu".split())
cmdline.execute("scrapy crawl wenshu -s JOBDIR=crawls/somespider-1".split())
