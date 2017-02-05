import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    _search_type = ""

    def _format_str(self, string):
        """Formats string to use in a URL by replacing whitespace with '+'s"""
        return "+".join(string.split())


    def start_requests(self):
        url = "https://openlibrary.org/search"

        keyword = getattr(self, "keyword", None)
        author = getattr(self, "author", None)
        subject = getattr(self, "subject", None)

        if keyword is not None:
            keyword = self._format_str(keyword)
            url += "?q=" + keyword
            self._search_type = "keyword"
        elif author is not None:
            author = self._format_str(author)
            url += "/authors?q=" + author
            self._search_type = "author"
        elif subject is not None:
            subject = self._format_str(subject)
            url += "/subject?q=" + subject
            self._search_type = "subject"
        else:
            raise Exception("No title, author or subject specified")

        yield scrapy.Request(url, self.parse_search)


    def parse_search(self, response):
        if self._search_type == "keyword":
            first_result = response.css("ul#siteSearch li a::attr(href)").extract_first()
            callbk = self.parse_open
        elif self._search_type == "author":
            first_result = response.css("ul.authorList li a::attr(href)").extract_first()
            callbk = self.parse
        elif self._search_type == "subject":
            raise NotImplementedError("Not implemented, my man")

        if first_result is not None:
            first_result = response.urljoin(first_result)
            yield scrapy.Request(first_result, callback=callbk)


    def parse_open(self, response):
        first_result = response.css("table#editions tbody tr .title a::attr(href)").extract_first()
        if first_result is not None:
            first_result = response.urljoin(first_result)
            # self.log("LOOK HEEEEERE!!!! " + first_result)
            yield scrapy.Request(first_result, callback=self.parse)


    def parse(self, response):
        if self._search_type == "keyword":
            self.log("AAAARARGGGHHHHH " + response.css(".editionCover img::attr(src)").extract_first())
            yield {
                "coverImg": response.css(".editionCover img::attr(src)").extract_first(),
                "dowloadLinks": response.css("#readBooks a").extract(),
            }
        elif self._search_type == "author":
            for book in response.css("ul#siteSearch li"):
                yield {
                    "title": book.css(".booktitle a::text").extract_first(),
                }

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
