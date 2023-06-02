from claude_server.server import server_feed

import moderngl_window as mglw
import numpy as np

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
        vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.vertex_array(self.program, vbo, 'in_vert')

        # Initialize uniforms
        self.write_uniform('f4', 'resolution', ClaudeApp.window_size)

        # Queue for sending messages from server process to application process
        self.queue = Queue()

        # Create and launch server process
        self.server = Process(target=server_feed, args=(ClaudeApp.ip, ClaudeApp.port, self.queue,))
        self.server.start()

    def write_uniform(self, np_dtype, name, value):
        try:
            self.program.get(name, None).write(np.array(value).astype(np_dtype).tobytes())
        except Exception:
            pass

    def render(self, time, frametime):
        # Prepare next frame
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)
        self.write_uniform('f4', 'time', time)

        # Read messages fed from server and update uniforms accordingly
        while not self.queue.empty():
            try:
                item = self.queue.get_nowait()
                self.write_uniform(item['np_dtype'], item['name'], item['value'])
            except Exception:
                pass

        # Render frame
        self.vao.render()

    def close(self):
        # Terminate server
        self.server.terminate()
