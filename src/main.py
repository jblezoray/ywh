

import sys
import logging

from core import consumer
from core import crawler
from config.config import CRAWL_INTERVAL_SECONDS
from config.containers import Container

CRAWLER_ARG="-crawler"
CONSUMER_ARG="-consumer"
ARGS=[
    CRAWLER_ARG,
    CONSUMER_ARG,
]

def main():
    
    if len(sys.argv)<2 or ((run_type := sys.argv[1]) not in ARGS):
        args_list = ", ".join(ARGS)
        print(f"This program requires an argument in {args_list}.") 
        exit(1)

    container = Container()
    container.init_resources()

    if run_type == CRAWLER_ARG:
        logging.info("Crawler started.")
        container.wire(modules=[crawler])
        crawler.start(CRAWL_INTERVAL_SECONDS)

    elif run_type == CONSUMER_ARG:
        logging.info("Consumer started.")
        container.wire(modules=[consumer])
        consumer.start()

if __name__ == "__main__":
    main()
