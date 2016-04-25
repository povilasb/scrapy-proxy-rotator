=====
About
=====

.. image:: https://travis-ci.org/povilasb/scrapy-proxy-rotator.svg?branch=master
.. image:: https://coveralls.io/repos/github/povilasb/scrapy-proxy-rotator/badge.svg?branch=master :target: https://coveralls.io/github/povilasb/scrapy-proxy-rotator?branch=master

This is a `Scrapy <http://scrapy.org/>`_ downloader middleware that sets proxy
server for requests.
Currently proxy servers are rotated randomly.
In the future more rotation strategies will be supported.

Configuration
=============

Scrapy settings file::

    DOWNLOADER_MIDDLEWARES = {
        'scrapy_proxy_rotator.ProxyMiddleware': 1,
    }

    PROXY_ROTATOR = {
        'username': 'user1',
        'password': 'pass1',
        'proxies_file': 'proxies.txt',
    }

In proxies file proxy server must be formatted like this `http://host:port`.
