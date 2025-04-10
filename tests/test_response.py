import pytest
from pydantic import BaseModel

from receipt_reader.response_models import LineItem, LineItemExpenseField, ValueDetection


@pytest.fixture
def line_item() -> LineItem:
    return LineItem(
        LineItemExpenseFields=[
            LineItemExpenseField(PageNumber=1, ValueDetection=ValueDetection(Text="some text"))
        ]
    )


class ItemInfo(BaseModel):
    text: str
    amount: float


def test_line_item(line_item: LineItem):
    assert isinstance(line_item, LineItem)
    assert line_item.line_item_expense_fields[0].page_number == 1
    assert line_item.line_item_expense_fields[0].value_detection.text == "some text"


def test_convert_to_item_infos(line_item: LineItem):
    infos = convert_to_item_infos(line_item)
    assert isinstance(infos, list)
    assert all(isinstance(info, ItemInfo) for info in infos)
