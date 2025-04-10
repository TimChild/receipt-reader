import io
import json
from pathlib import Path
from typing import Any

import boto3

from .response_models import ResponseModel


def get_textract_client(session: Any, region: str = "us-west-2") -> Any:
    client = session.client("textract", region_name=region)
    return client


def get_image_from_bucket(s3_connection: Any, bucket: str, document: str) -> bytes:
    s3_object = s3_connection.Object(bucket, document)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response["Body"].read())
    image_binary = stream.getvalue()
    return image_binary


def do_textract_process(client: Any, image_data: bytes) -> dict[str, Any]:
    response = client.analyze_expense(Document={"Bytes": image_data})
    return response


def validate_data(data: dict[str, Any]) -> ResponseModel:
    return ResponseModel.model_validate(data)


def save_data(data: ResponseModel, save_path: str) -> None:
    with Path(save_path).open("w") as f:
        f.write(data.model_dump_json(by_alias=True))


def get_raw_data(
    bucket: str,
    document: str,
    save_path: str,
    region: str = "us-west-2",
    profile: str | None = None,
) -> dict[str, Any]:
    session = boto3.Session(profile_name=profile)
    s3_connection = session.resource("s3")
    textract_client = get_textract_client(session, region)
    image_data = get_image_from_bucket(s3_connection, bucket, document)
    data = do_textract_process(textract_client, image_data)
    return data


def save_raw_data(data: dict[str, Any], save_path: str) -> None:
    with Path(save_path).open("w") as f:
        f.write(json.dumps(data, indent=2))


def save_validated_data(data: dict[str, Any], save_path: str) -> None:
    validated = validate_data(data)
    save_data(validated, save_path)


def load_raw_data(file_path: str) -> dict[str, Any]:
    with Path(file_path).open("r") as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    # raw_data = get_raw_data(
    #     bucket="timchild-test-bucket-20250404",
    #     document="example-receipt.png",
    #     save_path="output.json",
    # )
    # save_raw_data(raw_data, "raw_output.json")
    raw_data = load_raw_data("raw_output.json")
    save_validated_data(raw_data, "validated_output.json")
