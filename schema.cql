CREATE KEYSPACE IF NOT EXISTS ecommerce WITH replication = { 'class': 'NetworkTopologyStrategy', 'replication_factor': '1' } AND tablets = {'enabled': false};

CREATE TABLE ecommerce.product (
    id UUID,
    name TEXT,
    price FLOAT,
    img TEXT,
    PRIMARY KEY ()
);

CREATE TABLE ecommerce.cart (
    user_id TEXT,
    cart_id UUID,
    is_active BOOLEAN,
    PRIMARY KEY ()
);

CREATE TABLE ecommerce.cart_items (
    user_id TEXT,
    cart_id UUID,
    product_id UUID,
    product_quantity INT,
    PRIMARY KEY ()
) WITH cdc = {'enabled': true, 'preimage': true, 'postimage': true};
