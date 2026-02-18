"""Shared Pydantic v2 base model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BOJBaseModel(BaseModel):
    """Base model with shared configuration for all BOJ models."""

    model_config = ConfigDict(
        populate_by_name=True,
        frozen=True,
    )
