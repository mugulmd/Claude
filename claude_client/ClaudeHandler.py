from sardine_core.handlers.sender import Number, NumericElement, ParsableElement, Sender, StringElement
from sardine_core.utils import alias_param

import socket
from typing import Optional, List


class ClaudeHandler(Sender):
    """Sardine client for sending messages to the Claude server.

    Attributes:
      params['ip']: The IP address to connect to the Claude server.
      params['port']: The port to connect to the Claude server.
    """

    def __init__(self, params: dict):
        super().__init__()

        try:
            # Setup connection to Claude server
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((params['ip'], params['port']))
        except Exception as e:
            print(f'Connection to Claude server failed: {e}')
            self._socket = None

    def _send(self, message: str):
        # Send message encoded as raw bytes to Claude server
        if self._socket:
            self._socket.send(message.encode())

    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    @alias_param(name="datatype", alias="dt")
    def send(
        self,
        name: str,
        value: Optional[StringElement | List[StringElement]],
        datatype: str = 'f',
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):
        # Names of the 1st to 4th components of the received vector
        dims = ['x', 'y', 'z', 'w']

        # Add each component of the received vector
        # to the pattern dict for parsing
        if isinstance(value, list):
            if len(value) > 4:
                return
            for idx in range(len(value)):
                pattern[dims[idx]] = value[idx]
        else:
            pattern[dims[0]] = value

        # Parse each dimension separately
        reduced = self.pattern_reduce(pattern, iterator, divisor, rate)

        deadline = self.env.clock.shifted_time
        for item in reduced:
            # Build message to send to the Claude server
            message = f'{datatype} {name}'
            for dim in dims:
                if not dim in item:
                    break;
                message += f' {item[dim]}'
            # Schedule sending the message
            self.call_timed(deadline, self._send, message)
