from sardine_core.handlers.sender import Number, NumericElement, ParsableElement, Sender
from sardine_core.utils import alias_param

import socket


class ClaudeHandler(Sender):

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
        if self._socket:
            self._socket.send(message.encode())

    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send(
        self,
        name: str,
        value: NumericElement,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):
        if name is None or value is None:
            return

        if self.apply_conditional_mask_to_bars(pattern):
            return

        pattern['value'] = value
        reduced = self.pattern_reduce(pattern, iterator, divisor, rate)

        deadline = self.env.clock.shifted_time
        for item in reduced:
            message = f"{name} {item['value']}"
            self.call_timed(deadline, self._send, message)
