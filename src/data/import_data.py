"""This module imports data."""

import pandas as pd


def read_sales_data(sales_data: list) -> pd.DataFrame:
    """Read sales data stored in Excel files. All Excel sheets have either
    Sheet1 or KK/KB.

    Args:
    ---
    sales_data: a list of file paths
    """
    sales_df = pd.DataFrame()
    for path in sales_data:
        try:
            kk_sales = pd.read_excel(
                path, sheet_name="Sheet1", names=["data"], header=None
            )
            kk_sales["branch"] = "KK"

            if isinstance(path, str):
                kk_sales["filename"] = path.split("/")[-1]
            else:
                kk_sales["filename"] = path.name

            sales_df = pd.concat(objs=[sales_df, kk_sales], axis=0)
        except:
            kk_sales = pd.read_excel(path, sheet_name="KK", names=["data"], header=None)
            kk_sales["branch"] = "KK"

            if isinstance(path, str):
                kk_sales["filename"] = path.split("/")[-1]
            else:
                kk_sales["filename"] = path.name

            sales_df = pd.concat(objs=[sales_df, kk_sales], axis=0)

            kb_sales = pd.read_excel(path, sheet_name="KB", names=["data"], header=None)
            kb_sales["branch"] = "KB"

            if isinstance(path, str):
                kb_sales["filename"] = path.split("/")[-1]
            else:
                kb_sales["filename"] = path.name

            sales_df = pd.concat(objs=[sales_df, kb_sales], axis=0)

    return sales_df


def extract_revenue(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Extracts revenue from the raw sales data."""
    sales_data = sales_data.assign(
        revenue_=lambda df: df.data.str.extract(r".*-(\d+/?\d+).*"),
    )

    revenues = sales_data.revenue_.str.split("/", expand=True).fillna(0).astype(float)

    revenues = revenues.assign(revenue=lambda df: df[0] + df[1])
    sales_data = sales_data.assign(revenue=revenues.revenue).drop(columns="revenue_")

    return sales_data


def extract_sales_date(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Extract the day a sale was made."""
    sales_data = sales_data.assign(
        month=lambda df: df.filename.str.extract(r"(.*).xlsx"),
        day=lambda df: df.data.str.extract(r"^(\d{1,2})[a-z]{1,2}$").fillna(
            method="ffill"
        ),
        date=lambda df: pd.to_datetime(df.day + "/" + df.month, format="%d/%b%Y"),
    )

    return sales_data


def read_expenses_data(expenses_data: list) -> pd.DataFrame:
    """Read expenses data in the Expenses directory stored as csv files.

    Args:
    ---
    expenses_data: a list of file paths
    """

    # check if expenses_data is a list of strings
    all_strings = all([isinstance(path, str) for path in expenses_data])

    if all_strings:
        kabete_files = [file for file in expenses_data if "KB" in file]
        kikuyu_files = [file for file in expenses_data if "KB" not in file]
    else:
        kabete_files = [file for file in expenses_data if "KB" in file.name]
        kikuyu_files = [file for file in expenses_data if "KB" not in file.name]

    assert len(expenses_data) == len(kabete_files) + len(kikuyu_files)

    expenses_df = pd.DataFrame()

    for path in expenses_data:
        if path in kabete_files:
            temp_expenses = pd.read_csv(path).assign(branch="KB")
            expenses_df = pd.concat(objs=[expenses_df, temp_expenses], axis=0)
        else:
            temp_expenses = pd.read_csv(path).assign(branch="KK")
            expenses_df = pd.concat(objs=[expenses_df, temp_expenses], axis=0)

    expenses_df = expenses_df.assign(
        date=lambda df: pd.to_datetime(df.Date, format="%d/%m/%Y"),
    ).drop(columns="Date")

    expenses_df.columns = [col.strip().lower() for col in expenses_df.columns]

    expenses_df = expenses_df.assign(expenses=lambda df: abs(df.amount)).drop(
        columns="amount"
    )

    return expenses_df
