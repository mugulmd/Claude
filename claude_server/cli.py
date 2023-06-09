from argparse import ArgumentParser


def create_parser():
    """Command line interface parser for the Claude server application."""

    parser = ArgumentParser(
        prog='claude_server',
        description='Start the Claude server application with a given fragment shader.'
    )

    parser.add_argument(
        '--frag', type=str, default=None,
        help="Filepath to the input fragment shader.\n"
             "If left to default value, a demo wave shader will be used."
    )
    parser.add_argument(
        '--tex', type=str, default=None,
        help="Filepath to the base folder containing the texture folders.\n"
             "If left to default value, no texture will be loaded."
    )

    parser.add_argument(
        '--ip', type=str, default='127.0.0.1',
        help="Server IP address.\n"
             "Default: %(default)s"
    )
    parser.add_argument(
        '--port', type=int, default=65432,
        help="Server port.\n"
             "Default: %(default)s"
    )

    parser.add_argument(
        '--title', type=str, default='Claude',
        help="Window title.\n"
             "Default: %(default)s"
    )
    parser.add_argument(
        '--size', type=int, nargs=2, metavar=('W', 'H'), default=[800, 600],
        help="Window initial size.\n"
             "Default: %(default)s"
    )

    parser.add_argument(
        '--verbose', type=str, default='info',
        help="Verbose level (debug, info, warning, error, critical).\n"
             "Default: %(default)s"
    )

    return parser
