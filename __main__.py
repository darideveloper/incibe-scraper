import os
from dotenv import load_dotenv
from logic.business_scraper import BusinessScraper
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
    scraper = BusinessScraper(
        KEYWORDS,
        HEADLESS,
        COMPANY_TYPE,
        COMPANY_SIZE,
        PROVINCE_HEADQUARTERS,
        TARGET_COMPANY_SIZE,
        CATEGORIES,
        SUBCATEGORIES,
        TYPE,
        LANGUAGE,
        LICENSE
    )
    
    # Get data
    data = scraper.search()
    
    # Skill browser when finish
    scraper.driver.quit()

    # Open excel file
    print("Escribiendo en el archivo excel...")
    manager = SpreadsheetManager("empresas.xlsx")
    
    # Create sheet if not exists
    manager.create_set_sheet("ciberseguridad")
    
    # Write header
    header = [[
        "Nombre",
        "Descripción",
        "Ubicación",
        "Teléfono",
        "Correo",
        "Sitio web"
        "Typo de empresa",
        "Tamaño de empresa",
        "Provincia",
        "Tamaño de empresa objetivo",
        "Categorías",
        "Subcategorías",
        "Tipo",
        "Idioma",
        "Licencia"
    ]]
    manager.write_data(header, start_row=1, start_column=1)

    # Write content
    manager.write_data(data, start_row=2, start_column=1)
    manager.save()
