"""This module imports data."""

import sys
from glob import glob
import pandas as pd
import os

sys.path.append("../../")
from configs import config


def read_sales_data(sales_dir: str = config.SALES_DIR) -> pd.DataFrame:
    """Read sales data stored in Excel files. All Excel sheets have either
    Sheet1 or KK/KB.
    """
    sales_paths = glob(pathname=os.path.join(sales_dir, "*.xls*"))

    sales_data = pd.DataFrame()

    for path in sales_paths:
        try:
            kk_sales = pd.read_excel(
                path, sheet_name="Sheet1", names=["data"], header=None
            )
            kk_sales["branch"] = "KK"
            kk_sales["filename"] = path.split("/")[-1]
            sales_data = pd.concat(objs=[sales_data, kk_sales], axis=0)
        except:
            kk_sales = pd.read_excel(
                path, sheet_name="KK", names=["data"], header=None
            )
            kk_sales["branch"] = "KK"
            kk_sales["filename"] = path.split("/")[-1]
            sales_data = pd.concat(objs=[sales_data, kk_sales], axis=0)

            kb_sales = pd.read_excel(
                path, sheet_name="KB", names=["data"], header=None
            )
            kb_sales["branch"] = "KB"
            kb_sales["filename"] = path.split("/")[-1]
            sales_data = pd.concat(objs=[sales_data, kb_sales], axis=0)

    return sales_data


def extract_revenue(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Extracts revenue from the raw sales data."""
    sales_data = sales_data.assign(
        revenue_=lambda df: df.data.str.extract(r".*-(\d+/?\d+).*"),
    )

    revenues = (
        sales_data.revenue_.str.split("/", expand=True).fillna(0).astype(float)
    )

    revenues = revenues.assign(revenue=lambda df: df[0] + df[1])
    sales_data = sales_data.assign(revenue=revenues.revenue).drop(
        columns="revenue_"
    )

    return sales_data


def extract_sales_date(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Extract the day a sale was made."""
    sales_data = sales_data.assign(
        month=lambda df: df.filename.str.extract(r"(.*).xlsx"),
        day=lambda df: df.data.str.extract(r"^(\d{1,2})[a-z]{1,2}$").fillna(
            method="ffill"
        ),
        date=lambda df: pd.to_datetime(
            df.day + "/" + df.month, format="%d/%b%Y"
        ),
    )

    return sales_data


def read_expenses_data(
    expenses_dir: str = config.EXPENSES_DIR,
) -> pd.DataFrame:
    """Read expenses data in the Expenses directory stored as csv files."""
    expenses_files = glob(pathname=os.path.join(expenses_dir, "*.csv"))

    kabete_files = [file for file in expenses_files if "KB" in file]
    kikuyu_files = [file for file in expenses_files if "KB" not in file]

    assert len(expenses_files) == len(kabete_files) + len(kikuyu_files)

    expenses_data = pd.DataFrame()

    for path in expenses_files:
        if path in kabete_files:
            temp_expenses = pd.read_csv(path).assign(branch="KB")
            expenses_data = pd.concat(
                objs=[expenses_data, temp_expenses], axis=0
            )
        else:
            temp_expenses = pd.read_csv(path).assign(branch="KK")
            expenses_data = pd.concat(
                objs=[expenses_data, temp_expenses], axis=0
            )

    expenses_data = expenses_data.assign(
        date=lambda df: pd.to_datetime(df.Date, format="%d/%m/%Y"),
    ).drop(columns="Date")

    expenses_data.columns = [
        col.strip().lower() for col in expenses_data.columns
    ]

    expenses_data = expenses_data.assign(
        expenses=lambda df: abs(df.amount)
    ).drop(columns="amount")

    return expenses_data
