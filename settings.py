# This file is expected to be a part of
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Bank import Bank, Card

backupPath = 'backup.json'
banks: list[Bank] = []
cards: list[Card] = []