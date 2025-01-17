# SPDX-FileCopyrightText: 2021 2017-2021 Contributors to the OpenSTF project <korte.termijn.prognoses@alliander.com>
#
# SPDX-License-Identifier: MPL-2.0

import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from openstef_dbc.services.weather import Weather


@patch("openstef_dbc.data_interface._DataInterface.get_instance")
class TestRadiationShift(unittest.TestCase):
    def test(self, data_interface_get_instance_mock):
        # Mock database response
        start = pd.to_datetime("2077-01-01T02:00")
        end = pd.to_datetime("2077-01-01T04:00")

        index = pd.date_range(start, end, freq="15T")
        values = np.arange(index.size)

        df_test = pd.DataFrame(
            {
                "temp": values,
                "radiation": values,
            },
            index=index,
        )

        data_interface_get_instance_mock.return_value.exec_influx_query.return_value = {
            "weather": df_test
        }

        # Mock other functions
        weather = Weather()
        weather._get_nearest_weather_location = lambda x: x
        weather._combine_weather_sources = lambda x: x

        # Run function
        start += pd.Timedelta(hours=1)
        df_check = weather.get_weather_data(None, ["temp", "radiation"], start, end)

        # Check for correct results
        self.assertEqual(df_check.index[0], start)
        self.assertEqual(df_check.index[-1], end)
        np.testing.assert_array_equal(df_check["temp"], values[4:])
        np.testing.assert_array_equal(df_check["radiation"], values[4:] - 2)


if __name__ == "__main__":
    unittest.main()
