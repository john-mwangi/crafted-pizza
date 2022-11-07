import streamlit as st
from src.data import import_data, summarise_data
from datetime import datetime
import pathlib
import base64

st.title("Crafted Pizza App")


download_html = f'<a href="www/Nov2021.xlsx">Data template</a>'


with st.sidebar:
    st.write("### Instructions:")
    st.write(
        """
        1. Save sales data for each month in the data template
        2. Export expenses data for each branch and mark Kabete data with KB
        3. Save sales data for all months in a single folder
        4. Save expenses data for all months in another folder
        5. Enter the paths for the folders below
        6. Select a start and end period
        """
    )
    st.markdown(download_html, unsafe_allow_html=True)

    start_col, end_col = st.columns(2, gap="large")
    with start_col:
        start_period = st.date_input(
            label="Start Period",
            value=datetime(year=2020, month=1, day=1),
        )
        start_period = int(start_period.strftime("%Y%m"))

    with end_col:
        end_period = st.date_input(label="End Period", value=datetime.now())
        end_period = int(end_period.strftime("%Y%m"))

    sales_path = st.text_input(
        label="Sales path",
        help="Path to the folder containing sales data e.g. C:/data/sales/",
    )

    expenses_path = st.text_input(
        label="Expenses path",
        help="Path to the folder containing expenses data e.g. C:/data/expenses/",
    )


@st.cache
def get_results():
    sales_data = import_data.read_sales_data(sales_path)
    sales_data = import_data.extract_revenue(sales_data)
    sales_data = import_data.extract_sales_date(sales_data)
    sales_summary = summarise_data.summarise_performance(
        performance_data=sales_data, on_col="revenue"
    )

    expenses_data = import_data.read_expenses_data(expenses_path)
    expenses_summary = summarise_data.summarise_performance(
        performance_data=expenses_data, on_col="expenses"
    )

    results = summarise_data.summarise_profit(
        sales_summary=sales_summary,
        expenses_summary=expenses_summary,
        start_period=start_period,
        end_period=end_period,
    )

    return results


if sales_path == "" or expenses_path == "":
    st.write("*Enter the paths to the sales and expenses data to start!*")

if sales_path != "" and expenses_path != "":
    sales_path = pathlib.Path(sales_path).resolve()
    expenses_path = pathlib.Path(expenses_path).resolve()

    try:
        results = get_results()

        period_df = results.get("profit_summary")

        rev_col, KK_col, KB_col = st.columns(spec=3, gap="medium")
        with rev_col:
            st.metric(
                label="Total Profit",
                value=f"{results.get('total_profit'):,.0f}",
            )
        with KB_col:
            st.metric(
                label="Kabete Profit", value=f"{results.get('KB_profit'):,.0f}"
            )
        with KK_col:
            st.metric(
                label="Kikuyu Profit", value=f"{results.get('KK_profit'):,.0f}"
            )

        st.caption("*Hit refresh to update the results!*")
        st.dataframe(period_df)

        with st.sidebar:
            st.download_button(
                label="Download results",
                data=period_df.to_csv(index=True),
                mime="text/csv",
                file_name="profit_summary.csv",
            )

    except AttributeError:
        st.error(
            "*Please check the paths to the sales and expenses data and try again!*"
        )


def authorise_app():
    """Authorise this app using OAuth2"""
    # ref: https://www.youtube.com/watch?v=vQQEaSnQ_bs
    raise NotImplementedError


def download_data(real_file_id):
    """Downloads a Google Drive folder

    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # ref: https://developers.google.com/drive/api/v3/manage-downloads
    raise NotImplementedError
