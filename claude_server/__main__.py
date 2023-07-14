from claude_server.app import ClaudeApp
from claude_server.cli import create_parser

from moderngl_window import run_window_config
from moderngl_window.resources import register_dir

from pathlib import Path
import logging


# Command line interface
parser = create_parser()
args = parser.parse_args()

# Register resources directory
internal_resources_dir = (Path(__file__).parents[1] / 'resources').resolve()
register_dir(internal_resources_dir)
ClaudeApp.resource_dir = internal_resources_dir

# Log level coloring
logging.addLevelName(
    logging.INFO,
    '\u001b[32mINFO\u001b[0m'
)
logging.addLevelName(
    logging.WARNING,
    '\u001b[33mWARNING\u001b[0m'
)
logging.addLevelName(
    logging.ERROR,
    '\u001b[31mERROR\u001b[0m'
)
logging.addLevelName(
    logging.CRITICAL,
    '\u001b[31m\u001b[1mCRITICAL\u001b[0m'
)

# Configuration
logging.basicConfig(
    format='%(asctime)s - [%(levelname)s]::%(filename)s::%(funcName)s::%(lineno)d - %(message)s',
    level=args.verbose.upper()
)
ClaudeApp.log_level = logging.getLevelName(args.verbose.upper())
if args.frag:
    ClaudeApp.fragment_shader = args.frag
if args.tex:
    ClaudeApp.tex_folder = args.tex
ClaudeApp.ip = args.ip
ClaudeApp.port = args.port
ClaudeApp.title = args.title
ClaudeApp.window_size = (args.size[0], args.size[1])

# Start application using a pyglet window
run_window_config(ClaudeApp, args=['-wnd', 'pyglet'])
