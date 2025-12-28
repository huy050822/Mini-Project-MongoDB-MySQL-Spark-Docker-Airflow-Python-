import logging 

def set_up_logging():
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
        force=True
    )

    logging.info("Logging initialized")
