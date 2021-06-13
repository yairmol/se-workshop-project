import init_generator as ig

NUM_USERS = int(3e2)
NUM_SHOPS = int(1e2)
NUM_TRANSACTIONS = int(1e3)
NUM_PRODUCTS_PER_SHOP = int(1e1)
print(NUM_USERS, NUM_SHOPS, NUM_TRANSACTIONS, NUM_PRODUCTS_PER_SHOP)


ig.generate_init(
    "load_test_init_alot.json",
    [f"u{i}" for i in range(NUM_USERS)],
    *[ig.enter(f"u{i}") for i in range(NUM_USERS)],
    *[ig.register(f"u{i}", f"user{i}", "password") for i in range(NUM_USERS)],
    *[ig.login(f"u{i}", f"user{i}", "password") for i in range(NUM_USERS)],
    *[ig.open_shop(f"u{i}", f"Armani {i}", f"Armani ze asur {i}", add_ref=f"s{i}") for i in range(NUM_SHOPS)],
    *[
        ig.add_product_to_shop(
            f"u{i}",
            f"s{i}",
            f"Bamba {NUM_PRODUCTS_PER_SHOP * i + j}",
            "its osem",
            price=30,
            quantity=20,
            categories=["snacks"],
            add_ref=f"p{NUM_PRODUCTS_PER_SHOP * i + j}"
        )
        for j in range(NUM_PRODUCTS_PER_SHOP) for i in range(NUM_SHOPS)
    ],
    *[
        ig.purchase_product(f"u{NUM_SHOPS + i}", f"s{i}", f"p{i * NUM_PRODUCTS_PER_SHOP + j}", 1, {}, {})
        for i in range(NUM_SHOPS)
        for j in range(NUM_PRODUCTS_PER_SHOP)
    ]
)
