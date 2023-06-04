from claude_server.server import server_feed

import moderngl_window as mglw
import numpy as np

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from multiprocessing import Process, Queue


class ClaudeApp(mglw.WindowConfig):

    gl_version = (3, 3)

    # Window configuration
    window_size = (800, 600)
    title = 'Claude'

    # Shader configuration
    vertex_shader = 'default.vert'
    fragment_shader = 'wave.frag'

    # Server configuration
    ip = '127.0.0.1'
    port = 65432

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load shaders
        self.program = self.load_program(
            vertex_shader=ClaudeApp.vertex_shader,
            fragment_shader=ClaudeApp.fragment_shader
        )

        # Geometry: a quad made out of 2 triangles
        vertices = np.array([
            -1.0, -1.0, -1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, -1.0, -1.0, -1.0
        ])

        # Create vertex buffer and vertex array
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.vertex_array(self.program, self.vbo, 'in_vert')

        # Queue for sending messages from server process to application process
        self.queue = Queue()

        # Create and launch server process
        self.server = Process(
            target=server_feed,
            args=(ClaudeApp.ip, ClaudeApp.port, self.queue,)
        )
        self.server.start()

        # Create filewatcher event handler
        self.reload_frag = False
        filewatcher_handler = PatternMatchingEventHandler(
            patterns=[ClaudeApp.fragment_shader],
            ignore_directories=True,
            case_sensitive=True
        )
        filewatcher_handler.on_modified = self.on_frag_changed

        # Create and launch filewatcher
        self.observer = Observer()
        self.observer.schedule(
            filewatcher_handler,
            path=ClaudeApp.resource_dir,
            recursive=False
        )
        self.observer.start()

    def on_frag_changed(self, event):
        self.reload_frag = True

    def write_uniform(self, np_dtype, name, value):
        try:
            self.program.get(name, None).write(np.array(value).astype(np_dtype).tobytes())
        except Exception:
            pass

    def render(self, time, frametime):
        # Prepare next frame
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)
        self.write_uniform('f4', 'time', time)

        # Reload fragment shader
        if self.reload_frag:
            self.reload_frag = False
            try:
                program = self.load_program(
                    vertex_shader=ClaudeApp.vertex_shader,
                    fragment_shader=ClaudeApp.fragment_shader
                )
            except Exception as e:
                print(e)
            self.program = program
            self.vao = self.ctx.vertex_array(self.program, self.vbo, 'in_vert')

        # Read messages fed from server and update uniforms accordingly
        while not self.queue.empty():
            try:
                item = self.queue.get_nowait()
                self.write_uniform(item['np_dtype'], item['name'], item['value'])
            except Exception:
                pass

        # Render frame
        self.vao.render()

    def resize(self, width, height):
        self.write_uniform('f4', 'resolution', (width, height))

    def close(self):
        # Terminate server
        self.server.terminate()

        # Stop filewatcher
        self.observer.stop()
        self.observer.join()
