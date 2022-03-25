
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Bank import Bank, Card
    from ATM import ATM

backupPath = 'backup.json'
banks: list[Bank] = []
cards: list[Card] = []
atm: ATM