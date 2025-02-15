"""
Module config.py
"""
import os


class Config:
    """
    Description
    -----------

    A class for configurations
    """

    def __init__(self) -> None:
        """
        Notes<br>
        -------<br>

        <a href="https://otexts.com/fpp2/stationarity.html">Stationarity</a><br>
        Upcoming: Drift
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.decompositions_ = os.path.join(self.warehouse, 'series', 'decompositions')

        # Seed
        self.seed = 5

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'

        '''
        For architecture JSON
        '''

        # Fields
        self.fields = ['week_ending_date', 'health_board_code', 'hospital_code',  'n_attendances']

        # Seasons, trends, etc.
        self.seasons = 52
        self.trends = 1
