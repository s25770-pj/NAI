from pydantic import BaseModel, confloat, Field
from uuid import UUID, uuid4


class UFO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    height: confloat(gt=0) = None
    speed: confloat(gt=0) = None
    temperature: confloat(gt=0) = None

