from hamcrest import assert_that, is_
from mock import patch, MagicMock

from scrapy_proxy_rotator import proxy_auth_header, ProxyMiddleware


def test_proxy_auth_header_returns_base64_encoded_proxy_username_and_password():
    auth_header = proxy_auth_header('user1', 'pass')

    assert_that(auth_header, is_('Basic dXNlcjE6cGFzcw==\n'))


@patch('scrapy_proxy_rotator.read_proxies')
def test_contructor_sets_proxy_rotator_specific_settings(read_proxies_mock):
    proxy_settings = MagicMock()
    settings = {'PROXY_ROTATOR': proxy_settings}

    middleware = ProxyMiddleware(settings)

    assert_that(middleware.settings, is_(proxy_settings))


@patch('scrapy_proxy_rotator.read_proxies')
def test_contructor_reads_proxies_from_file_specified_in_settings(
        read_proxies_mock):
    settings = {'PROXY_ROTATOR': {
        'username': 'dummy',
        'password': 'dummy',
        'proxies_file': '/tmp/proxies.txt',
    }}

    middleware = ProxyMiddleware(settings)

    read_proxies_mock.assert_called_with('/tmp/proxies.txt')


@patch('scrapy_proxy_rotator.read_proxies')
def test_process_request_sets_proxy_for_request(read_proxies_mock):
    middleware = ProxyMiddleware(MagicMock())
    middleware.set_proxy = MagicMock()

    middleware.process_request('request', 'dummy')

    middleware.set_proxy.assert_called_with('request')


@patch('scrapy_proxy_rotator.read_proxies')
def test_set_proxy_sets_random_proxy_in_request_meta_info(read_proxies_mock):
    middleware = ProxyMiddleware(MagicMock())
    middleware.random_proxy = MagicMock(return_value='1.2.3.4')
    request = MagicMock()

    middleware.set_proxy(request)

    request.meta.__setitem__.assert_called_with('proxy', '1.2.3.4')


@patch('scrapy_proxy_rotator.proxy_auth_header')
@patch('scrapy_proxy_rotator.read_proxies')
def test_set_proxy_sets_authorization_header_in_request_meta_info(
        read_proxies_mock, auth_header_mock):
    auth_header_mock.return_value = 'Basic abc123=='

    middleware = ProxyMiddleware(MagicMock())
    request = MagicMock()

    middleware.set_proxy(request)

    request.headers.__setitem__.assert_called_with(
        'Proxy-Authorization', 'Basic abc123==')
