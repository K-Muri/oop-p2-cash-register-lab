#!/usr/bin/env python3
from typing import List, Dict, Union, Optional

class CashRegister:
    def __init__(self, discount: int = 0):
        self._discount = 0
        self.discount = discount
        self.total: float = 0.0
        self.items: List[str] = []
        self.previous_transactions: List[Dict] = []
    
    @property
    def discount(self) -> int:
        return self._discount
    
    @discount.setter
    def discount(self, value: int) -> None:
        if isinstance(value, int) and 0 <= value <= 100:
            self._discount = value
        else:
            print(f"Error: '{value}' is not a valid discount. Must be integer 0-100.")
            self._discount = 0
    
    @property
    def item_count(self) -> int:
        """Return total number of items (including quantities)"""
        return len(self.items)
    
    @property
    def transaction_count(self) -> int:
        """Return number of transactions"""
        return len(self.previous_transactions)
    
    def add_item(self, item: str, price: float, quantity: int = 1) -> None:
        """
        Add item(s) to the register
        
        Args:
            item: Name of the item
            price: Price per unit
            quantity: Number of items (default: 1)
        """
        if not item or not isinstance(item, str):
            print("Error: Item must be a non-empty string")
            return
        
        if not isinstance(price, (int, float)) or price <= 0:
            print("Error: Price must be a positive number")
            return
        
        if not isinstance(quantity, int) or quantity < 1:
            print("Error: Quantity must be a positive integer")
            return
        
        self.total += price * quantity

        for _ in range(quantity):
            self.items.append(item)

        self.previous_transactions.append({
            'item': item,
            'price': price,
            'quantity': quantity,
            'subtotal': price * quantity
        })
        
        print(f"Added {quantity} x {item} @ ${price:.2f} = ${price * quantity:.2f}")
    
    def apply_discount(self) -> Optional[float]:
        """
        Apply discount to total
        
        Returns:
            Discount amount or None if no discount applied
        """
        if self.discount == 0:
            print("There is no discount to apply.")
            return None
        
        if self.total == 0:
            print("No items in cart. Cannot apply discount.")
            return None
        
        discount_amount = self.total * (self.discount / 100)
        self.total -= discount_amount

        self.total = round(self.total, 2)
        
        print(f"Discount applied: {self.discount}% off")
        print(f"After discount, the total comes to ${self.total:.2f}.")
        
        return discount_amount
    
    def void_last_transaction(self) -> bool:
        """
        Remove the last transaction
        
        Returns:
            True if transaction was voided, False otherwise
        """
        if not self.previous_transactions:
            print("No transactions to void.")
            return False
        
        last = self.previous_transactions.pop()

        for _ in range(last['quantity']):
            self.items.pop()
        
        self.total -= last['price'] * last['quantity']
        self.total = round(self.total, 2)
        
        print(f"Voided: {last['quantity']} x {last['item']} (${last['subtotal']:.2f})")
        print(f"New total: ${self.total:.2f}")
        
        return True
    
    def void_all_transactions(self) -> None:
        """Clear all transactions and reset register"""
        self.total = 0.0
        self.items = []
        self.previous_transactions = []
        print("All transactions voided. Register reset.")
    
    def get_receipt(self) -> str:
        """Generate a formatted receipt"""
        if not self.previous_transactions:
            return "No items purchased."
        
        receipt = "\n" + "=" * 40 + "\n"
        receipt += "          RECEIPT\n"
        receipt += "=" * 40 + "\n"
        
        for i, trans in enumerate(self.previous_transactions, 1):
            receipt += f"{i}. {trans['item']}\n"
            receipt += f"   {trans['quantity']} x ${trans['price']:.2f} = ${trans['subtotal']:.2f}\n"
        
        receipt += "-" * 40 + "\n"
        
        if self.discount > 0:
            discount_amount = self.total * (self.discount / (100 - self.discount))
            subtotal = self.total + discount_amount
            receipt += f"Subtotal: ${subtotal:.2f}\n"
            receipt += f"Discount ({self.discount}%): -${discount_amount:.2f}\n"
        
        receipt += f"TOTAL: ${self.total:.2f}\n"
        receipt += "=" * 40
        
        return receipt
    
    def __str__(self) -> str:
        """String representation of the register"""
        return f"CashRegister(total=${self.total:.2f}, items={self.item_count}, discount={self.discount}%)"
    
    def __repr__(self) -> str:
        return self.__str__()