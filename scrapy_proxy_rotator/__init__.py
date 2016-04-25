"""Proxy rotator for Scrapy. """

import base64
import random


class ProxyMiddleware(object):
    """Donwloader middleware that sets proxies for requests.

    Proxies are rotated for each request.
    """

    def __init__(self, settings):
        self.settings = settings.get('PROXY_ROTATOR')

        self.username = self.settings['username']
        self.password = self.settings['password']

        self.proxies = read_proxies(self.settings['proxies_file'])

        self.remove_proxy_for_status_codes = \
            self.settings['remove_proxy_for_status_codes']
        self.blacklisted_proxies = []


    @classmethod
    def from_settings(cls, settings):
        """Constructs proxy middleware from specified settings.

        Args:
            settings (scrapy.settings.Settings): crawler settings.

        Returns:
            ProxyMiddleware
        """
        return ProxyMiddleware(settings)


    def process_request(self, request, spider):
        """Called for every request.

        Args:
            request (scrapy.Request)
        """
        self.set_proxy(request)


    def process_response(self, request, response, spider):
        """Called for every response.

        Args:
            request (scrapy.Request)
            response (scrapy.Response)
        """
        if self.should_remove_proxy(response):
            self.blacklisted_proxies.append(request.meta['proxy'])

        return response


    def set_proxy(self, request):
        """Sets proxy server for request.

        Args:
            request (scrapy.Request)
        """
        request.meta['proxy'] = self.random_proxy()
        request.headers['Proxy-Authorization'] = proxy_auth_header(
            self.username, self.password)


    def random_proxy(self):
        """
        Returns:
            str: random proxy address.
        """
        return random.choice(self.proxies)


    def should_remove_proxy(self, response):
        """
        Args:
            response (scrapy.Response): response object used to get status
                code.

        Returns:
            bool: True if proxy server should be blacklisted, meaning
                it will not be used for future requests.
        """
        return response.status in self.remove_proxy_for_status_codes


def proxy_auth_header(user, password):
    """
    Args:
        user (str): proxy server username.
        password (str): user password.

    Returns:
        str: proxy authentication header.
    """
    return 'Basic ' + base64.encodestring('%s:%s' % (user, password))


def read_proxies(fname):
    """Read proxy list from ips.txt.

    Returns:
        [str]: proxy IPs.
    """
    txt_file = open(fname, 'r')
    return [line.strip() for line in txt_file.readlines()]
