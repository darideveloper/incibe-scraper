import time
import itertools
from urllib.parse import urlparse
from libs.web_scraping import WebScraping


class Business_scraper(WebScraping):
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
                "Consultoría|Integrador",
                "Mayorista/Distribuidor",
                "Fabricante",
                "Proveedores de seguridad gestionada",
                "Proveedores especializados locales",
                "Revendedor de valor añadido (VAR)"
            ],
            "companySize": [
                "",
                "Pequeña empresa",
                "Mediana empresa",
                "Microempresa",
                "Gran empresa"
            ],
            "provinceHeadquarters": [
                "",
                "Madrid",
                "Barcelona",
                "Málaga",
                "Valencia/València",
                "Asturias",
                "Las Palmas",
                "Murcia",
                "Alicante",
                "Valladolid",
                "Vizcaya"
            ],
            "targetCompanySize": [
                "",
                "Mediana empresa",
                "Pequeña empresa",
                "Gran empresa",
                "Microempresa"
            ],
            "categories": [
                "",
                "Certificación normativa",
                "Implantación de soluciones",
                "Soporte y mantenimiento",
                "Auditoría Técnica",
                "Cumplimiento legal y normativo",
                "Formación y concienciación",
                "Contingencia y continuidad",
                "Protección de las comunicaciones",
                "Gestión de incidentes",
                "Seguridad en la nube"
            ],
            "subcategories": [
                "",
                "Sistemas de Gestión de la Seguridad de la Información",
                "Diseño de soluciones",
                "Seguridad Gestionada",
                "Análisis de logs y puertos",
                "Herramientas para el cumplimiento con la legislación",
                "Formación académica (masters, posgrados)",
                "Planes de contingencia y continuidad de negocio",
                "Cortafuegos", "Prevención de incidentes de seguridad",
                "Software como servicio (SaaS)"],
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

    def __generate_search_url__(self):
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
        base_url = "https://catalogo.incibe.es/search"

        params = {
            "page": "0",  # Página inicial
            "size": "25",  # Tamaño de página predeterminado
            "text": self.search_text,  # Palabras clave de búsqueda
        }

        for key, value in self.custom_filters.items():
            print(value)
            if int(value) != 0:
                params[str(key)] = value

        print(params)

    def search(self):
        return self.__generate_search_url__()

    def extract_business(self):
        pass
