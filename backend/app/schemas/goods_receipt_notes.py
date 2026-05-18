from pydantic import BaseModel, ConfigDict, Field


class GoodsReceiptNoteBase(BaseModel):
    creator_no: str | None = Field(default=None, max_length=60)
    purchase_order_no: str | None = Field(default=None, max_length=60)
    date: int | None = None
    category: int | None = None
    item_ref_no: str | None = Field(default=None, max_length=60)
    item_ref_displayName: str | None = Field(default=None, max_length=60)
    item_no: str | None = Field(default=None, max_length=255)
    item_name: str | None = Field(default=None, max_length=255)
    itemCategory: int | None = None
    itemSubCategory: int | None = None
    unit: int | None = None
    price: float | None = None
    expectedCount: float | None = None
    checkedCount: float | None = None
    feeCount: float | None = None
    amount: int | None = None
    addDeleteAmount: int | None = None
    comment: str | None = Field(default=None, max_length=128)
    creationTime: int | None = None


class GoodsReceiptNoteCreate(GoodsReceiptNoteBase):
    no: str = Field(min_length=1, max_length=20)


class GoodsReceiptNoteUpdate(GoodsReceiptNoteBase):
    no: str | None = Field(default=None, min_length=1, max_length=20)


class GoodsReceiptNoteRead(GoodsReceiptNoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    no: str


class GoodsReceiptNoteList(BaseModel):
    total: int
    items: list[GoodsReceiptNoteRead]
