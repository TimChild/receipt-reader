from pydantic import BaseModel, Field


class S3Object(BaseModel):
    bucket: str = Field(..., alias="Bucket")
    name: str = Field(..., alias="Name")
    version: str = Field(..., alias="Version")


class Document(BaseModel):
    bytes: str = Field(..., alias="Bytes")
    s3_object: S3Object = Field(..., alias="S3Object")


class DocumentModel(BaseModel):
    document: Document = Field(..., alias="Document")
