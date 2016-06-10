from __future__ import print_function
import logging
import math
import sys

from progressbar import (
    AdaptiveETA, ProgressBar, BouncingBar, Percentage)
from kinto_http import cli_utils

from . import parse

logger = logging.getLogger(__file__)

PARSE_DEFAULT_SERVER = 'https://api.parse.com'
RECORD_PER_PAGES = 1000


def main(args=None):
    parser = cli_utils.add_parser_options(
        description="Parse2Kinto importer",
        default_bucket=None,
        default_collection=None)

    parser.add_argument('--parse-server',
                        help='Parse API server',
                        type=str, default=PARSE_DEFAULT_SERVER)

    parser.add_argument('--parse-app',
                        help='Your Parse APP ID',
                        type=str)

    parser.add_argument('--parse-rest-key',
                        help='Your Parse APP ID REST API KEY',
                        type=str)

    parser.add_argument('--parse-class',
                        help='The Parse APP class you want to import',
                        type=str)

    args = parser.parse_args(args)
    cli_utils.setup_logger(logger, args)
    kinto_client = cli_utils.create_client_from_args(args)
    parse_client = parse.create_client_from_args(args)

    # Create bucket
    kinto_client.create_bucket(if_not_exists=True)

    # Create collection if doesn't exists yet
    # try:
    #     kinto_client.create_collection(safe=True)
    # except KintoException as e:
    #     if hasattr(e, 'response') and e.response.status_code == 412:
    #         raise KintoException("The collection already exists. Please "
    #                              "delete it first to make a clean import.")
    kinto_client.create_collection(if_not_exists=True)

    # Count number of objects
    count = parse_client.get_number_of_records()

    pages = math.ceil(float(count) / RECORD_PER_PAGES)
    widgets = ['Import: ', Percentage(), ' ', BouncingBar(), ' ', AdaptiveETA()]

    print("Importing %d records from %s" % (count, args.parse_class))

    num_processed = 0

    with ProgressBar(widgets=widgets, max_value=count) as p:
        # Get parse records
        p.update(num_processed)
        for page in range(pages):
            records = parse_client.get_records(page, RECORD_PER_PAGES)

            # Create kinto batch request
            with kinto_client.batch() as batch:
                for record in records:
                    batch.create_record(data=parse.convert_record(record),
                                        safe=True)
                    num_processed += 1

            p.update(num_processed)


if __name__ == '__main__':
    sys.exit(main())
