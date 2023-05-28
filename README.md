# Claude

**Claude** is a tool for synchronizing visuals with audio in a live-coding context.

## Introduction

Claude is built around a standard *client-server* architecture, in which the server is in charge of rendering the visuals and the client sends messages to modify the visuals.

More specifically, the Claude server creates a window in which it renders a simple rectangle using OpenGL.
Hence, the content of the window can be customized using a *fragment shader* provided as input.

The Claude server - as its name indicates - also creates a server process that listens for any incoming messages.
These messages are used to modify the fragment shader's *uniforms*.
Claude clients connect to the server process and send messages to change uniform values.

> Note: for now only uniforms of type *float* are supported. This should change soon.

How does that make it an audio-visual synchronization tool?
Several audio live-coding environments work in the exact same way: by connecting to a server in charge of "making sounds" and regularly sending it messages using a *clock* system.
Therefore, by creating Claude clients in these audio live-coding environments, we can use the same clock to update our fragment shader's uniform, giving the impression that the visuals are synchronized with the audio.

Currently Claude is available in only one live-coding environment: **Sardine**.
It can be used as a regular *sender*, thus allowing to take advantage of the *Sardine Pattern Language* for writing uniform values to send.

## Install

See [INSTALL](INSTALL.md).

## First test with telnet

To test the installation of Claude, start by simply launching a Claude server:

```
cd Claude
python -m claude_server
```

Then, in another terminal, connect to the server using the *telnet* utility:

```
telnet 127.0.0.1 65432
```

You can now send messages to the server, try the following ones and see what happens in Claude's window:

```
freq 5
amp .1
amp .4
freq 1
...
```

By default the Claude server uses the [wave](resources/wave.frag) shader, which has two uniforms: `freq` (frequency) and `amp` (amplitude).
These two parameters allow you to tweak the sine wave you are visualizing on screen.

## Using Claude in Sardine

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
