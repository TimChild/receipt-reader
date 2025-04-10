from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    height: float = Field(..., alias="Height")
    left: float = Field(..., alias="Left")
    top: float = Field(..., alias="Top")
    width: float = Field(..., alias="Width")


class PolygonPoint(BaseModel):
    x: float = Field(..., alias="X")
    y: float = Field(..., alias="Y")


class Geometry(BaseModel):
    bounding_box: BoundingBox = Field(..., alias="BoundingBox")
    polygon: list[PolygonPoint] = Field(..., alias="Polygon")


class Query(BaseModel):
    alias: str = Field(..., alias="Alias")
    pages: list[str] = Field(..., alias="Pages")
    text: str = Field(..., alias="Text")


class Relationship(BaseModel):
    ids: list[str] = Field(..., alias="Ids")
    type: str = Field(..., alias="Type")


class Block(BaseModel):
    block_type: str = Field(..., alias="BlockType")
    column_index: int | None = Field(None, alias="ColumnIndex")
    column_span: int | None = Field(None, alias="ColumnSpan")
    confidence: float = Field(..., alias="Confidence")
    entity_types: list[str] = Field(..., alias="EntityTypes")
    geometry: Geometry = Field(..., alias="Geometry")
    id: str = Field(..., alias="Id")
    page: int = Field(..., alias="Page")
    query: Query | None = Field(None, alias="Query")
    relationships: list[Relationship] | None = Field(None, alias="Relationships")
    row_index: int | None = Field(None, alias="RowIndex")
    row_span: int | None = Field(None, alias="RowSpan")
    selection_status: str | None = Field(None, alias="SelectionStatus")
    text: str | None = Field(None, alias="Text")
    text_type: str | None = Field(None, alias="TextType")


class Currency(BaseModel):
    code: str = Field(..., alias="Code")
    confidence: float = Field(..., alias="Confidence")


class GroupProperty(BaseModel):
    id: str = Field(..., alias="Id")
    types: list[str] = Field(..., alias="Types")


class LabelDetection(BaseModel):
    confidence: float = Field(..., alias="Confidence")
    geometry: Geometry = Field(..., alias="Geometry")
    text: str = Field(..., alias="Text")


class TypeField(BaseModel):
    confidence: float = Field(..., alias="Confidence")
    text: str = Field(..., alias="Text")


class ValueDetection(BaseModel):
    confidence: float = Field(..., alias="Confidence")
    geometry: Geometry = Field(..., alias="Geometry")
    text: str = Field(..., alias="Text")


class LineItemExpenseField(BaseModel):
    currency: Currency | None = Field(None, alias="Currency")
    group_properties: list[GroupProperty] | None = Field(None, alias="GroupProperties")
    label_detection: LabelDetection | None = Field(None, alias="LabelDetection")
    page_number: int = Field(..., alias="PageNumber")
    type: TypeField = Field(..., alias="Type")
    value_detection: ValueDetection = Field(..., alias="ValueDetection")


class LineItem(BaseModel):
    line_item_expense_fields: list[LineItemExpenseField] = Field(..., alias="LineItemExpenseFields")


class LineItemGroup(BaseModel):
    line_item_group_index: int = Field(..., alias="LineItemGroupIndex")
    line_items: list[LineItem] = Field(..., alias="LineItems")


class SummaryField(BaseModel):
    currency: Currency | None = Field(None, alias="Currency")
    group_properties: list[GroupProperty] | None = Field(None, alias="GroupProperties")
    label_detection: LabelDetection | None = Field(None, alias="LabelDetection")
    page_number: int = Field(..., alias="PageNumber")
    type: TypeField = Field(..., alias="Type")
    value_detection: ValueDetection = Field(..., alias="ValueDetection")


class ExpenseDocument(BaseModel):
    blocks: list[Block] = Field(..., alias="Blocks")
    expense_index: int = Field(..., alias="ExpenseIndex")
    line_item_groups: list[LineItemGroup] = Field(..., alias="LineItemGroups")
    summary_fields: list[SummaryField] = Field(..., alias="SummaryFields")


class DocumentMetadata(BaseModel):
    pages: int = Field(..., alias="Pages")


class ResponseModel(BaseModel):
    document_metadata: DocumentMetadata = Field(..., alias="DocumentMetadata")
    expense_documents: list[ExpenseDocument] = Field(..., alias="ExpenseDocuments")
