from matplotlib import pyplot as plt
import numpy as np


class MyScatter():
    def __init__(self, x, y, ax, size=1, m=None, **kwargs):
        import matplotlib.markers as mmarkers

        self.n = len(x)
        self.ax = ax
        self.ax.figure.canvas.draw()
        self.size_data = size
        self.size = size
        sc = ax.scatter(x, y, s=self.size, **kwargs)

        if (m is not None) and (len(m) == len(x)):
            paths = []
            for marker in m:
                if isinstance(marker, mmarkers.MarkerStyle):
                    marker_obj = marker
                else:
                    marker_obj = mmarkers.MarkerStyle(marker)
                path = marker_obj.get_path().transformed(
                    marker_obj.get_transform())
                paths.append(path)
            sc.set_paths(paths)

        self.sc = sc
        self._resize()
        self.cid = ax.figure.canvas.mpl_connect('draw_event', self._resize)

    def _resize(self, event=None):
        ppd = 72./self.ax.figure.dpi
        trans = self.ax.transData.transform
        s = ((trans((1, self.size_data))-trans((0, 0)))*ppd)[1]
        if s != self.size:
            self.sc.set_sizes(s**2*np.ones(self.n))
            self.size = s
            self._redraw_later()

    def _redraw_later(self):
        self.timer = self.ax.figure.canvas.new_timer(interval=10)
        self.timer.single_shot = True
        self.timer.add_callback(lambda: self.ax.figure.canvas.draw_idle())
        self.timer.start()
