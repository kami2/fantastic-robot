from requests.adapters import HTTPAdapter
import logging
import requests
from urllib3.connectionpool import HTTPConnectionPool
from urllib3.poolmanager import PoolManager
from urllib3.exceptions import MaxRetryError


class CustomHTTPConnectionPool(HTTPConnectionPool):
    def __init__(self, *args, **kwargs):
        self.refresh_headers_func = kwargs.pop("refresh_headers_func", None)
        super(CustomHTTPConnectionPool, self).__init__(*args, **kwargs)

    def urlopen(self, method, url, body=None, headers=None, retries=None, **kwargs):
        if headers is None:
            headers = self.headers.copy()

        if retries is None:
            retries = self.retries

        while True:
            response = super(CustomHTTPConnectionPool, self).urlopen(
                method, url, body=body, headers=headers, retries=0, **kwargs  # Disable internal retries
            )

            has_retry_after = bool(response.headers.get("Retry-After"))
            if retries and retries.is_retry(method, response.status, has_retry_after):
                if self.refresh_headers_func and callable(self.refresh_headers_func):
                    refreshed_headers = self.refresh_headers_func()
                    headers.update(refreshed_headers or headers)  # Update headers

                retries = retries.increment(method, url, response=response, _pool=self)
                response.drain_conn()
                retries.sleep(response)
                continue

            return response


class CustomPoolManager(PoolManager):
    def __init__(self, num_pools, maxsize, block=False, **kwargs):
        self.refresh_headers_func = kwargs.pop("refresh_headers_func", None)
        super().__init__(num_pools=num_pools, maxsize=maxsize, block=block, **kwargs)

        logging.info(f"CustomPoolManager initialized")

    def _new_pool(self, scheme, host, port, request_context=None):
        logging.info(f"Creating pool for {scheme}://{host}:{port}")

        # Create the connection pool for this scheme
        pool_cls = self.pool_classes_by_scheme.get(scheme, HTTPConnectionPool)

        return pool_cls(
            host=host,
            port=port,
            refresh_headers_func=self.refresh_headers_func,
            **self.connection_pool_kw
        )


class HTTPAdapterWithCustomPool(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.refresh_headers_func = kwargs.pop("refresh_headers_func", None)
        super(HTTPAdapterWithCustomPool, self).__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = CustomPoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            refresh_headers_func=self.refresh_headers_func,
            **pool_kwargs
        )
        self.poolmanager.pool_classes_by_scheme["http"] = CustomHTTPConnectionPool
        self.poolmanager.pool_classes_by_scheme["https"] = CustomHTTPConnectionPool


def get_keep_alive_session(*args, **kwargs):
    adapter = HTTPAdapterWithCustomPool(*args, **kwargs)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
