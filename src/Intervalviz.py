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
        assert isinstance(self.intervals, list)

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

        prev_length = 0
        fig, ax = pl.subplots()
        total = 0
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
            y1_s = range(total + 1, total + number_of_bars + 1)
            y2_s = y1_s[:]
            x1_s, x2_s = zip(*intervals)

            # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines = zip(start_coord, end_coord)

            lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
            ax.add_collection(lc)
            total += number_of_bars - 1

            ax.autoscale()
            ax.margins(0.1)
        pl.show()

    def qual_compare_barcodes(self, secondbarcode, secondbar_replaceInf, write=False):

        import numpy as np
        import pylab as pl
        from matplotlib import collections  as mc
        import seaborn as sns

        assert isinstance(secondbarcode, list)

        dims = len(self.intervals)
        assert dims < 6  # 6 is the maximum number of distinct colors
        assert len(secondbarcode) < 6

        # y-axis Normalization factor
        divide_by = {} # if divide_by[i] = -1 no bar for that dimension, else divide_by[i] is the maximum number of
                        # bars in ith dimension in both barcodes.
        for i in range(max(len(self.intervals), len(secondbarcode))):
            norm_fact = -1
            if i < len(self.intervals):
                if self.intervals[i]:
                    norm_fact = len(self.intervals[i])
            if i < len(secondbarcode):
                if secondbarcode[i]:
                    norm_fact = max(norm_fact,len(secondbarcode[i]))

            divide_by[i] = norm_fact

        # Process first bar
        cols = sns.color_palette()[:dims]

        fig, (ax0, ax1) = pl.subplots(nrows=1, ncols=2, sharey=True)
        total = 0
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
            if number_of_bars < 1:
                if divide_by[dim]>0:
                    total += max(number_of_bars, divide_by[dim]) - 1
                continue

            y1_s = range(total + 1, total + number_of_bars + 1)
            y2_s = y1_s[:]
            x1_s, x2_s = zip(*intervals)

            # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines = zip(start_coord, end_coord)

            lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
            ax0.add_collection(lc)
            total += max(number_of_bars, divide_by[dim]) - 1

        ax0.autoscale()
        ax0.get_yaxis().set_visible(False)
            # ax0.margins(0.1)

        # Process second barcodes

        # Process first bar


        cols = sns.color_palette()[:dims]

        total = 0
        for dim in range(dims):
            interval_list = sorted(secondbarcode[dim], key=lambda (x, y): (x, y - x))
            intervs = []
            for intv in interval_list:
                if intv[1] == np.inf:
                    intervs.append((intv[0], secondbar_replaceInf))
                else:
                    intervs.append((intv[0], intv[1]))
            intervals = [x for x in intervs if x[1] > x[0]]

            number_of_bars = len(intervals)
            if number_of_bars < 1:
                if divide_by[dim]>0:
                    total += max(number_of_bars, divide_by[dim]) - 1
                continue

            y1_s = range(total + 1, total + number_of_bars + 1)
            y2_s = y1_s[:]
            # print len(intervals), "--"
            x1_s, x2_s = zip(*intervals)

            # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines = zip(start_coord, end_coord)

            lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
            ax1.add_collection(lc)
            total += max(number_of_bars, divide_by[dim]) - 1

        ax1.autoscale()
        ax1.get_yaxis().set_visible(False)
            # ax1.margins(0.1)

        pl.show()

# def draw_barcodes(intervals_numpyarray, replace_Inf):
#     """
#     Draw persistence barcodes corresponding to the intervals
#     """
#     import numpy as np
#     import pylab as pl
#     from matplotlib import collections  as mc
#     import seaborn as sns
#
#     dims = len(intervals_numpyarray)
#     assert dims < 6
#     cols = sns.color_palette()[:dims]
#
#     prev_length = 0
#     fig, ax = pl.subplots()
#     total = 0
#     for dim in range(dims):
#         interval_list = sorted(intervals_numpyarray[dim], key=lambda (x, y): (x, y - x))
#         intervs = []
#         for intv in interval_list:
#             if intv[1] == np.inf:
#                 intervs.append((intv[0], replace_Inf))
#             else:
#                 intervs.append((intv[0], intv[1]))
#         intervals = [x for x in intervs if x[1] > x[0]]
#
#         number_of_bars = len(intervals)
#         y1_s = range(total + 1, total + number_of_bars + 1)
#         y2_s = y1_s[:]
#         x1_s, x2_s = zip(*intervals)
#
#         # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
#         start_coord = zip(x1_s, y1_s)
#         end_coord = zip(x2_s, y2_s)
#         lines = zip(start_coord, end_coord)
#
#         lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
#         ax.add_collection(lc)
#         total += number_of_bars - 1
#
#         ax.autoscale()
#         ax.margins(0.1)
#     pl.show()
