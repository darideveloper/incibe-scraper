import itertools
from urllib.parse import quote_plus
from libs.web_scraping import WebScraping


class BusinessScraper(WebScraping):
    def __init__(self, keywords: list, headless: bool = False,
                 companyType: int = 0, companySize: int = 0, provinceHeadquarters: int = 0,
                 targetCompanySize: int = 0, categories: int = 0, subcategories: int = 0,
                 type: int = 0, language: int = 0, license: int = 0):
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

        # Get the url to search
        keywords_str = " ".join(keywords)
        self.search_text = f"{keywords_str}"

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

    def __add_all_filters__(self):
        """Add all filters to the dictionary."""
        for filter_name, filter_options in self.all_filters.items():
            self.filters[filter_name] = {i: option for i, option in enumerate(filter_options)}

    def __generate_all_combinations__(self):
        """Loop over all possible combinations
        it still can generate duplicated entries
        and it's not intended to be use in production yet
        """
        # Get the values of every filter
        filter_values = list(self.filters.values())

        # Calculate all posible combinations
        total_combinations = list(itertools.product(*filter_values))

        # Print the number of combinations
        self.logger.info("Número total de combinaciones: %d", len(total_combinations))

        # Loop through all combinations
        for combination in total_combinations:
            print(combination)

    def __loop_results__(self):
        pass

    def __generate_search_url__(self, page: int = 0):
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
            "text": quote_plus(self.search_text),  # Palabras clave de búsqueda
        }

        # Set all params
        for key, value in self.custom_filters.items():
            print(value)
            if int(value) != 0:
                params[str(key)] = self.filters[str(key)][int(value)]

        # Construye la URL con los parámetros
        url = base_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

        return url

    def search(self):
        url = self.__generate_search_url__()
        print(url)

    def extract_business(self):
        pass
