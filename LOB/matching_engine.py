from typing import List, Dict, Any
from .order import Order
from .order_book import OrderBook
import time


class MatchingEngine:
    """
    Core matching logic:
    - Takes incoming orders
    - Matches them against the opposite side of the book
    - Records trades (price, quantity, buy_id, sell_id)
    """

    def _init_(self):
        self.book = OrderBook()
        self.trades: List[Dict[str, Any]] = []

    def _record_trade(self, price: float, quantity: int, buy_id: int, sell_id: int):
        """
        Add a trade record to the log.
        """
        self.trades.append({
            "timestamp": time.time(),
            "price": price,
            "quantity": quantity,
            "buy_id": buy_id,
            "sell_id": sell_id
        })

    def process_order(self, order: Order):
        """
        Main entry point: handles matching logic.

        If order matches immediately, execute trades.
        Otherwise, store it as a limit order in the book.
        """
        # Determine opposite side
        if order.side == "BUY":
            opposite = self.book.asks
            price_check = lambda best_ask: best_ask is not None and best_ask <= order.price
            best_price_fn = self.book.best_ask
        else:
            opposite = self.book.bids
            price_check = lambda best_bid: best_bid is not None and best_bid >= order.price
            best_price_fn = self.book.best_bid


        while True:
            best_price = best_price_fn()
            if not price_check(best_price):
                break

            price_level_queue = opposite[best_price]
            best_order = price_level_queue[0]

            # Determine trade quantity
            traded_qty = min(order.quantity, best_order.quantity)

            # Record the trade
            if order.side == "BUY":
                self._record_trade(best_price, traded_qty, order.order_id, best_order.order_id)
            else:
                self._record_trade(best_price, traded_qty, best_order.order_id, order.order_id)

            # Update quantities
            order.quantity -= traded_qty
            best_order.quantity -= traded_qty

            # Remove fully filled orders from the price level
            if best_order.quantity == 0:
                price_level_queue.popleft()

            # Remove empty price level
            if not price_level_queue:
                del opposite[best_price]

            # If incoming order is fully matched, done
            if order.quantity == 0:
                return

        # If we reached here: order not fully matched, add remainder to book
        self.book.add_limit_order(order)