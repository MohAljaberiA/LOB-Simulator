from dataclasses import dataclass
import time

@dataclass
class Order:
    order_id: int           # Unique Order ID
    side: str               # 'Buy' or 'Sell'
    price: float            # Limit Price
    quantity: int           # Number of Units
    timestamp: float = None # Time of Order Creation 

    def __post_init_(self):
        if self.timestamp is None:
            self.timestamp = time.time()
            
