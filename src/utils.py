__author__ = 'Naheed'

def comparePIntervals(interv1, interv2):
    """
    Compares two intervals whether they are equal
    """
    # print sorted(phom_intervals)
    # print sorted(self.intervals)
    for dim, li in enumerate(interv2):
        for pair in li:
            if pair in interv1[0]:
                try:
                    interv1[0].remove(pair)
                except:
                    return False
        if len(interv1[0]) == 0:
            interv1.remove([])

    if len(interv1):
        return False

    return True