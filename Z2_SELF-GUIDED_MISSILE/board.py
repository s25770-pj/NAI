from pydantic import BaseModel, conint


class Board(BaseModel):
    width: conint(ge=0, le=29999) = 10000
    height: conint(ge=0, le=29999) = 10000
