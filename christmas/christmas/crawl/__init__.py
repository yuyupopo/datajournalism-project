"""
Retrive data from the internet and store in `CHRISTMAS_DATA_PATH`/raw_data
"""

import logging
import json
import os
import sys
import urllib.request
import urllib.parse

from functools import lru_cache


class Crawler:

    __tokens__ = {}

    def __init__(self):
        pass

    @classmethod
    def _get_app_key(cls, app_key):
        _key = cls.__tokens__.get(app_key, None)
        if not _key:
            _key = os.getenv(app_key, None)
            cls.__tokens__[app_key] = _key

        if not _key:
            err_msg = 'key {} is not defined as environmnet variable'.format(
                app_key)
            logging.error(err_msg)
            sys.exit(1)

        return _key

    def _send_request(self, req):
        logging.debug(req)
        res = urllib.request.urlopen(req)
        rescode = res.getcode()

        if rescode == 200:
            logging.debug('response 200')
            res = res.read().decode('utf-8')
            return res
        else:
            logging.error('response: %d', rescode)
            return None


class NaverCrawler(Crawler):

    def __init__(self, base_url):
        self.base_url = base_url

    def search(self, **param):
        # encText = urllib.parse.quote(**encText)
        url = self.base_url.format(**param)
        req = urllib.request.Request(url)

        naver_api_id = self._get_app_key('NAVER_API_ID')
        naver_api_secret = self._get_app_key('NAVER_API_SECRET')
        req.add_header('X-Naver-Client-Id', naver_api_id)
        req.add_header('X-Naver-Client-Secret', naver_api_secret)

        res = self._send_request(req)

        return res


class DataLabSearchCrawler(NaverCrawler):

    def __init__(self):
        url = (
            'https://openapi.naver.com/v1/datalab/search'
            '?startDate={start}&endDate={end}&query={query}'
        )
        super(DataLabSearchCrawler, self).__init__(url)

    def __call__(self, addr):
        encText = urllib.parse.quote(addr)
        res = self.search(query=encText)
        res = json.loads(res)
        addr_body = res['documents']
        if len(addr_body) == 0:
            print('address: {} has no results'.format(addr))
            return None, None

        addr_body = addr_body[0]['address']
        x = float(addr_body['x'])
        y = float(addr_body['y'])
        return x, y


class KakaoCrawler(Crawler):

    def __init__(self, base_url):
        self.base_url = base_url

    def search(self, **param):
        url = self.base_url.format(**param)
        req = urllib.request.Request(url)

        kakao_api = self._get_app_key('KAKAO_KEY')
        kakao_key = 'KakaoAK ' + kakao_api
        req.add_header('Authorization', kakao_key)

        res = self._send_request(req)

        return res


class AddressCoordCrawler(KakaoCrawler):

    def __init__(self):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query={query}'
        super(AddressCoordCrawler, self).__init__(url)

    def __call__(self, addr):
        encText = urllib.parse.quote(addr)
        res = self.search(query=encText)
        res = json.loads(res)
        addr_body = res['documents']
        if len(addr_body) == 0:
            print('address: {} has no results'.format(addr))
            return None, None

        addr_body = addr_body[0]['address']
        x = float(addr_body['x'])
        y = float(addr_body['y'])
        return x, y


class SubwayAddressCrawler(KakaoCrawler):

    def __init__(self):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={query}'
        super(SubwayAddressCrawler, self).__init__(url)

    def __call__(self, addr):
        encText = urllib.parse.quote(addr)
        res = self.search(query=encText)
        res = json.loads(res)
        addr_body = res['documents']
        if not addr_body:
            return None, None, None

        addr_body = addr_body[0]
        road_addr = addr_body['road_address_name']
        x = addr_body['x']
        y = addr_body['y']
        return road_addr, x, y


class SeoulAPICrawler(Crawler):

    def __init__(self, base_url):
        self.base_url = base_url

    def search(self, **param):
        api_key = self._get_app_key('DATASEOUL_KEY')
        param['key'] = api_key

        url = self.base_url.format(**param)
        req = urllib.request.Request(url)

        res = self._send_request(req)

        return res


class WeatherHistoryCrawler(SeoulAPICrawler):

    def __init__(self):

        super(WeatherHistoryCrawler, self).__init__(
            "http://openapi.seoul.go.kr:8088/{key}/json/DailyWeatherStation/1/400/{year}/{region}"
        )

    def __call__(self, year, region):
        region = urllib.parse.quote(region)
        res = self.search(region=region, year=year)
        return res
