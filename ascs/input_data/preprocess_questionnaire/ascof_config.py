import typed_params


class SimpleAscofConversion(typed_params.BaseModel):
    """
    This class represents a simple ascof conversion where a conversion is
    one question's responses recoded to new values
    e.g q3a's responses [1, 2, 3, 4] becomes [1, 1, 2, 2]
    """

    SCORE_NAME: str
    QUESTION_COLUMN: str
    CONVERSION: dict[int, int]
