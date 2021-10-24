import fdrtd


def create(microprotocol):

    if microprotocol == 'BasicMinMax':
        from fdrtd.builtins.simon.microprotocols.microprotocol_basic_min_max import MicroprotocolBasicMinMax
        return MicroprotocolBasicMinMax

    if microprotocol == 'BasicSum':
        from fdrtd.builtins.simon.microprotocols.microprotocol_basic_sum import MicroprotocolBasicSum
        return MicroprotocolBasicSum

    if microprotocol == 'SetIntersection':
        from fdrtd.builtins.simon.microprotocols.microprotocol_set_intersection import MicroprotocolSetIntersection
        return MicroprotocolSetIntersection

    if microprotocol == 'SetIntersectionSize':
        from fdrtd.builtins.simon.microprotocols.microprotocol_set_intersection_size import MicroprotocolSetIntersectionSize
        return MicroprotocolSetIntersectionSize

    if microprotocol == 'StatisticsBivariate':
        from fdrtd.builtins.simon.microprotocols.microprotocol_statistics_bivariate import MicroprotocolStatisticsBivariate
        return MicroprotocolStatisticsBivariate

    if microprotocol == 'StatisticsFrequency':
        from fdrtd.builtins.simon.microprotocols.microprotocol_statistics_frequency import MicroprotocolStatisticsFrequency
        return MicroprotocolStatisticsFrequency

    if microprotocol == 'StatisticsUnivariate':
        from fdrtd.builtins.simon.microprotocols.microprotocol_statistics_univariate import MicroprotocolStatisticsUnivariate
        return MicroprotocolStatisticsUnivariate

    raise fdrtd.server.exceptions.NotAvailable(microprotocol)
