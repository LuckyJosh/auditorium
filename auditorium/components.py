# coding: utf8

from enum import IntEnum

class ShowMode(IntEnum):
    Markup = 1
    Code = 2


class Animation:
    def __init__(self, steps, time, loop):
        self.steps = steps
        self.time = time
        self.loop = loop
        self._current = 0

    @property
    def current(self):
        return self._current

    def next(self):
        self._current += 1

        if self._current >= self.steps:
            if self.loop:
                self._current = 0
            else:
                self._current = self.steps - 1

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class Column:
    def __init__(self, widths, show):
        self.widths = list(widths)
        self.show = show

    def __enter__(self):
        self.show.current_content.append(f'<div class="columns">')
        self.show.current_content.append(f'<div class="column" style="width: {self.widths[0] * 100}%;">')
        self.widths.pop(0)
        return self

    def tab(self):
        self.show.current_content.append(f'</div>')
        self.show.current_content.append(f'<div class="column" style="width: {self.widths[0] * 100}%;">')
        self.widths.pop(0)

    def __exit__(self, *args, **kwargs):
        self.show.current_content.append('</div>')
        self.show.current_content.append('</div>')
