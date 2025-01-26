def init_logging():
    import logging

    log = logging.getLogger()
    log.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
    console_handler.setFormatter(formatter)

    log.addHandler(console_handler)

    httpx_logger = logging.getLogger("httpx")

    httpx_logger.setLevel(logging.WARNING)


__all__ = ["init_logging"]
