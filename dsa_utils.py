# DSA utilities for the chatbot
# Using data structures and algorithms

from collections import defaultdict

class ReviewAggregator:
    def __init__(self):
        self.products = defaultdict(list)  # Dict as hash table

    def add_review(self, product, review):
        self.products[product].append(review)

    def get_reviews(self, product):
        return self.products.get(product, [])

    def sort_reviews_by_rating(self, product, descending=True):
        reviews = self.get_reviews(product)
        # Use sorting algorithm (Python's sort is Timsort)
        return sorted(reviews, key=lambda x: x['rating'], reverse=descending)

    def search_reviews(self, product, keyword):
        reviews = self.get_reviews(product)
        # Linear search
        return [r for r in reviews if keyword.lower() in ' '.join(r['points']).lower()]

# Sample usage (commented out)
# aggregator = ReviewAggregator()
# aggregator.add_review("Laptop A", {"reviewer": "User1", "rating": 5, "points": ["Great performance", "Long battery life"]})
# aggregator.add_review("Laptop A", {"reviewer": "User2", "rating": 4, "points": ["Good value", "Fast boot"]})