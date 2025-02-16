"""Module decomposing.py"""
import logging

import dask
import pandas as pd
import statsmodels.tsa.seasonal as stl

import config
import src.decomposition.persist
import src.decomposition.structuring


class Decomposing:
    """
    Decomposing
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data: The index is a DatetimeIndex, which is necessary for the decomposition algorithm
        """

        self.__data = data

        # Instances
        self.__configurations = config.Config()
        self.__structuring = src.decomposition.structuring.Structuring()
        self.__persist = src.decomposition.persist.Persist()

    @dask.delayed
    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        data: pd.DataFrame = self.__data.copy().loc[self.__data['hospital_code'] == code, :]
        return data.sort_values(by='week_ending_date', ascending=True)

    @dask.delayed
    def __decompose(self, frame: pd.DataFrame) -> stl.DecomposeResult:
        """

        :param frame:
        :return:
        """

        parts = stl.seasonal_decompose(
            x=frame['n_attendances'], model='additive', period=self.__configurations.seasons)

        return parts

    @dask.delayed
    def __exc_structuring(self, parts: stl.DecomposeResult) -> pd.DataFrame:
        """

        :param parts:
        :return:
        """

        return self.__structuring.exc(parts=parts)

    @dask.delayed
    def __exc__persist(self, data: pd.DataFrame, health_board_code: str, hospital_code: str):
        """

        :param data:
        :param health_board_code:
        :param hospital_code:
        :return:
        """

        return self.__persist.exc(
            data=data, health_board_code=health_board_code, hospital_code=hospital_code)

    def exc(self):
        """

        :return:
        """

        # The distinct pairings of boards & institutions
        doublet = self.__data[['health_board_code', 'hospital_code']].drop_duplicates()

        # Compute
        computations = []
        for i in range(doublet.shape[0]):
            frame = self.__get_data(code=doublet.hospital_code.iloc[i])
            parts = self.__decompose(frame=frame)
            data = self.__exc_structuring(parts=parts)
            message = self.__exc__persist(
                data=data, health_board_code=doublet.health_board_code.iloc[i],
                hospital_code=doublet.hospital_code.iloc[i])
            computations.append(message)

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
