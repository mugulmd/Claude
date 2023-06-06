from argparse import ArgumentParser


def create_parser():
    """Command line interface parser for the Claude server application."""
    parser = ArgumentParser(
        prog='claude_server',
        description='Start the Claude server application with a given fragment shader.'
    )

    parser.add_argument(
        '--res', type=str, default=None,
        help="Filepath to the resource folder containing the fragment shader.\n"
             "If left to default value, Claude's internal resources folder will be used."
    )
    parser.add_argument(
        '--frag', type=str, default='wave.frag',
        help="Filename of the fragment shader to use.\n"
             "Default: %(default)s"
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

    return parser
