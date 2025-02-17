from typing import Iterator

import bs4
import pandas as pd

from langchain_community.document_loaders import CSVLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class ProgramsCSVLoader(BaseLoader):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        processed_file = self._preprocess_csv()
        loader = CSVLoader(file_path=processed_file,
                           autodetect_encoding=True,
                           csv_args={
                               'dialect': 'excel'
                           },
                           source_column='source_url',
                           metadata_columns=[
                               'catalog_oid',
                               'program_oid',
                               'program_type',
                               'degree_type',
                               'program_name',
                           ],
                           content_columns=[
                               'document_type',
                               'source_url',
                               'program_name',
                               'program_type',
                               'degree_type',
                               'program_description',
                               'structure',
                           ])
        return loader.lazy_load()

    def _preprocess_csv(self) -> str:
        use_columns = [
            'Catalog OID',
            'Program OID',
            'Program Type',
            "Degree Type",
            "Program Code",
            "Program Name",
            "Program Description",
            "Structure",
            "Is Active",
        ]
        df = pd.read_csv(self.file_path,
                         usecols=use_columns,
                         encoding="utf-8",
                         dtype=str)
        df = df.rename(columns={
            'Catalog OID': 'catalog_oid',
            'Program OID': 'program_oid',
            'Program Type': 'program_type',
            'Degree Type': 'degree_type',
            'Program Name': 'program_name',
            'Program Description': 'program_description',
            'Structure': 'structure',
        })

        # Filter out inactive programs
        df = df[df["Is Active"] == "1"]

        df['document_type'] = 'program'

        # remove HTML from program description using bs4
        df['program_description'] = df['program_description'].fillna("").astype(str)
        df['program_description'] = df['program_description'].apply(
            lambda x: bs4.BeautifulSoup(x, "html.parser").get_text())

        base_url = "https://catalog.sonoma.edu/preview_program.php?catoid=11&returnto=1431&poid="
        df['source_url'] = base_url + df['program_oid']

        temp_file = self.file_path.replace(".csv", "_processed.csv")
        df.to_csv(temp_file, index=False, encoding="utf-8")

        return temp_file
