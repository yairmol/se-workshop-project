import unittest
import threading as th
from domain.commerce_system.appointment import ShopOwner, ShopManager
from domain.commerce_system.shop import Shop
from domain.commerce_system.user import Subscribed


shop_dict = {"shop_name": "s1", "description": "desc"}


def run_parallel_test(f1, f2):
    t1, t2 = th.Thread(target=f1), th.Thread(target=f2)
    t1.start(), t2.start()
    t1.join(), t2.join()


class TestShopOwner(unittest.TestCase):

    def setUp(self):
        self.owner_sub = Subscribed("test sub")
        self.test_shop = self.owner_sub.open_shop(shop_dict)
        self.owner_app = self.owner_sub.get_appointment(self.test_shop)
        self.assertIsInstance(self.test_shop, Shop)
        self.assertEqual(self.test_shop.name, shop_dict["shop_name"])

    def test_open_shop(self):
        # check setup
        self.assertTrue(True)

    def test_add_appointment(self):
        new_sub = Subscribed("new sub")
        self.owner_sub.appoint_owner(new_sub, self.test_shop)
        self.assertIn(self.test_shop, new_sub.appointments)
        self.assertIsInstance(new_sub.appointments[self.test_shop], ShopOwner)

    def test_add_appointment_not_owner(self):
        new_sub = Subscribed("new sub")
        new_shop = Shop(**shop_dict)
        self.assertRaises(Exception, new_sub.appoint_owner, self.owner_sub, new_shop)

    def test_promote_appointment(self):
        new_sub = Subscribed("new sub")
        self.owner_sub.appoint_manager(new_sub, self.test_shop, [])
        self.assertIsInstance(new_sub.appointments[self.test_shop], ShopManager)
        self.owner_sub.promote_manager_to_owner(new_sub, self.test_shop)
        self.assertIn(self.test_shop, new_sub.appointments.keys())
        self.assertIsInstance(new_sub.appointments[self.test_shop], ShopOwner)
        new_shop = Shop(**shop_dict)
        self.assertRaises(Exception, self.owner_sub.appoint_owner, new_sub, new_shop)

    def test_remove_manager(self):
        new_sub = Subscribed("new sub")
        self.owner_sub.appoint_manager(new_sub, self.test_shop, [])
        self.owner_sub.un_appoint_manager(new_sub, self.test_shop)
        self.assertNotIn(self.test_shop, new_sub.appointments.keys())

    def remove_manager_parallel(self):
        def a(x):
            def f():
                new_sub = Subscribed("new sub")
                x.owner_sub.appoint_manager(new_sub, self.test_shop, [])
                x.owner_sub.un_appoint_manager(new_sub, self.test_shop)
                x.assertNotIn(self.test_shop, new_sub.appointments.keys())
        return a(self)

    def test_remove_manager_parallel(self):
        run_parallel_test(self.remove_manager_parallel(), self.remove_manager_parallel())

    def test_unappoint_from_non_appointer(self):
        new_sub = Subscribed("new sub")
        new_shop = Shop(**shop_dict)
        test_owner_2 = ShopOwner(new_shop)
        new_sub_2 = Subscribed("new sub 2")
        new_sub_2.appointments[new_shop] = test_owner_2
        new_sub_2.appoint_manager(new_sub, new_shop, [])
        # owner_sub is not an owner of new_shop
        self.assertRaises(Exception, self.owner_sub.un_appoint_manager, new_sub, new_shop)

    def test_remove_owner(self):
        new_sub = Subscribed("new sub")
        self.owner_sub.appoint_owner(new_sub, self.test_shop)
        self.owner_sub.un_appoint_owner(new_sub, self.test_shop)
        self.assertNotIn(self.test_shop, new_sub.appointments.keys())
        new_shop = Shop(**shop_dict)
        test_owner_2 = ShopOwner(new_shop)
        new_sub_2 = Subscribed("new sub 2")
        new_sub_2.appointments[new_shop] = test_owner_2
        new_sub_2.appoint_owner(new_sub, new_shop)
        self.assertRaises(Exception, self.owner_sub.un_appoint_owner, new_sub, new_shop)

    def test_wrong_owner(self):
        new_sub = Subscribed("new sub")
        new_sub2 = Subscribed("new sub 2")
        app2 = self.owner_app.appoint_owner(new_sub2)
        new_sub2.appointments[self.test_shop] = app2
        self.owner_sub.appoint_manager(new_sub, self.test_shop, [])
        self.assertRaises(Exception, new_sub2.un_appoint_manager, new_sub, self.test_shop)

    def test_cascade_owner_unappointment(self):
        new_sub = Subscribed("new sub2")
        new_sub2 = Subscribed("new sub3")
        new_sub3 = Subscribed("new sub4")
        self.owner_sub.appoint_owner(new_sub, self.test_shop)
        new_sub.appoint_owner(new_sub2, self.test_shop)
        new_sub.appoint_owner(new_sub3, self.test_shop)
        self.owner_sub.un_appoint_owner(new_sub, self.test_shop)
        assert self.test_shop not in new_sub3.appointments.keys()
