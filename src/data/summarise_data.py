import pandas as pd
from datetime import datetime


def summarise_performance(
    performance_data: pd.DataFrame, on_col: str = "revenue"
):
    """Summarise sales by year/month and branch.

    Args:
    ---
    performance_data: either sales_data or expenses_data
    on_col: the column to summarise on either "revenue" or "expenses"
    """

    performance_data = performance_data.assign(
        year_month=lambda df: df.date.dt.strftime("%Y%m").astype(int),
    )

    summarised_data = performance_data.groupby(
        by=["year_month", "branch"]
    ).aggregate(amount=(f"{on_col}", "sum"))

    performance_summary = (
        summarised_data.pivot_table(
            index="year_month", columns="branch", values="amount"
        )
        .fillna(0)
        .assign(total=lambda df: df.KK + df.KB)
    )

    return performance_summary


def summarise_profit(
    sales_summary: pd.DataFrame,
    expenses_summary: pd.DataFrame,
    start_period: int = int(datetime.now().strftime("%Y" + "01")),
    end_period: int = int(datetime.now().strftime("%Y" + "12")),
) -> None:
    """Summarise profit by year/month and branch.

    Args:
    ---
    sales_summary: summary of sales per year_month and branch
    expenses_summary: summary of expenses per year_month and branch
    start_period: evaluation period YYYYMM format
    end_period: evaluation period YYYYMM format
    """

    profit_summary = pd.merge(
        left=sales_summary,
        right=expenses_summary,
        how="left",
        left_index=True,
        right_index=True,
        suffixes=("_sales", "_expenses"),
    )

    profit_summary = profit_summary.assign(
        KB_profit=lambda df: df.KB_sales - df.KB_expenses,
        KK_profit=lambda df: df.KK_sales - df.KK_expenses,
        total_profit=lambda df: df.total_sales - df.total_expenses,
    )

    print(profit_summary)

    print(f"\nprofit this period: {start_period} - {end_period}")

    total_profit_this_year = profit_summary[
        (profit_summary.index >= start_period)
        & (profit_summary.index <= end_period)
    ].total_profit.sum()

    KB_profit_this_year = profit_summary[
        (profit_summary.index >= start_period)
        & (profit_summary.index <= end_period)
    ].KB_profit.sum()

    KK_profit_this_year = profit_summary[
        (profit_summary.index >= start_period)
        & (profit_summary.index <= end_period)
    ].KK_profit.sum()

    print("\ntotal profit:", total_profit_this_year)
    print("kabete profit:", KB_profit_this_year)
    print("kikuyu profit:", KK_profit_this_year)
