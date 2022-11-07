from src.data import import_data, summarise_data
from configs import config
from glob import glob
import os


def main():

    sales_paths = glob(pathname=os.path.join(config.SALES_DIR, "*.xls*"))
    expenses_paths = glob(pathname=os.path.join(config.EXPENSES_DIR, "*.csv"))

    sales_data = import_data.read_sales_data(sales_paths)
    sales_data = import_data.extract_revenue(sales_data)
    sales_data = import_data.extract_sales_date(sales_data)
    sales_summary = summarise_data.summarise_performance(
        performance_data=sales_data, on_col="revenue"
    )

    expenses_data = import_data.read_expenses_data(expenses_paths)
    expenses_summary = summarise_data.summarise_performance(
        performance_data=expenses_data, on_col="expenses"
    )

    summarise_data.summarise_profit(
        sales_summary=sales_summary,
        expenses_summary=expenses_summary,
        start_period=202001,
        end_period=202012,
    )

    exit()


if __name__ == "__main__":
    main()
