from sardine_core.handlers.sender import Number, NumericElement, ParsableElement, Sender, StringElement
from sardine_core.utils import alias_param

import socket
from typing import Optional, List


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
        value: Optional[StringElement | List[StringElement]],
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):
        if name is None or value is None:
            return

        if self.apply_conditional_mask_to_bars(pattern):
            return

        dims = ['x', 'y', 'z', 'w']

        if isinstance(value, list):
            if len(value) > 4:
                return
            for idx in range(len(value)):
                pattern[dims[idx]] = value[idx]
        else:
            pattern[dims[0]] = value

        reduced = self.pattern_reduce(pattern, iterator, divisor, rate)

        deadline = self.env.clock.shifted_time
        for item in reduced:
            message = name
            for dim in dims:
                if not dim in item:
                    break;
                message += f' {item[dim]}'
            self.call_timed(deadline, self._send, message)
