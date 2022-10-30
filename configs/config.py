import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
EXPENSES_DIR = ROOT_DIR / "data/raw/expenses"
SALES_DIR = ROOT_DIR / "data/raw/sales"

# Price lists (lowest)
pizza_large = (850, 900, 950, 1000)
pizza_medium = (650, 700, 750, 800)
pizza_small = (450, 500, 550, 600)
