from typing import Literal, Type

import pandas as pd
from .base_stratified_tables import BaseStratifiedTables, SectionSettings


class BaseStratifiedNotByResponseTables(BaseStratifiedTables):
    def use_population_2c(self, section_settings: Type[SectionSettings]) -> bool:
        return section_settings.column_question == "q2c"

    def get_easy_read_weight_type_to_use(
        self, section_settings: Type[SectionSettings]
    ) -> Literal["Std", "ER", None]:
        if section_settings.column_question_er_info.easy_read_type in ["Std", "ER"]:
            return section_settings.column_question_er_info.easy_read_type
        return None
