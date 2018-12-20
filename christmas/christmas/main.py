import argparse
import os

from christmas.common.log import define_logger


def main():
    """Run constellation"""
    parser = argparse.ArgumentParser(prog=__doc__)
    # global arguments
    parser.add_argument(
        '-v', '--verbose', help='verbose mode', action='store_true')
    parser.add_argument(
        '-l', '--logdir', help='log directory',
        default=os.getenv('CHRISTMAS_LOG_PATH')
    )
    mode_parser = parser.add_subparsers(dest="mode")

    # master
    master_parser = mode_parser.add_parser('master')

    # crawl
    crawl_parser = mode_parser.add_parser('crawl')

    # preprocess
    preprocess_parser = mode_parser.add_parser('preprocess')

    # analysis
    analysis_parser = mode_parser.add_parser('analysis')

    args = parser.parse_args()

    if args.logdir is None:
        parser.error(
            'specifiy --logdir in command line or '
            'add CHRISTMAS_LOG_PATH'
        )

    define_logger(args.logdir, args.verbose)

    mode = args.mode
    mode_run_map = {
        'master': master,
        'crawl': master,
        'preprocess': master,
        'analysis': master,
    }

    if mode not in mode_run_map:
        parser.error('Mode: {} invalid. \n Please specify one of: {}'.format(
            mode, ', '.join(list(mode_run_map.keys()))
        ))

    mode_run_map[mode](args)


def master(args):
    pass
