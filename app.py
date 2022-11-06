import streamlit as st
from src.data import import_data, summarise_data
from datetime import datetime
import io
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# download latest data (zip)
# unzip folder
# download data template
# fill data template with latest data
# put data template in data folder
# point app to data folder
# refresh app

CLIENT_ID = ""
CLIENT_SECRET = ""

st.title("Crafted Pizza App")

sales_data = import_data.read_sales_data()
sales_data = import_data.extract_revenue(sales_data)
sales_data = import_data.extract_sales_date(sales_data)
sales_summary = summarise_data.summarise_performance(
    performance_data=sales_data, on_col="revenue"
)

expenses_data = import_data.read_expenses_data()
expenses_summary = summarise_data.summarise_performance(
    performance_data=expenses_data, on_col="expenses"
)

start_period = st.date_input(
    label="Start Period",
    value=datetime(year=2020, month=1, day=1),
)
start_period = int(start_period.strftime("%Y%m"))

end_period = st.date_input(label="End Period", value=datetime.now())
end_period = int(end_period.strftime("%Y%m"))

results = summarise_data.summarise_profit(
    sales_summary=sales_summary,
    expenses_summary=expenses_summary,
    start_period=start_period,
    end_period=end_period,
)

period_df = results.get("profit_summary")

st.write(f"**Period: {start_period} - {end_period}**")
st.write(f"**Total profit: {results.get('total_profit'):,.0f}**")

st.write(f"Kabete profit: {results.get('KB_profit'):,.0f}")
st.write(f"Kikuyu profit: {results.get('KK_profit'):,.0f}")

st.write("*Hit refresh to update the results!*")
st.dataframe(period_df)

st.download_button(
    label="Download results",
    data=period_df.to_csv(index=True),
    mime="text/csv",
    file_name="profit_summary.csv",
)


def download_data(real_file_id):
    """Downloads a Google Drive folder

    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.getvalue()


st.button(
    label="Download latest data",
    on_click=download_data,
    kwargs={"real_file_id": "1xg_YYjGZTyTVFjGYWoeCi7LwZHKta1N2"},
)

# TODO: Implement Oauth2 authentication
