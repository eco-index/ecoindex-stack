from pydantic import BaseModel

class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """

class IDModelMixin(BaseModel):
    id: int

# @dataclass
# class InventoryItem:
#     """Class for keeping track of an item in inventory."""
#     name: str
#     unit_price: float
#     quantity_on_hand: int = 0

#     def total_cost(self) -> float:
#         return self.unit_price * self.quantity_on_hand

# class Item:
#     def __init__(self, *, name: str, unit_price: float, quantity_on_hand: int = 0) -> None:
#         self.name = name
#         self.unit_price = unit_price
#         self.quantity_on_hand = quantity_on_hand
        
#     def total_cost(self) -> float:
#         return self.unit_price * self.quantity_on_hand