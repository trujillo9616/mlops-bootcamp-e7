def recency_scoring(rfm) -> int:
    if rfm.recency <= 24.0:
        recency_score = 4
    elif rfm.recency <= 57.0:
        recency_score = 3
    elif rfm.recency <= 149.0:
        recency_score = 2
    else:
        recency_score = 1

    return recency_score


def frequency_scoring(rfm) -> int:
    if rfm.frequency >= 10.0:
        frequency_score = 4
    elif rfm.frequency >= 5.0:
        frequency_score = 3
    elif rfm.frequency >= 2.0:
        frequency_score = 2
    else:
        frequency_score = 1

    return frequency_score


def monetary_scoring(rfm) -> int:
    if rfm.monetary >= 1571.0:
        monetary_score = 4
    elif rfm.monetary >= 645.0:
        monetary_score = 3
    elif rfm.monetary >= 298.0:
        monetary_score = 2
    else:
        monetary_score = 1

    return monetary_score


def rfm_scoring(rfm):
    return (
        str(int(rfm["recency_score"]))
        + str(int(rfm["frequency_score"]))
        + str(int(rfm["monetary_score"]))
    )


def categorizer(rfm):
    if (rfm[0] in ["2", "3", "4"]) & (rfm[1] in ["4"]) & (rfm[2] in ["4"]):
        rfm = "Champion"

    elif (rfm[0] in ["3"]) & (rfm[1] in ["1", "2", "3", "4"]) & (rfm[2] in ["3", "4"]):
        rfm = "Top Loyal Customer"

    elif (rfm[0] in ["3"]) & (rfm[1] in ["1", "2", "3", "4"]) & (rfm[2] in ["1", "2"]):
        rfm = "Loyal Customer"

    elif (rfm[0] in ["4"]) & (rfm[1] in ["1", "2", "3", "4"]) & (rfm[2] in ["3", "4"]):
        rfm = "Top Recent Customer"

    elif (rfm[0] in ["4"]) & (rfm[1] in ["1", "2", "3", "4"]) & (rfm[2] in ["1", "2"]):
        rfm = "Recent Customer"

    elif (
        (rfm[0] in ["2", "3"])
        & (rfm[1] in ["1", "2", "3", "4"])
        & (rfm[2] in ["3", "4"])
    ):
        rfm = "Top Customer Needed Attention"

    elif (
        (rfm[0] in ["2", "3"])
        & (rfm[1] in ["1", "2", "3", "4"])
        & (rfm[2] in ["1", "2"])
    ):
        rfm = "Customer Needed Attention"

    elif (rfm[0] in ["1"]) & (rfm[1] in ["1", "2", "3", "4"]) & (rfm[2] in ["3", "4"]):
        rfm = "Top Lost Customer"

    elif (rfm[0] in ["1"]) & (rfm[1] in ["1", "2", "3", "4"]) & (rfm[2] in ["1", "2"]):
        rfm = "Lost Customer"

    return rfm
