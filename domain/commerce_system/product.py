from __future__ import annotations
import threading
from typing import List, Dict, TypeVar, Type
from enum import Enum, auto

from data_model import ProductModel as Pm, PurchaseTypes as Pt
from domain.commerce_system.category import Category


class PurchaseType:
    __nextid = 1
    __nextid_lock = threading.Lock()

    def __init__(self, product: Product, **kwargs):
        self.product = product
        with PurchaseType.__nextid_lock:
            self.id = PurchaseType.__nextid
            PurchaseType.__nextid += 1

    def can_purchase(self, **kwargs) -> bool:
        raise NotImplementedError()

    def get_price(self, **kwargs) -> float:
        raise NotImplementedError()

    def to_dict(self, **kwargs) -> dict:
        return {"id": self.id}


T_PT = TypeVar('T_PT', bound=PurchaseType)


class Product:
    __product_id = 1
    __id_lock = threading.Lock()

    def __init__(
            self, product_name: str, price: float, description: str = "",
            quantity: int = 0, categories: List[str] = None, shop_id=None, image_url=None
    ):
        if categories is None:
            categories = []
        with Product.__id_lock:
            self.product_id = Product.__product_id
            Product.__product_id += 1
        self.product_name = product_name
        self.price = price
        self.description = description
        self._quantity = 0
        self.set_quantity(quantity)
        self.categories: List[Category] = [Category(name) for name in categories]
        self.shop_id = shop_id
        self.image_url = image_url
        buy_now = BuyNow(self)
        self.purchase_types: Dict[int, PurchaseType] = {buy_now.id: buy_now}

    def to_dict(self, include_purchase_types=True) -> dict:
        ret = {
            Pm.PRODUCT_ID: self.product_id,
            Pm.PRODUCT_NAME: self.product_name,
            Pm.PRODUCT_DESC: self.description,
            Pm.PRICE: self.price,
            Pm.QUANTITY: self._quantity,
            Pm.CATEGORIES: [category.name for category in self.categories],
            Pm.SHOP_ID: self.shop_id,
        }
        if include_purchase_types:
            ret[Pm.PURCHASE_TYPES] = [pt.to_dict() for pt in self.purchase_types.values()]
        return ret

    def set_quantity(self, new_quantity):
        assert new_quantity >= 0, "product quantity must be non-negative"
        self._quantity = new_quantity
        return True

    def get_quantity(self):
        return self._quantity

    def get_category_names(self):
        return [category.name for category in self.categories]

    def add_purchase_type(self, purchase_type_info: dict) -> PurchaseType:
        ptype = purchase_type_info[Pt.PURCHASE_TYPE]
        purchase_type_info.pop(Pt.PURCHASE_TYPE)
        new_ptype = purchase_types_factory(ptype, self, **purchase_type_info)
        self.purchase_types[new_ptype.id] = new_ptype
        return new_ptype

    def get_purchase_type_of_type(self, purchase_type: Type[T_PT], not_found_message: str = "") -> T_PT:
        ret = [pt for pt in self.purchase_types.values() if isinstance(pt, purchase_type)]
        assert len(ret) > 0, not_found_message
        return ret[0]

    def add_price_offer(self, username: str, offer: float) -> bool:
        purchase_offer_type = self.get_purchase_type_of_type(PurchaseOfferType)
        return purchase_offer_type.offer_price(username, offer)

    def reply_price_offer(self, offer_maker: str, action: str) -> bool:
        assert action in [Pt.APPROVE, Pt.REJECT], "bad action"
        purchase_offer_type = self.get_purchase_type_of_type(PurchaseOfferType)
        if action == Pt.APPROVE:
            purchase_offer_type.approve(offer_maker)
        elif action == Pt.REJECT:
            purchase_offer_type.reject(offer_maker)
        return True

    def get_price(self, purchase_type_type: Type[T_PT], **kwargs) -> float:
        purchase_type = self.get_purchase_type_of_type(purchase_type_type)
        return purchase_type.get_price(**kwargs)

    def can_purchase(self, purchase_type_type: Type[T_PT], **kwargs) -> bool:
        purchase_type = self.get_purchase_type_of_type(purchase_type_type)
        return purchase_type.can_purchase(**kwargs)

    def get_purchase_type(self, purchase_type_id: int) -> PurchaseType:
        return self.purchase_types[purchase_type_id]

    def set_purchase_types(self, purchase_types: list):
        to_remove = []
        for ptid, pt in self.purchase_types.items():
            if all("id" not in other_pt or other_pt["id"] != ptid for other_pt in purchase_types):
                to_remove.append(ptid)
        for ptid in to_remove:
            self.purchase_types.pop(ptid)
        for pt in purchase_types:
            if "id" not in pt or all(other_pt != pt["id"] for other_pt in self.purchase_types.keys()):
                self.add_purchase_type(pt)

    def get_offers(self) -> List[PurchaseOffer]:
        try:
            pt_offer = self.get_purchase_type_of_type(PurchaseOfferType)
            return list(pt_offer.offers.values())
        except AssertionError:
            return []

    def set_categories(self, categories):
        self.categories = [Category(c) for c in categories]


