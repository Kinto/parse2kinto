import logging
import sys

from kinto_http import cli_utils
from kinto_http.exceptions import KintoException

from . import parse

logger = logging.getLogger(__file__)

PARSE_DEFAULT_SERVER = 'https://api.parse.com'


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

    # Get parse records
    records = parse_client.get_records()
    
    # Create kinto batch request
    with kinto_client.batch() as batch:
        for record in records:
            batch.create_record(data=record)


if __name__ == '__main__':
    sys.exit(main())
