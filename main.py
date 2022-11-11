from configs import config
from glob import glob
import os
from app import get_results

if __name__ == "__main__":
    start_period = 202001
    end_period = 202212

    sales_paths = glob(pathname=os.path.join(config.SALES_DIR, "*.xls*"))
    expenses_paths = glob(pathname=os.path.join(config.EXPENSES_DIR, "*.csv"))

    get_results(
        sales_data=sales_paths,
        expenses_data=expenses_paths,
        start_period=start_period,
        end_period=end_period,
    )
    exit()
