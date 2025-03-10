from pydantic import BaseModel, ConfigDict


class ConfigBase(BaseModel):
    key: str
    value: str = ''


class ConfigOut(ConfigBase):
    class Config:
        model_config = ConfigDict(from_attributes=True)
