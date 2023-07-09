from claude_server.server import server_feed

import moderngl_window as mglw
import numpy as np

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from multiprocessing import Process, Queue
import os


class ClaudeApp(mglw.WindowConfig):
    """Class centralizing the Claude server application.

    This class is in charge of:
      * window management
      * rendering with OpenGL
      * updating uniforms and the shading program when needed.

    It also manages the server process and filewatcher which allow interactivity.
    """

    # OpenGL version
    gl_version = (3, 3)

    # Window configuration
    window_size = (800, 600)
    title = 'Claude'
    aspect_ratio = None

    # Shader configuration
    vertex_shader = 'default.vert'
    fragment_shader = 'template.frag'

    # Textures base folder
    tex_folder = None

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

        # Queue for sending messages from server process to rendering process
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

        # Uniform cache
        # Used to reset uniforms to their latest value
        # after fragment shader is reloaded
        self.uniform_cache = {}

        # Cache textures
        self.textures = []
        self.tex_locations = {}
        self.load_textures()

        # Store render lopp time
        self.render_time = 0.0

    def load_textures(self):
        if not ClaudeApp.tex_folder:
            return

        for dir_entry in os.scandir(ClaudeApp.tex_folder):
            # At this stage we only take directories into account
            if not dir_entry.is_dir(follow_symlinks=False):
                continue

            locations = []

            # Iterate through texture files in alphabetical order
            for tex_name in sorted(os.listdir(dir_entry.path)):
                # Load texture and bind to next texture unit available
                try:
                    tex = self.load_texture_2d(os.path.join(dir_entry.path, tex_name))
                    loc = len(self.textures)
                    tex.use(location=loc)
                    self.textures.append(tex)
                    locations.append(loc)
                except Exception as e:
                    print(e)
                    continue

            if len(locations) > 0:
                self.tex_locations[dir_entry.name] = locations

    def on_frag_changed(self, event):
        # Notify rendering process that fragment shader must be reloaded
        self.reload_frag = True

    def get_location(self, tex_id):
        tex_info = tex_id.split(':', 1)
        tex_name = tex_info[0]
        tex_index = 0
        if len(tex_info) > 1:
            tex_index = int(tex_info[1]) % len(self.tex_locations[tex_name])
        return self.tex_locations[tex_name][tex_index]

    def to_float(self, val):
        if val == 'cld:time':
            return self.render_time
        return float(val)

    def parse_message(self, message):
        datatype = message[0]
        name = message[1]
        value = message[2:]
        np_dtype = None
        if datatype == 'i':
            np_dtype = 'i4'
            value = list(map(int, value))
        elif datatype == 't':
            np_dtype = 'i4'
            value = list(map(self.get_location, value))
        elif datatype == 'f':
            np_dtype = 'f4'
            value = list(map(self.to_float, value))
        return np_dtype, name, value

    def write_uniform(self, np_dtype, name, value, caching = True):
        try:
            # Retrieve uniform object using its name
            uniform = self.program.get(name, None)
            if uniform:
                # Send value as raw bytes
                uniform.write(np.array(value).astype(np_dtype).tobytes())
        except Exception as e:
            print(e)
            return

        # Uniform value was sent successfully
        # Store this value in the uniform cache
        if caching:
            self.uniform_cache[name] = {
                'np_dtype': np_dtype,
                'value': value
            }

    def render(self, time, frametime):
        # Prepare next frame
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)
        self.render_time = time

        # Reload fragment shader
        if self.reload_frag:
            self.reload_frag = False
            try:
                program = self.load_program(
                    vertex_shader=ClaudeApp.vertex_shader,
                    fragment_shader=ClaudeApp.fragment_shader
                )
                # Loading was successful
                # Reset OpenGL objects
                self.program = program
                self.vao = self.ctx.vertex_array(self.program, self.vbo, 'in_vert')
                # Send last known uniform values
                for name, content in self.uniform_cache.items():
                    self.write_uniform(content['np_dtype'], name, content['value'], False)
            except Exception as e:
                print(e)

        # Read messages fed from server and update uniforms accordingly
        while not self.queue.empty():
            try:
                message = self.queue.get_nowait()
                np_dtype, name, value = self.parse_message(message)
                self.write_uniform(np_dtype, name, value)
            except Exception as e:
                print(e)
                pass

        # Update time
        # No need to cache the time uniform value
        # as it must be sent between each frame
        self.write_uniform('f4', 'time', time, False)

        # Render frame
        self.vao.render()

    def resize(self, width, height):
        # Update resolution uniform with new dimensions
        self.write_uniform('f4', 'resolution', (width, height))

    def close(self):
        # Terminate server
        self.server.terminate()

        # Stop filewatcher
        self.observer.stop()
        self.observer.join()
