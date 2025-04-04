import boto3
import io
import json
from typing import Any, Dict, List
from PIL import Image, ImageDraw
import click


def show_bounding_box(
    draw: ImageDraw.ImageDraw, box: Dict[str, float], width: int, height: int, box_color: str
) -> None:
    left = width * box["Left"]
    top = height * box["Top"]
    draw.rectangle(
        [left, top, left + (width * box["Width"]), top + (height * box["Height"])],
        outline=box_color,
    )


def show_selected_element(
    draw: ImageDraw.ImageDraw, box: Dict[str, float], width: int, height: int, box_color: str
) -> None:
    left = width * box["Left"]
    top = height * box["Top"]
    draw.rectangle(
        [left, top, left + (width * box["Width"]), top + (height * box["Height"])], fill=box_color
    )


def display_block_information(block: Dict[str, Any]) -> Dict[str, Any]:
    block_info = {
        "Id": block.get("Id"),
        "Type": block.get("BlockType"),
        "Confidence": block.get("Confidence", 0),
        "Text": block.get("Text", ""),
        "Geometry": block.get("Geometry"),
    }

    if block["BlockType"] == "CELL":
        block_info.update(
            {
                "Column": block.get("ColumnIndex"),
                "Row": block.get("RowIndex"),
                "ColumnSpan": block.get("ColumnSpan"),
                "RowSpan": block.get("RowSpan"),
            }
        )

    if "Relationships" in block:
        block_info["Relationships"] = block["Relationships"]

    if block["BlockType"] == "KEY_VALUE_SET":
        block_info["EntityType"] = block.get("EntityTypes", [None])[0]

    if block["BlockType"] == "SELECTION_ELEMENT":
        block_info["SelectionStatus"] = block.get("SelectionStatus")

    if "Page" in block:
        block_info["Page"] = block["Page"]

    return block_info


def process_text_analysis(
    s3_connection: boto3.resource, client: boto3.client, bucket: str, document: str
) -> List[Dict[str, Any]]:
    s3_object = s3_connection.Object(bucket, document)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response["Body"].read())
    image = Image.open(stream)

    image_binary = stream.getvalue()
    response = client.analyze_document(
        Document={"Bytes": image_binary}, FeatureTypes=["TABLES", "FORMS", "SIGNATURES"]
    )

    blocks = response["Blocks"]
    width, height = image.size
    block_data = []

    for block in blocks:
        block_info = display_block_information(block)
        block_data.append(block_info)

        draw = ImageDraw.Draw(image)
        if block["BlockType"] == "KEY_VALUE_SET":
            if block["EntityTypes"][0] == "KEY":
                show_bounding_box(draw, block["Geometry"]["BoundingBox"], width, height, "red")
            else:
                show_bounding_box(draw, block["Geometry"]["BoundingBox"], width, height, "green")
        if block["BlockType"] == "TABLE":
            show_bounding_box(draw, block["Geometry"]["BoundingBox"], width, height, "blue")
        if block["BlockType"] == "CELL":
            show_bounding_box(draw, block["Geometry"]["BoundingBox"], width, height, "yellow")
        if block["BlockType"] == "SELECTION_ELEMENT":
            if block["SelectionStatus"] == "SELECTED":
                show_selected_element(draw, block["Geometry"]["BoundingBox"], width, height, "blue")

    image.show()
    return block_data


@click.command()
@click.option("--profile", default=None, help="AWS profile name")
@click.option("--region", default="us-west-2", help="AWS region name")
@click.option("--bucket", prompt="Bucket name", help="S3 bucket name")
@click.option("--document", prompt="Document name", help="Document name in S3 bucket")
def main(profile: str, region: str, bucket: str, document: str) -> None:
    """
    Main function to analyze the document stored in S3 using AWS Textract.
    """
    session = boto3.Session(profile_name=profile)
    s3_connection = session.resource("s3")
    client = session.client("textract", region_name=region)

    block_data = process_text_analysis(s3_connection, client, bucket, document)

    # Save the block data to a JSON file
    output_file = f"{document.split('.')[0]}_analysis.json"
    with open(output_file, "w") as f:
        json.dump(block_data, f, indent=4)

    print(f"Analysis complete. Data saved to {output_file}")


if __name__ == "__main__":
    main()
