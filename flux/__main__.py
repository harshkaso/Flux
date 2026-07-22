import sys
from typing import Any
from flux.core.app import App
from flux.utils.logger import setup_logger, get_logger, shutdown_loggers

setup_logger()
logger = get_logger(__name__)


def bootstrap() -> Any:
    logger.info("bootstrapping application components")
    # metadata
    app = App()
    return app


def main() -> int:
    try:
        app = bootstrap()
        app.run()
        logger.info("application exited successfully.")
        return 0
    except KeyboardInterrupt:
        logger.warning("application interrupted by user.")
        return 0
    except Exception:
        logger.error("an error occured while running the application", exc_info=True)
        return 1
    finally:
        shutdown_loggers()


if __name__ == "__main__":
    sys.exit(main())
