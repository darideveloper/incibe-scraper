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
    
    # Open excel file
    manager = SpreadsheetManager("empresas.xlsx")
    
    # Create sheet if not exists, and set
    sheet_name = "ciberseguridad"
    manager.create_set_sheet("ciberseguridad")
    
    # Get business already extracted
    print("\nObteniendo empresas ya extraídas...")
    data = manager.get_data()
    business_extracted = [row[0] for row in data[1:]]
    last_row = len(data) + 1
    
    scraper = BusinessScraper(
        HEADLESS,
        COMPANY_TYPE,
        COMPANY_SIZE,
        PROVINCE_HEADQUARTERS,
        TARGET_COMPANY_SIZE,
        CATEGORIES,
        SUBCATEGORIES,
        TYPE,
        LANGUAGE,
        LICENSE,
        business_extracted
    )
    
    # Write header
    header = [[
        "Nombre",
        "Descripción",
        "Ubicación",
        "Teléfono",
        "Correo",
        "Sitio web",
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
    
    # Extract each keyword
    for keyword in KEYWORDS:
        print("\n______________________________")
        print(f">>> Buscando empresas con la palabra clave: {keyword}")
        
        # Get data
        data = scraper.search(keyword)
        if data:
            print(f">>> Empresas nuevas encontradas: {len(data)}")
        else:
            print(">>> No se encontraron empresas con la palabra clave")
            continue
        
        # Write content
        manager.write_data(data, start_row=last_row, start_column=1)
        manager.save()
        
        # Update last row
        last_row += len(data)
        
    # Skill browser when finish
    scraper.driver.quit()