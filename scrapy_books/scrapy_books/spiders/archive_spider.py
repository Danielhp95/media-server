import scrapy


class ArchiveSpider(scrapy.Spider):
    name = "archive"
    _search_type = ""

    def _format_str(self, string):
        """Formats string to use in a URL by replacing whitespace with '+'s"""
        return "+".join(string.split())


    def start_requests(self):
        url = "https://archive.org/details/texts"

        keyword = getattr(self, "keyword", None)
        author = getattr(self, "author", None)
        subject = getattr(self, "subject", None)

        # if keyword is not None:
        #     keyword = self._format_str(keyword)
        #     url += "?q=" + keyword
        #     self._search_type = "keyword"
        # elif author is not None:
        if keyword is not None:
            keyword = self._format_str(keyword)
            url += "?and[]=" + keyword
            self._search_type = "keyword"
        else:
            raise Exception("No keyword specified")

        yield scrapy.Request(url, self.parse_search)


    def parse_search(self, response):
        if self._search_type == "keyword":
            first_result = response.css(".results .item-ttl a::attr(href)").extract_first()
            callbk = self.parse
        elif self._search_type == "author":
            raise NotImplementedError("Not implemented, my man")

        if first_result is not None:
            first_result = response.urljoin(first_result)
            yield scrapy.Request(first_result, callback=callbk)


    # def parse_open(self, response):
    #
    #     if first_result is not None:
    #         first_result = response.urljoin(first_result)
    #         # self.log("LOOK HEEEEERE!!!! " + first_result)
    #         yield scrapy.Request(first_result, callback=self.parse)


    def parse(self, response):
        if self._search_type == "keyword":
            # self.log("AAAARARGGGHHHHH " + response.css(".editionCover img::attr(src)").extract_first())
            links = response.css(".quick-down a.download-pill")
            the_link = None
            for link in links:
                if "TORRENT" in link.css("::text").extract_first():
                    the_link = link.css("::attr(href)").extract_first()
            if the_link is not None:
                the_link = response.urljoin(the_link)
            else:
                raise Exception("dammit")
            yield {
                "downloadLink": the_link,
            }
        # elif self._search_type == "author":
        #     for book in response.css("ul#siteSearch li"):
        #         yield {
        #             "title": book.css(".booktitle a::text").extract_first(),
        #         }

        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").extract_first(),
        #         "author": quote.css("span small::text").extract_first(),
        #         "tags": quote.css("div.tags a.tag::text").extract_first(),
        #     }
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
