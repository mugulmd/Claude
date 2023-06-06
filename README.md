# Claude

**Claude** is a tool for synchronizing visuals with audio in a live-coding context.

## Introduction

Claude is built around a standard *client-server* architecture, in which the server is in charge of rendering the visuals and the client sends messages to modify the visuals.

More specifically, the Claude server creates a window in which it renders a simple rectangle using OpenGL.
Hence, the content of the window can be customized using a *fragment shader* provided as input.

You can modify the fragment shader while Claude is running:
whenever you save this file, the changes will apply in the window.

The Claude server - as its name indicates - also creates a server process that listens for any incoming messages.
These messages are used to modify the fragment shader's *uniforms*.
Claude clients connect to the server process and send messages to change uniform values.

How does that make it an audio-visual synchronization tool?
Several audio live-coding environments work in the exact same way: by connecting to a server in charge of "making sounds" and regularly sending it messages using a *clock* system.
Therefore, by creating Claude clients in these audio live-coding environments, we can use the same clock to update our fragment shader's uniform, giving the impression that the visuals are synchronized with the audio.

Currently Claude is available in only one live-coding environment: [Sardine](https://github.com/Bubobubobubobubo/sardine).
It can be used as a regular *sender*, thus allowing to take advantage of the *Sardine Pattern Language* for writing uniform values to send.

## Install

See [INSTALL](INSTALL.md).

## Usage

### First test with telnet

To test the installation of Claude, start by simply launching a Claude server:
```
cd Claude
python -m claude_server
```
A window should open, displaying an animated wave.

Then, in another terminal, connect to the server using the *telnet* utility:
```
telnet 127.0.0.1 65432
```

You can now send messages to the server, try the following ones and see what happens in Claude's window:
```
f freq 5
f amp .1
f water 1 0 0
i nb_waves 3
```

By default the Claude server uses the [wave](resources/wave.frag) shader, which has a few uniforms for controlling the output.
These parameters allow you to tweak the wave(s) you are visualizing on screen.

### Using Claude in Sardine

Once the Claude extension is installed in Sardine, a Claude client will be initialized when you start a new session.

You can then use the `Claude(...)` alias to send messages to the Claude server:
```python
@swim
def wave(p=2, i=0):
    Claude('freq', 'rand*10', i=i)
    Claude('amp', '[1:5]/10', i=i)
    again(wave, p=2, i=i+1)
```

This alias takes two positional arguments, the uniform name and value, followed by the usual Sardine send parameters (iterator, divisor, rate).
Note that you can use patterns for the value argument, thus giving great flexibility during live-coding sessions.

In the previous example, the uniforms sent were simply floats, but we can also send vectors (up to 4 dimensions):
```python
@swim
def wave(p=2, i=0):
    Claude('water', ['.2 1 .5', 0, '1 .2'], i=i)
    again(wave, p=2, i=i+1)
```

Moreover, another optional argument lets us specify the *datatype* that we want to use.
This argument is called `datatype` but it can be replaced by its alias `dt`:
```python
@swim
def wave(p=2, i=0):
    Claude('nb_waves', '1 2 3 4 3 2', dt='i', i=i)
    again(wave, p=2, i=i+1)
```

> Note: for now only the float and integer datatypes are supported ('f' and 'i').
> The default datatype is float, hence it is not necessary to specify it.

### Shader live-coding

The `claude_server` application has a few configuration options that can be detailed with:
```
python -m claude_server -h
```

The two most important options are `--res` and `--frag`, which allow you to pass in and use your own fragment shader.

Claude is designed for live-coding: you can edit your fragment shader while Claude is running, and every time you save it Claude will update its content.

Feel free to use the [template shader](resources/template.frag) and [utilities](resources/utils/glsl) provided.

## Contributions

Claude is at an early development stage, and we're actively seeking contributors to help enhance the project.

Contributions can take many forms:
- general feedback
- bug reports
- features requests
- code improvements
- documentation
- tool design ideas
- demos and tutorials.

There is no official communication channel yet, so please use GitHub issues.
