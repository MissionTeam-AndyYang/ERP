from pydantic import BaseModel, ConfigDict, Field


class BatchNumberBase(BaseModel):
    date: int | None = None
    creator_no: str | None = Field(default=None, max_length=60)
    refCategory: int | None = None
    item_no: str | None = Field(default=None, max_length=60)
    item_name: str | None = Field(default=None, max_length=60)
    item_ref_no: str | None = Field(default=None, max_length=60)
    item_ref_displayName: str | None = Field(default=None, max_length=60)
    itemCategory: int | None = None
    itemSubCategory: int | None = None
    itemType: int | None = None
    unit: int | None = None
    expectedCount: float | None = None
    checkedCount: float | None = None
    validDays: int | None = None
    validDate: int | None = None
    validDateNo: str | None = Field(default=None, max_length=60)
    comment: str | None = Field(default=None, max_length=128)
    creationTime: int | None = None


class BatchNumberCreate(BatchNumberBase):
    no: str = Field(min_length=1, max_length=60)
    ref_no: str = Field(min_length=1, max_length=60)


class BatchNumberUpdate(BatchNumberBase):
    no: str | None = Field(default=None, min_length=1, max_length=60)
    ref_no: str | None = Field(default=None, min_length=1, max_length=60)


class BatchNumberRead(BatchNumberBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    no: str
    ref_no: str


class BatchNumberList(BaseModel):
    total: int
    items: list[BatchNumberRead]
