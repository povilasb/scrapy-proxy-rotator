from setuptools import setup

setup(
    name='scrapy-proxy-rotator',
    version='0.1.0',
    description='Scrapy downloader middleware that rotates proxies.',
    long_description=open('README.rst').read(),
    url='https://github.com/povilasb/scrapy-proxy-rotator',
    author='Povilas Balciunas',
    author_email='balciunas90@gmail.com',
    license='MIT',
    packages=['scrapy_proxy_rotator'],
    zip_safe=False
)
