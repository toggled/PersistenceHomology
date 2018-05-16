import numpy as np
import pylab as pl
from matplotlib import collections  as mc
import seaborn as sns
import csv


class PersistenceViz:
    """
    Class to visualize persistence intervals in different manner e.g. barcode, diagram.
    """

    def __init__(self, intervals, replace_Inf):
        """
        :param intervals: list with dimension as index, list of pairs as values.
        :param replace_Inf: real number to replace occurances of "Inf"
        """
        self.intervals = intervals
        assert isinstance(self.intervals, list)
        self.INF = replace_Inf

    def draw_barcodes(self, write= False, writefilename= None):
        """
        Draw persistence barcodes corresponding to the intervals (list) in this class.
        """
        dims = len(self.intervals)
        assert dims < 6
        cols = sns.color_palette()[:dims]

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
            total += (number_of_bars)

            ax.autoscale()
            ax.margins(0.1)
        pl.show()

    def qual_compare_barcodes(self, secondbarcode, secondbar_replaceInf, write=False, writefilename = None, param = {}):
        """
        method to visualize this barcode with another one up to scale.
        :argument secondbarcode: Persistence intervals to compare with.
        :argument secondbar_replaceInf: value to replace  Inf in the second barcode
        :argument write: whether to write the comparative barcodes as pdf file or not.
        :argument writefilename: filename of the pdf containing the barcode figure
        :argument param: hashtable of parameters- e.g. title , x-axis labels (left fig., right fig.) of the figure
        """
        import numpy as np
        import pylab as pl
        from matplotlib import collections  as mc
        import seaborn as sns

        assert isinstance(secondbarcode, list)

        if param == {}:
            param = {"title": "Barcode Comparison", "xlabels": ("Left Barcode", "Right barcode")}

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
                    norm_fact = max(norm_fact, len(secondbarcode[i]))

            divide_by[i] = norm_fact

        # Process first bar
        cols = sns.color_palette()[:dims]

        # Iniitialize the subplots
        fig, (ax0, ax1) = pl.subplots(nrows=1, ncols=2, sharey=True)
        total = 0
        for dim in range(dims):
            interval_list = sorted(self.intervals[dim], key=lambda (x, y): (x, y - x))
            intervs = []
            for intv in interval_list:
                if intv[1] == float("inf"):
                    intervs.append((intv[0], self.INF))
                else:
                    intervs.append((intv[0], intv[1]))
            intervals = [x for x in intervs if x[1] > x[0]]

            number_of_bars = len(intervals)
            if number_of_bars < 1:
                if divide_by[dim]>0:
                    total += max(number_of_bars, divide_by[dim])
                continue

            y1_s = range(total + 1, total + number_of_bars + 1)
            y2_s = y1_s[:]
            x1_s, x2_s = zip(*intervals)

            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines = zip(start_coord, end_coord)

            lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
            ax0.add_collection(lc)
            total += max(number_of_bars, divide_by[dim])

        ax0.autoscale()
        ax0.get_yaxis().set_visible(False)
        ax0.set_xlabel(param["xlabels"][0])
            # ax0.margins(0.1)

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
                    total += max(number_of_bars, divide_by[dim])
                continue

            y1_s = range(total + 1, total + number_of_bars + 1)
            y2_s = y1_s[:]
            x1_s, x2_s = zip(*intervals)

            start_coord = zip(x1_s, y1_s)
            end_coord = zip(x2_s, y2_s)
            lines = zip(start_coord, end_coord)

            lc = mc.LineCollection(lines, colors=[cols[dim]] * number_of_bars, linewidths=1)
            ax1.add_collection(lc)
            total += max(number_of_bars, divide_by[dim])

        ax1.autoscale()
        ax1.get_yaxis().set_visible(False)
        ax1.set_xlabel(param["xlabels"][1])

        # Set plot title
        pl.suptitle(param["title"])
        # pl.show()

        # Save the figure
        if write and writefilename is not None:
            pl.savefig(writefilename, format="pdf")

    def qual_compare_barcodes_fromPersViz(self, secondbarViz, write=False, writefilename = None, param = {}):
        """
        method to visualize this barcode with another one up to scale.
        :argument secondbarViz: PersistenceViz object representation of another intervals.
        :argument write: whether to write the comparative barcodes as pdf file or not.
        :argument writefilename: filename of the pdf containing the barcode figure
        :argument param: hashtable of parameters- e.g. title , x-axis labels (left fig., right fig.) of the figure
        """
        assert isinstance(secondbarViz, PersistenceViz)

        secondbarcode = secondbarViz.intervals
        secondbar_replaceinf = secondbarViz.INF

        self.qual_compare_barcodes(secondbarcode,secondbar_replaceinf, write, writefilename, param)


    @classmethod
    def input_int_fromCSVs(cls, csvfilepaths, delimeter =",",replace_inf = float("inf")):
        """
        :argument list of filepaths of a csv file which has 2 columns (birth,death), delimeter for the columns, value which replaces infinity
        :return PersistenceViz object
        """
        j = 0
        INF = replace_inf

        intervals = [[] for s in csvfilepaths]
        for filepath in csvfilepaths:
            reader = None
            try:
                with open(filepath, 'r') as f:
                    reader = csv.reader(f, delimiter=delimeter)

                    for row in reader:
                        birth = float(row[0])
                        death = float(row[1])

                        if death == float("inf"):
                            death = INF

                        intervals[j].append((birth, death))

            except IOError:
                raise Exception("File does not exists")
                return cls(None,None)

            j += 1
        return cls(intervals, INF)

    @classmethod
    def input_int_threecolumned_fromCSVs(cls, csvfilepaths, delimeter=",", replace_inf = float("inf")):
        """
        :argument list of filepaths of a csv file which has 3 columns (dim,birth,death)
                 delimeter for the columns,
                 value which replaces infinity
        :return PersistenceViz object
        """
        j = 0
        INF = replace_inf

        intervals = [[] for s in csvfilepaths]
        for filepath in csvfilepaths:
            reader = None
            try:
                with open(filepath, 'r') as f:
                    reader = csv.reader(f, delimiter=delimeter)

                    for row in reader:
                        birth = float(row[1])
                        death = float(row[2])

                        if death == float("inf"):
                            death = INF

                        intervals[j].append((birth, death))

            except IOError:
                raise Exception("File does not exists")
                return cls(None, None)

            j += 1
        return cls(intervals, INF)