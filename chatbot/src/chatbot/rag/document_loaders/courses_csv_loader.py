from typing import Iterator

import pandas as pd

from langchain_community.document_loaders import CSVLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class CoursesCSVLoader(BaseLoader):

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
                               'course_oid',
                               'course_prefix',
                               'course_code',
                               'course_name',
                           ],
                           content_columns=[
                               'document_type',
                               'source_url',
                               'course_name',
                               'course_prefix',
                               'course_code',
                               'department_name',
                               'course_type',
                               'school_college_name',
                               'units',
                               'description',
                               'prerequisites',
                               'co_requisites',
                               'ge_category',
                               'typically_offered',
                               'teaching_mode',
                               'grading',
                               'program_usage',
                           ])
        return loader.lazy_load()

    def _preprocess_csv(self) -> str:
        use_columns = [
            'Catalog OID',
            'Course OID',
            'Department Name',
            'Course Type',
            'School/College Name',
            'Prefix',
            'Code',
            'Name',
            'Unit(s):',
            'Description (Rendered no HTML)',
            'Prerequisite(s): (Rendered no HTML)',
            'Co-requisite(s): (Rendered no HTML)',
            'GE Category:',
            'Typically Offered',
            'Teaching Mode:',
            'Grading:',
            'Program Usage',
            'Is Active',
        ]
        df = pd.read_csv(self.file_path,
                         usecols=use_columns,
                         encoding="utf-8",
                         dtype=str)
        df = df.rename(columns={
            'Catalog OID': 'catalog_oid',
            'Course OID': 'course_oid',
            'Department Name': 'department_name',
            'Course Type': 'course_type',
            'School/College Name': 'school_college_name',
            'Prefix': 'course_prefix',
            'Code': 'course_code',
            'Name': 'course_name',
            'Unit(s):': 'units',
            'Description (Rendered no HTML)': 'description',
            'Prerequisite(s): (Rendered no HTML)': 'prerequisites',
            'Co-requisite(s): (Rendered no HTML)': 'co_requisites',
            'GE Category:': 'ge_category',
            'Typically Offered': 'typically_offered',
            'Teaching Mode:': 'teaching_mode',
            'Grading:': 'grading',
            'Program Usage': 'program_usage',
        })

        # Filter out inactive courses
        df = df[df["Is Active"] == "1"]

        df['document_type'] = 'course'

        df['course_name'] = df['course_prefix'] + ' ' + df['course_code'] + ' - ' + df['course_name']

        base_url = "https://catalog.sonoma.edu/content.php?filter%5B27%5D="
        df['source_url'] = ((base_url + df['course_prefix'] +
                             '&filter%5B29%5D=' + df['course_code'])
                            + '&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter'
                              '%5Bcpage%5D=1&cur_cat_oid=11&expand=1&navoid=1421&search_database=Filter#')

        temp_file = self.file_path.replace(".csv", "_processed.csv")
        df.to_csv(temp_file, index=False, encoding="utf-8")

        return temp_file
