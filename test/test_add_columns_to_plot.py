import pandas as pd
import pytest

from pydykit import utils
from pydykit.postprocessors import Postprocessor


def test_add_columns_to_plot():
    # Sample data
    columns_to_plot = ["existing_column"]
    results_df = pd.DataFrame(
        {"quantity_1": [1, 2, 3], "quantity_2": [4, 5, 6], "other_column": [7, 8, 9]}
    )
    quantity = "quantity"

    # Expected result
    expected_columns = ["existing_column", "quantity_1", "quantity_2"]

    # Call the method
    updated_columns = utils.add_columns_to_plot(columns_to_plot, results_df, quantity)

    # Assert the result
    assert updated_columns == expected_columns


if __name__ == "__main__":
    pytest.main()
