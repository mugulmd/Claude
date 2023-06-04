from claude_server.app import ClaudeApp

from moderngl_window.resources import register_dir

from argparse import ArgumentParser
from pathlib import Path


# Command line interface
parser = ArgumentParser(
    prog='claude'
)

parser.add_argument('--res', type=str, default=None)
parser.add_argument('--frag', type=str, default='wave.frag')
parser.add_argument('--ip', type=str, default='127.0.0.1')
parser.add_argument('--port', type=int, default=65432)
parser.add_argument('--title', type=str, default='Claude')
parser.add_argument('--size', type=int, nargs=2, metavar=('W', 'H'), default=[800, 600])

args = parser.parse_args()

# Register resources directories
ClaudeApp.resource_dir = (Path(__file__).parents[1] / 'resources').resolve()
if args.res:
    ClaudeApp.resource_dir = args.res

# Configuration
ClaudeApp.fragment_shader = args.frag
ClaudeApp.ip = args.ip
ClaudeApp.port = args.port
ClaudeApp.title = args.title
ClaudeApp.window_size = (args.size[0], args.size[1])

# Start application
ClaudeApp.run()
