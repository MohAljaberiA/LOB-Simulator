from collections import defaultdict, deque
from typing import Dict, Deque, Optional
from .order import Order


class OrderBook:
    def _init_(self) -> None:
        # price -> queue of orders at that price
        self.bids: Dict[float, Deque[Order]] = defaultdict(deque)
        self.asks: Dict[float, Deque[Order]] = defaultdict(deque)

    # ---------- Internal helper ----------

    def _get_book_side(self, side: str) -> Dict[float, Deque[Order]]:
        side = side.upper()
        if side == "BUY":
            return self.bids
        elif side == "SELL":
            return self.asks
        else:
            raise ValueError("side must be 'BUY' or 'SELL'")

    # ---------- Public API ----------

    def add_limit_order(self, order: Order) -> None:
        book_side = self._get_book_side(order.side)
        book_side[order.price].append(order)

    def best_bid(self) -> Optional[float]:
        if not self.bids:
            return None
        return max(self.bids.keys())

    def best_ask(self) -> Optional[float]:
        if not self.asks:
            return None
        return min(self.asks.keys())

    def spread(self) -> Optional[float]:
        (ask - bid), or None if one side is empty.
        ask = self.best_ask()
        if bid is None or ask is None:
            return None
        return ask - bid

    def mid_price(self) -> Optional[float]:
        bid = self.best_bid()
        ask = self.best_ask()
        if bid is None or ask is None:
            return None
        return (bid + ask) / 2