from functools import reduce
from typing import List

from domain.commerce_system.product import Product

SIMILARITY_THRESHOLD = 0.3


class Filter:
    @staticmethod
    def from_dict(prod_filter: dict):
        return {
            "price_range": PriceRangeFilter
        }[prod_filter["type"]](prod_filter)

    def apply(self, product_list):
        raise NotImplementedError()


class PriceRangeFilter(Filter):
    def __init__(self, prod_filter: dict):
        self._from = prod_filter["from"]
        self._to = prod_filter["to"]

    def apply(self, product_list: List[Product]):
        return list(filter(lambda p: self._from <= p.price <= self._to,
                           product_list))


def search(
        products: List[Product], product_name: str = None, keywords: List[str] = None,
        categories: List[str] = None, filters: List[Filter] = None
) -> List[Product]:
    filtered_products = products
    if filters:
        filtered_products = search_by_filters(products, filters)
    if product_name:
        filtered_products = search_by_product_name(filtered_products, product_name)
    if keywords:
        filtered_products = search_by_keywords(products, keywords)
    if categories:
        filtered_products = search_by_categories(products, categories)
    return filtered_products


def search_by_filters(products, filters):
    for prod_filter in filters:
        products = prod_filter.apply(products)
    return products


def search_by_product_name(products: List[Product], product_name):
    return list(filter(lambda p: is_similar_words(p.name, product_name), products))


def search_by_keywords(products: List[Product], keywords: List[str]):
    # TODO: implement, priority: low
    return products


def is_similar_words(s1: str, s2: str) -> bool:
    return (levenshtein_distance(s1, s2) / max(len(s1), len(s2))) <= SIMILARITY_THRESHOLD


def search_by_categories(products: List[Product], categories: List[str]):
    def filtering(prod_categories):
        return any(map(lambda pc:  # There exists a product category pc such that
                       any(map(lambda c: is_similar_words(pc, c), categories)),  # There exists a category similar to pc
                       prod_categories))

    return list(filter(lambda p: filtering(p.categories), products))


# from stack_overflow: https://stackoverflow.com/questions/2460177/edit-distance-in-python
def levenshtein_distance(s1: str, s2: str):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
