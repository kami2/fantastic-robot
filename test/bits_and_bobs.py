from smallworker.utils.response import get_keep_alive_session
from requests.adapters import Retry
import logging


def get_headers(force_refresh=False):
    if force_refresh:
        return {"code": "200"}
    else:
        return {"code": "500"}


def force_headers():
    return get_headers(force_refresh=True)


def test_refresh_headers():
    retry_strategy = Retry(
        total=2,
        status_forcelist=[104, 408, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"],
        backoff_factor=1
    )

    session = get_keep_alive_session(max_retries=retry_strategy, refresh_headers_func=force_headers)

    response = session.get("http://127.0.0.1:5000/test_refresh", headers=get_headers())

    return response.text


if __name__ == "__main__":
    logging.info(test_refresh_headers())
