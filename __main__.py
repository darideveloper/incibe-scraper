import os
from dotenv import load_dotenv
from logic import BusinessScraper
from libs import SpreadsheetManager

# Env variables
load_dotenv()
HEADLESS = os.getenv("SHOW_BROWSER") != "True"
KEYWORDS = os.getenv("KEYWORDS").split(",")
COMPANY_TYPE = os.getenv("COMPANY_TYPE")
COMPANY_SIZE = os.getenv("COMPANY_SIZE")
PROVINCE_HEADQUARTERS = os.getenv("PROVINCE_HEADQUARTERS")
TARGET_COMPANY_SIZE = os.getenv("TARGET_COMPANY_SIZE")
CATEGORIES = os.getenv("CATEGORIES")
SUBCATEGORIES = os.getenv("SUBCATEGORIES")
TYPE = os.getenv("TYPE")
LANGUAGE = os.getenv("LANGUAGE")
LICENSE = os.getenv("LICENSE")

if __name__ == "__main__":
    scraper = BusinessScraper(KEYWORDS,
                              HEADLESS,
                              COMPANY_TYPE,
                              COMPANY_SIZE,
                              PROVINCE_HEADQUARTERS,
                              TARGET_COMPANY_SIZE,
                              CATEGORIES,
                              SUBCATEGORIES,
                              TYPE,
                              LANGUAGE,
                              LICENSE)

    data = scraper.search()

    manager = SpreadsheetManager("empresas.xlsx")
    manager.set_sheet("cyberseguridad")

    manager.write_data(data, start_row=2, start_column=1)
    manager.save()
