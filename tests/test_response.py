import pytest

from receipt_reader.response_models import LineItem, LineItemExpenseField, ValueDetection


@pytest.fixture
def line_item() -> LineItem:
    return LineItem(
        LineItemExpenseFields=[
            LineItemExpenseField(PageNumber=1, ValueDetection=ValueDetection(Text="some text"))
        ]
    )


def test_line_item(line_item: LineItem):
    assert isinstance(line_item, LineItem)
