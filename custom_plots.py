from matplotlib import pyplot as plt
import numpy as np
import matplotlib.markers as mmarkers


class MyScatter():
    def __init__(self, x, y, ax, size=1, markers=None, colors=None, **kwargs):

        self.n = len(x)
        self.ax = ax
        self.ax.figure.canvas.draw()
        self.size_data = size
        self.size = size

        self.x = x
        self.y = y
        self.update(markers, colors, **kwargs)

    def update(self, markers, colors, **kwargs):
        sc = self.ax.scatter(self.x, self.y, s=self.size,
                             color=colors, **kwargs)

        if (markers is not None) and (len(markers) == len(self.x)):
            paths = []
            for m in markers:
                if isinstance(m, mmarkers.MarkerStyle):
                    marker_obj = m
                else:
                    marker_obj = mmarkers.MarkerStyle(m)
                path = marker_obj.get_path().transformed(
                    marker_obj.get_transform())
                paths.append(path)
            sc.set_paths(paths)

        self.sc = sc
        self._resize()
        self.cid = self.ax.figure.canvas.mpl_connect(
            'draw_event', self._resize)

    def _resize(self, event=None):
        ppd = 72./self.ax.figure.dpi
        trans = self.ax.transData.transform
        s = ((trans((1, self.size_data))-trans((0, 0)))*ppd)[1]
        if s != self.size:
            self.sc.set_sizes(s**2*np.ones(self.n))
            self.size = s
            # self._redraw_later()

    def _redraw_later(self):
        self.timer = self.ax.figure.canvas.new_timer(interval=10)
        self.timer.single_shot = True
        self.timer.add_callback(lambda: self.ax.figure.canvas.draw_idle())
        self.timer.start()