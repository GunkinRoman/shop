\set  user  `echo  ${SOCIAL_NETWORK_USER}`
\set  pass  `echo  "'${SOCIAL_NETWORK_USER_PASSWORD}'"`
\set  db_name  `echo  ${SOCIAL_NETWORK_DB_NAME}`

CREATE DATABASE :db_name;

\c :db_name;

CREATE USER :user WITH ENCRYPTED PASSWORD :pass SUPERUSER;

CREATE TABLE acc_role(
    "id" BIGSERIAL PRIMARY KEY,
    "acc_id" BIGINT NOT NULL,
    "role" VARCHAR(20) NOT NULL
);


CREATE TABLE account(
    "id" BIGSERIAL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL,
    "first_name" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(100) NULL,
    "passw" VARCHAR(100) NULL,
    "mail" VARCHAR(100) NOT NULL,
    "mobile_telephone" CHAR(13) NOT NULL,
    "address" CHAR(100) NOT NULL
);

CREATE TABLE product(
    "id" BIGSERIAL PRIMARY KEY,
    "article" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "cost" DECIMAL(8, 2) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "photo" VARCHAR(255) NOT NULL,
    "discount" DECIMAL(1, 2) NOT NULL,
    "quantity" BIGINT NOT NULL,
    "category" VARCHAR(100) NOT NULL
);

CREATE TABLE product_in_cart(
    "id" BIGSERIAL PRIMARY KEY,
    "acc_id" BIGINT NOT NULL,
    "product" BIGINT NOT NULL,
    "quantity" BIGINT NOT NULL
);

CREATE TABLE orders(
    "id" BIGSERIAL PRIMARY KEY,
    "acc_id" BIGINT NOT NULL,
    "cost" DECIMAL(8, 2) NOT NULL,
    "paid" BOOLEAN NOT NULL
);

CREATE TABLE products_order(
    "id" BIGSERIAL PRIMARY KEY,
    "order_id" BIGINT NOT NULL,
    "product" BIGINT NOT NULL,
    "quantity" BIGINT NOT NULL
);

ALTER TABLE
    orders ADD CONSTRAINT "orders_acc_id_foreign"
     FOREIGN KEY("acc_id") REFERENCES account("id");
ALTER TABLE
    product_in_cart ADD CONSTRAINT "product_in_cart_product_foreign" 
    FOREIGN KEY("product") REFERENCES product("id");
ALTER TABLE
    acc_role ADD CONSTRAINT "role_acc_id_foreign" FOREIGN KEY("acc_id")
     REFERENCES account("id");
ALTER TABLE
    products_order ADD CONSTRAINT "products_order_product_foreign"
     FOREIGN KEY("product") REFERENCES product("id");
ALTER TABLE
    products_order ADD CONSTRAINT "products_order_order_id_foreign"
     FOREIGN KEY("order_id") REFERENCES orders("id");
ALTER TABLE
    product_in_cart ADD CONSTRAINT "product_in_cart_acc_id_foreign"
     FOREIGN KEY("acc_id") REFERENCES account("id");