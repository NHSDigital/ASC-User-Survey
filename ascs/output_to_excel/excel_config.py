from typed_params import BaseModel


class ExcelConfig(BaseModel):
    SHEET_NAME: str
    START_ROW: int
    START_COLUMN: int
    HORIZONTAL_GAP_SIZE: int
    VERTICAL_GAP_SIZE: int
