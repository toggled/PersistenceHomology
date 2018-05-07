__author__ = 'Naheed'
import numpy as np
import pylab as pl


class PersistenceViz:
    """
    Class to visualize persistence intervals in different manner e.g. barcode, diagram.
    """

    def __init__(self, intervals, replace_Inf):
        """
        :param intervals: hashtable keyed by dimension , valued by list of pairs.
        """
        self.intervals = intervals
        self.INF = replace_Inf
        # print self.intervals
        # print type(self.intervals)
        # assert isinstance(self.intervals,dict)

    def draw_barcodes(self, write=False, writefilename=None):
        """
        Draw persistence barcodes corresponding to the intervals.
        """
        import numpy as np
        import pylab as pl
        from matplotlib import collections  as mc
        import seaborn as sns

        dims = len(self.intervals)
        assert dims < 6
        cols = sns.color_palette()[:dims]

        for dim in range(dims):
            interval_list = sorted(self.intervals[dim], key=lambda (x, y): (x, y - x))
            intervs = []
            for intv in interval_list:
                if intv[1] == np.inf:
                    intervs.append((intv[0], self.INF))
                else:
                    intervs.append((intv[0], intv[1]))
            intervals = [x for x in intervs if x[1] > x[0]]

            number_of_bars = len(intervals)
            y1_s = range(1, number_of_bars + 1)
            y2_s = y1_s[:]
            x1_s, x2_s = zip(*intervals)

            # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines = zip(start_coord, end_coord)

            lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
            fig, ax = pl.subplots()
            ax.add_collection(lc)
            ax.autoscale()
            ax.margins(0.1)
            pl.show()

    def qual_compare_barcodes(self, secondbarcode, write=False):
        import numpy as np
        import pylab as pl
        from matplotlib import collections  as mc
        import seaborn as sns

        assert isinstance(secondbarcode, list)

        dims = len(self.intervals)
        assert dims < 6
        cols = sns.color_palette()[:dims]

        paint_colors = []
        lines = []
        for dim in range(dims):
            interval_list = sorted(self.intervals[dim], key=lambda (x, y): (x, y - x))
            intervs = []
            for intv in interval_list:
                if intv[1] == np.inf:
                    intervs.append((intv[0], self.INF))
                else:
                    intervs.append((intv[0], intv[1]))
            intervals = [x for x in intervs if x[1] > x[0]]

            number_of_bars = len(intervals)
            y1_s = range(1, number_of_bars + 1)
            y2_s = y1_s[:]
            x1_s, x2_s = zip(*intervals)

            # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines.extend(zip(start_coord, end_coord))
            paint_colors.extend([cols[dim]] * number_of_bars)

        lc = mc.LineCollection(lines, colors=paint_colors, linewidths=0.5)
        fig, ax = pl.subplots()
        ax.add_collection(lc)
        ax.autoscale()
        ax.margins(0.1)
        pl.show()
