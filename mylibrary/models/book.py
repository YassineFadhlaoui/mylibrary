"""
module that implements the Model for Book
"""
from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import registry

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class BookModel:
    """
    Database Model for Book
    """
    __sa_dataclass_metadata_key__ = "sa"
    __tablename__ = "books"
    title: str = field(metadata={"sa": Column(String(1024), primary_key=True)})
    author: str = field(metadata={"sa": Column(String(256)), })
    cover: str = field(metadata={"sa": Column(String(2048), nullable=True)})
    finished: bool = field(metadata={"sa": Column(Boolean, default=False)})
    progress: int = field(metadata={"sa": Column(Integer, default=0)})
    notes: str = field(metadata={"sa": Column(String(4096), default="no notes yet", nullable=True)})
