# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from crawler.items import CrawlerItem
from scrapy.http import HtmlResponse
from scrapy.http import JsonRequest
class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["vietlott.vn"]

    def start_requests(self):
        url = "https://vietlott.vn/ajaxpro/Vietlott.PlugIn.WebParts.Game645ResultDetailWebPart,Vietlott.PlugIn.WebParts.ashx"
        for period in range(600):
            drawId =  "{:05d}".format(period+1)
            headers = {
               "Content-Type":"application/json",
                "X-AjaxPro-Method":"ServerSideDrawResult"
            }

            formdata = {
                "DrawId": drawId,
                "Key": "254fcccf",
                "ORenderInfo": {
                    "ExtraParam1": "",
                    "ExtraParam2": "",
                    "ExtraParam3": "",
                    "FullPageAlias": None,
                    "IsPageDesign": False,
                    "OrgPageAlias": None,
                    "PageAlias": None,
                    "RefKey": None,
                    "SiteAlias": "main.vi",
                    "SiteId": "main.frontend.vi",
                    "SiteLang": "vi",
                    "SiteName": "Vietlott",
                    "SiteURL": "",
                    "System": "1",
                    "UserSessionId": "",
                    "WebPage": None
                }
            }
            yield JsonRequest(url, method="POST", data=formdata, headers=headers, callback=self.parse)

        # yield result
    def parse(self, response):
        body = json.loads(response.body)
        content = body['value']
        RetExtraParam1 = content["RetExtraParam1"]
        selectors = Selector(text=RetExtraParam1).xpath('//div[@class="chitietketqua_title"]/h5/b/text()')
        item = CrawlerItem()
        item["period"] = selectors[0].get().replace("#", "")
        item["date"] = selectors[1].get()
        item["numbers"] = []
        numbers = Selector(text=RetExtraParam1).xpath('//div[@class="day_so_ket_qua_v2"]/span/text()')
        for number in numbers:
            item["numbers"].append(number.get())
        yield item
