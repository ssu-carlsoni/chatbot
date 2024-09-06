from abc import ABC

from bs4 import BeautifulSoup

from ..models.document import Document


class Extractor(ABC):
    @staticmethod
    def get_search_content(document: Document) -> str:
        pass

    @staticmethod
    def get_prompt_content(document: Document) -> str:
        pass

    @staticmethod
    def get_urls(document: Document) -> [str]:
        pass


class CatalogExtractor(Extractor):
    @staticmethod
    def get_search_content(document: Document) -> str:
        content = ''
        elements = CatalogExtractor.get_elements(document)
        for element in elements:
            content += (element.get_text()
                        .replace("•", "")
                        .replace("\u00A0", "")
                        .strip() + '\n')
        return content

    @staticmethod
    def get_prompt_content(document: Document) -> str:
        content = ''
        elements = CatalogExtractor.get_elements(document)
        for element in elements:
            content += f'{element.name}: {element.get_text()}\n'
        return content

    @staticmethod
    def get_urls(document: Document) -> [str]:
        soup = BeautifulSoup(document.raw_content, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('preview_'):
                if href not in urls:
                    urls.append(link.get('href'))
        absolute_urls = [f'https://catalog.sonoma.edu/{url}' for url in urls]
        return absolute_urls

    @staticmethod
    def get_elements(document: Document) -> [str]:
        elements = []
        soup = BeautifulSoup(document.raw_content, 'html.parser')
        content_wrapper = (soup.find('h1')
                           .find_parent('table')
                           .find_parent('table'))

        found_h1 = False
        for element in content_wrapper.find_all(['h1', 'h2', 'h3', 'h4',
                                                 'h5', 'h6', 'p', 'li',]):
            if not found_h1 and element.name == 'h1':
                found_h1 = True

            if found_h1:
                elements.append(element)

        return elements