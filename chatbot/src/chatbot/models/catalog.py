from dataclasses import dataclass


@dataclass
class CatalogCourse:
    catalog_id: int
    course_id: int
    course_type: str
    prefix: str
    code: str
    name: str
    units: str
    description: str
    prerequisites: str
    ge_category: str
    typically_offered: str
    teaching_mode: str
    grading: str

# https://catalog.sonoma.edu/content.php?filter%5B27%5D=MATH&filter%5B29%5D
# =161&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=11&expand=1&navoid=1421&search_database=Filter#acalog_template_course_filter