class ProductInBag:
    def __init__(self, product: Product, amount: int, purchase_type: T_PT, **purchase_type_args):
        self.product = product
        self.amount = amount
        self.purchase_type = purchase_type
        self.purchase_type_args = purchase_type_args


class BuyNow(PurchaseType):

    def can_purchase(self, **kwargs) -> bool:
        return True

    def get_price(self, **kwargs) -> float:
        return self.product.price

    def to_dict(self, **kwargs) -> dict:
        ret = super().to_dict(**kwargs)
        ret.update({Pt.PURCHASE_TYPE: Pt.BUY_NOW, Pt.FOR_SUBS_ONLY: False})
        return ret


class OfferState(Enum):
    WAITING = auto()
    APPROVED = auto()
    REJECTED = auto()


class PurchaseOffer:
    def __init__(self, offer_maker: str, offer: float):
        self.offer_maker = offer_maker
        self.offer = offer
        self.offer_state: OfferState = OfferState.WAITING

    def approve(self):
        self.offer_state = OfferState.APPROVED

    def reject(self):
        self.offer_state = OfferState.REJECTED

    def to_dict(self) -> dict:
        return {
            Pt.OFFER_MAKER: self.offer_maker,
            Pt.OFFER: self.offer,
            Pt.STATE: self.offer_state.name
        }


class PurchaseOfferType(PurchaseType):

    def __init__(self, product: Product):
        super().__init__(product)
        # map between usernames and purchase offers
        self.offers: Dict[str, PurchaseOffer] = {}

    def offer_price(self, offer_maker: str, offer: float) -> bool:
        # we can allow re offers
        # assert offer_maker not in self.offers  self.offers[offer_maker].offer_state == OfferState.REJECTED,\
        #     "Can't make two simultaneous offers for the same product"
        self.offers[offer_maker] = PurchaseOffer(offer_maker, offer)
        return True

    def approve(self, offer_maker: str):
        assert offer_maker in self.offers, f"There is no existing offer for {offer_maker}"
        self.offers[offer_maker].approve()

    def reject(self, offer_maker: str):
        assert offer_maker in self.offers, f"There is no existing offer for {offer_maker}"
        self.offers[offer_maker].reject()

    def can_purchase(self, offer_maker: str) -> bool:
        assert offer_maker in self.offers, "You must first make an offer before you purchase"
        offer_state = self.offers[offer_maker].offer_state
        if offer_state != OfferState.APPROVED:
            error_message = (
                "offer must be approved before purchasing" if offer_state == OfferState.WAITING else
                "offer was rejected"
            )
            raise AssertionError(error_message)
        return True

    def get_price(self, offer_maker) -> float:
        assert offer_maker in self.offers, f"There is no existing offer for {offer_maker}"
        return self.offers[offer_maker].offer

    def to_dict(self, include_offers=False, **kwargs) -> dict:
        ret = super().to_dict(**kwargs)
        ret.update({Pt.PURCHASE_TYPE: Pt.OFFER, Pt.FOR_SUBS_ONLY: True})
        if include_offers:
            ret.update({"offers": [offer.to_dict() for offer in self.offers.values()]})
        return ret


ptype_str_to_ptype = {
    Pt.BUY_NOW: BuyNow,
    Pt.OFFER: PurchaseOfferType
}


def purchase_types_factory(ptype: str, product: Product, **ptype_info):
    assert ptype in ptype_str_to_ptype, "invalid purchase type"
    return ptype_str_to_ptype[ptype](product, **ptype_info)
