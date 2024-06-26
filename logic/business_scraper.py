import re
import time
from urllib.parse import quote_plus
from libs.web_scraping import WebScraping


class BusinessScraper(WebScraping):
    def __init__(self, headless: bool = False,
                 companyType: int = 0, companySize: int = 0,
                 provinceHeadquarters: int = 0, targetCompanySize: int = 0,
                 categories: int = 0, subcategories: int = 0,
                 type: int = 0, language: int = 0, license: int = 0,
                 business_extracted: str = ""):
        """ Start chrome and save search text

        Args:
            keywords (list): Keywords to search
            headless (bool, optional): If True, the browser will not be shown.
                Defaults to False.
        """

        # Initialize scraper
        super().__init__(
            headless=headless,
        )

        # Custom filters
        self.custom_filters = {
            "companyType": companyType,
            "companySize": companySize,
            "provinceHeadquarters": provinceHeadquarters,
            "targetCompanySize": targetCompanySize,
            "categories": categories,
            "subcategories": subcategories,
            "type": type,
            "language": language,
            "license": license
        }

        # Define all filters
        self.all_filters = {
            "companyType": [
                "",
                "Consultoría%7CIntegrador",
                "Mayorista%2FDistribuidor",
                "Fabricante",
                "Proveedores%20de%20seguridad%20gestionada",
                "Proveedores%20especializados%20locales",
                "Revendedor%20de%20valor%20añadido%20(VAR)"
            ],
            "companySize": [
                "",
                "Pequeña%20empresa",
                "Mediana%20empresa",
                "Microempresa",
                "Gran%20empresa"
            ],
            "provinceHeadquarters": [
                "",
                "Madrid",
                "Barcelona",
                "Málaga",
                "Valencia%2FValència",
                "Asturias",
                "Las%20Palmas",
                "Murcia",
                "Alicante",
                "Valladolid",
                "Vizcaya"
            ],
            "targetCompanySize": [
                "",
                "Mediana%20empresa",
                "Pequeña%20empresa",
                "Gran%20empresa",
                "Microempresa"
            ],
            "categories": [
                "",
                "Certificación%20normativa",
                "Implantación%20de%20soluciones",
                "Soporte%20y%20mantenimiento",
                "Auditoría%20Técnica",
                "Cumplimiento%20legal%20y%20normativo",
                "Formación%20y%20concienciación",
                "Contingencia%20y%20continuidad",
                "Protección%20de%20las%20comunicaciones",
                "Gestión%20de%20incidentes",
                "Seguridad%20en%20la%20nube"
            ],
            "subcategories": [
                "",
                "Sistemas%20de%20Gestión%20de%20la%20Seguridad%20de%20la%20Información",
                "Diseño%20de%20soluciones",
                "Seguridad%20Gestionada",
                "Análisis%20de%20logs%20y%20puertos",
                "Herramientas%20para%20el%20cumplimiento%20con%20la%20legislación",
                "Formación%20académica%20(masters,%20posgrados)",
                "Planes%20de%20contingencia%20y%20continuidad%20de%20negocio",
                "Cortafuegos",
                "Prevención%20de%20incidentes%20de%20seguridad",
                "Software%20como%20servicio%20(SaaS)"
            ],
            "type": [
                "",
                "SERVICE",
                "PRODUCT"
            ],
            "language": [
                "",
                "español",
                "inglés",
                "catalán",
                "alemán",
                "francés",
                "italiano",
                "otros",
                "portugués"
            ],
            "license": [
                "",
                "false",
                "true"
            ]
        }

        # Create a dictionary
        self.filters = {filter_name: {0: ""} for filter_name in self.all_filters}

        # Add all filters to dictionary
        self.__add_all_filters__()
        
        self.business_extracted = business_extracted

    def __add_all_filters__(self):
        """Add all filters to the dictionary."""
        for filter_name, filter_options in self.all_filters.items():
            self.filters[filter_name] = {
                i: option for i, option in enumerate(filter_options)
            }

    def __check_results__(self, selectors: str, tries: int = 3):
        try:
            self.refresh_selenium()
            time.sleep(10)
            self.implicit_wait(selectors["total_business"], True)
        except Exception:
            print("Problemas de coneccion")

    def __loop_results__(self, selectors: str, page: int, keyword: str):
        url = self.__generate_search_url__(page, keyword)
        self.set_page(url)

        # Wait till the element appears
        self.__check_results__(selectors)

        # Fetch Current elements
        elems = self.get_elems(selectors["business_list"])

        return elems

    def __get_counter__(self, selectors: str):
        # Get business quantity
        time.sleep(5)
        business = self.get_text(selectors["total_business"])

        # Extract numeric quantity value
        business_values = re.search(r'\d+', business)
        total_business = int(business_values.group())

        # Set business counter
        counter = int(total_business)

        return counter

    def __generate_search_url__(self, page: int, keyword: str):
        """ companyType: Tipo de empresa
            companySize: Tamaño de empresa
            provinceHeadquarters: Sede de empresa
            targetCompanySize: Empresa a la que se dirige
            categories: Categoria
            subcategories: Subcategoria
            type: Tipo
            language": Idiomas
            license": Gratuito
        """
        # Base url
        base_url = "https://catalogo.incibe.es/search"

        # Parameters
        params = {
            "page": page,  # Página inicial
            "size": "25",  # Tamaño de página predeterminado
            "text": quote_plus(keyword),  # Palabras clave de búsqueda
        }

        # Set all params
        for key, value in self.custom_filters.items():
            if int(value) != 0:
                params[str(key)] = self.filters[str(key)][int(value)]

        # Construye la URL con los parámetros
        url = base_url + "?" + "&".join([
            f"{key}={value}" for key, value in params.items()
        ])

        return url

    def search(self, keyword: str):
        """ Search for a keyword and extract data

        Args:
            keyword (str): Keyword to search

        Returns:
            list: extracted data from businesses
        """
        
        selectors = {
            "total_business": "div.list__info__data__total",
            "business_list": ".list__company",
            "business_name": ".mat-expansion-panel-header",
            "expand": "mat-expansion-panel-header",
            "description": ".mat-expansion-panel-body .description",
            "location": ".mat-expansion-panel-body"
                        " .container .row .contact-data.mt-0 div",
            "phone": ".mat-expansion-panel-body .container .row .contact-data a",
            "email": ".mat-expansion-panel-body .container .row .contact-data.mt-0 a",
            "website": ".mat-expansion-panel-body .container"
                       " .row.mt-3 .contact-data:nth-child(2)"
        }

        # Define current page
        page = 0

        # Fetch target business quantity
        elems = self.__loop_results__(selectors, page, keyword)
        if not elems:
            print("No se encontraron resultados con esa combinacion de filtros.")
            return []

        business = self.__get_counter__(selectors)

        print(f"Extrayendo datos de {business} empresas..")

        # Debug
        return self.extract_business(selectors, business, keyword)
    
    def extract_business(self, selectors: str, business: int, keyword: str = ""):
        counter = business
        page = 0

        extracted_data = []
        
        # Get filters values
        filters_values = {}
        for filter_name, filter_id in self.custom_filters.items():
            filter_value = self.filters[filter_name][int(filter_id)]
            filter_value = filter_value.replace("%20", " ").replace("%7C", "/")
            filters_values[filter_name] = filter_value

        while counter > 0:
            elems = self.__loop_results__(selectors, page, keyword)
            time.sleep(5)

            # If elems aren't empty loop throug business's data
            for item in range(0, len(elems)):
                # Extract business's name (try 3 times)
                time.sleep(1)
                extracted = False
                for _ in range(3):
                    try:
                        name_object = self.get_text(
                            elems[item],
                            selectors["business_name"]
                        )
                    except Exception:
                        print("Error al extraer, reintentando...")
                        time.sleep(10)
                        self.refresh_selenium()
                        continue
                    else:
                        extracted = True
                        
                if not extracted:
                    print("* Error al extraer datos en la página actual.")
                    counter -= 25
                    continue

                # Filter business's name values
                name = re.sub(r'[\s\n]*Empresa|[\n\r]+', '', name_object)
                count_text = f"{business - counter + 1}/{business}"
                if name in self.business_extracted:
                    print(f"Empresa {name} ya extraída. {count_text}")
                    counter -= 1
                    continue

                print(f"Extrayendo {name}... {count_text}")

                # Extract business data
                self.click_js(elems[item], selectors["expand"])

                # Wait a few seconds to load data
                time.sleep(5)

                # harvest data
                description = self.get_text(elems[item], selectors["description"])

                location = self.get_text(elems[item], selectors["location"])

                phone = self.get_text(elems[item], selectors["phone"])

                email = self.get_text(elems[item], selectors["email"])

                website_object = self.get_text(elems[item], selectors["website"])
                website = re.sub(
                    r'^\s*wysiwyg\s*|\s*$',
                    "",
                    website_object,
                    flags=re.MULTILINE
                )

                # Store in a temporal list
                temp = [
                    name,
                    description,
                    location,
                    phone,
                    email,
                    website,
                ]
                
                # Add filters values to register
                for _, filter_value in filters_values.items():
                    temp.append(filter_value)

                # Append to extracted data
                extracted_data.append(temp)
                
                # Save business name
                self.business_extracted.append(name)

                counter -= 1
                if counter == 0:
                    break

            page += 1

            if counter == 0:
                break

        return extracted_data
