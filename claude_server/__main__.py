from claude_server.app import ClaudeApp
from claude_server.cli import create_parser

from moderngl_window import run_window_config
from moderngl_window.resources import register_dir

from pathlib import Path


# Command line interface
parser = create_parser()
args = parser.parse_args()

# Register resources directory
ClaudeApp.resource_dir = (Path(__file__).parents[1] / 'resources').resolve()
if args.res:
    ClaudeApp.resource_dir = args.res

# Configuration
ClaudeApp.fragment_shader = args.frag
ClaudeApp.ip = args.ip
ClaudeApp.port = args.port
ClaudeApp.title = args.title
ClaudeApp.window_size = (args.size[0], args.size[1])

# Start application using a pyglet window
run_window_config(ClaudeApp, args=['-wnd', 'pyglet'])
