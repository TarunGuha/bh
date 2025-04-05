from pydantic import BaseModel, ConfigDict


class UserBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
    )
