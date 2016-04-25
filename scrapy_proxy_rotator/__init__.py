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
