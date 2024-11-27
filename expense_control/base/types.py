from typing import TypeVar
from pydantic import BaseModel

from expense_control.base.model import Base

Model = TypeVar('Model', bound=Base)

CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)

EntitySchema = TypeVar('EntitySchema', bound=BaseModel)

FilterSchema = TypeVar('FilterSchema', bound=BaseModel)

