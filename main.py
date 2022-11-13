import argparse
import os
from glob import glob

from app import get_results
<<<<<<< HEAD
<<<<<<< HEAD
from configs import config
=======
import argparse
>>>>>>> f072879 (Add cli params)
=======
from configs import config
>>>>>>> abe773f (Add pre-commit hooks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_period", type=int, help="Start period")
    parser.add_argument("--end_period", type=int, help="End period")
    args = parser.parse_args()

    start_period = args.start_period
    end_period = args.end_period

    sales_paths = glob(pathname=os.path.join(config.SALES_DIR, "*.xls*"))
    expenses_paths = glob(pathname=os.path.join(config.EXPENSES_DIR, "*.csv"))

    get_results(
        sales_data=sales_paths,
        expenses_data=expenses_paths,
        start_period=start_period,
        end_period=end_period,
    )
    exit()
