# app/validation.py

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemIn(BaseModel):
    """Request body for POST /items."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)

    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    quantity: Optional[int] = Field(default=None, ge=0, le=1_000_000)
