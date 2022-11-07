import streamlit as st
from src.data import import_data, summarise_data
from datetime import datetime
from pathlib import Path
import base64

st.title("Crafted Pizza App")


@st.cache
def get_results(sales_data, expenses_data):
    sales_data = import_data.read_sales_data(sales_data)
    sales_data = import_data.extract_revenue(sales_data)
    sales_data = import_data.extract_sales_date(sales_data)
    sales_summary = summarise_data.summarise_performance(
        performance_data=sales_data, on_col="revenue"
    )

    expenses_data = import_data.read_expenses_data(expenses_data)
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


def create_download_link(file_path):
    """
    str -> bytes -> enc b64 bytes -> b64 str -> dec b64 str -> str
    my_string -> my_string.encode() -> b64encode(my_bytes) -> b64.decode()** -> b64decode(b64) -> my_bytes.decode()
    """
    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/12?page=3
    file_bytes = Path(file_path).read_bytes()
    b64_str = base64.b64encode(file_bytes).decode()
    html = f'<a href="data:application/octet-stream;base64,{b64_str}" download="sales_template.xlsx">Data template</a>'
    return html


html = create_download_link("./www/Nov2021.xlsx")

# SIDE BAR
with st.sidebar:
    st.markdown(html, unsafe_allow_html=True)

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

    sales_data = st.file_uploader(
        label="Sales Data", type="xlsx", accept_multiple_files=True
    )
    expenses_data = st.file_uploader(
        label="Expenses Data", type="csv", accept_multiple_files=True
    )


# MAIN BODY
with st.expander(label="Instructions"):
    st.write(
        """
        1. Save sales data for each month in the data template
        2. Save sales data for all months in a single folder
        3. Export expenses data for each branch
        4. Mark Kabete expenses with KB in the file name
        5. Save expenses data for all months in another folder
        6. Select your data
        7. Select a start and end period
        """
    )

if len(sales_data) == 0 or len(expenses_data) == 0:
    st.write("*Use the sidebar to upload sales and expenses data to start!*")

if len(sales_data) > 0 and len(expenses_data) > 0:
    try:
        results = get_results(sales_data, expenses_data)

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
