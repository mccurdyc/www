---
title: Getting Started Locally with HashiCorp Vault and a PostgreSQL Storage Backend
description: ""
author: "Colton J. McCurdy"
date: 2019-11-27
post-tags: ["vault", "hashicorp", "secrets", "2019"]
posts: ["Getting Started Locally with HashiCorp Vault and a PostgreSQL Storage Backend"]
---

## Motivation

HashiCorp has really great documentation for its products. However, for someone like
myself who is new to a product, specifically Vault in this case, it is difficult
to know where to look in their documentation.

They have a great way to familiarize yourself with development version of Vault
on their [learn subdomain](https://learn.hashicorp.com/vault). I wanted to use
a non-development version of Vault. Specifically what I was interested in doing,
was connecting Vault to a PostgreSQL `storage` backend.

### Initial Setup

Setup your shell with `alias`es and environment variables

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export DB_USER="user"
export DB_NAME="secrets"
export DB_PASSWORD="pw"
export PG_CONNECTION_URL="postgresql://${DB_USER}:${DB_PASSWORD}@127.0.0.1:5432/${DB_NAME}?sslmode=disable"
alias psqlconn="psql -h 127.0.0.1 -U ${DB_USER} -p 5432 -W ${DB_NAME}"
```

_Note:_ You will need to set these in every new shell that you open.

Make sure that you don't already have a PostgreSQL running. Also, it is important
to note that the PostgreSQL Docker image is configured using environment variables
_on first startup_. Make sure you clear your local Docker image cache of the PostgreSQL
image.

_Note:_ I ran into connection issues using `localhost` instead of `127.0.0.1` as the connection URL, even when it worked
when connecting directly via `pslconn`.


### Configuring your PostgreSQL Storage Backend
To read more about the PostgreSQL Docker image, refer to the official [documentation](https://hub.docker.com/_/postgres).

+ Start PostgreSQL in a Docker container

```bash
docker run \
  --rm \
  --name psql \
  -p 5432:5432 \
  -e POSTGRES_USER="${DB_USER}" \
  -e POSTGRES_PASSWORD="${DB_PASSWORD}" \
  -e POSTGRES_DB="${DB_NAME}" \
  -d postgres
```

+ Connect to the running PostgreSQL container

```bash
$ psqlconn

Password: pw
psql (11.5, server 12.1 (Debian 12.1-1.pgdg100+1))
WARNING: psql major version 11, server major version 12.
         Some psql features might not work.
Type "help" for help.

secrets=#
```

+ Create a database `SUPERUSER` role for Vault to use

```sql
CREATE ROLE vault WITH SUPERUSER LOGIN CREATEROLE;
```

+ Create a table for storing the encrypted secrets since this step is not done automatically by Vault

```sql
CREATE TABLE vault_kv_store (
  parent_path TEXT COLLATE "C" NOT NULL,
  path        TEXT COLLATE "C",
  key         TEXT COLLATE "C",
  value       BYTEA,
  CONSTRAINT pkey PRIMARY KEY (path, key)
);

CREATE INDEX parent_path_idx ON vault_kv_store (parent_path);
```

_Note:_ [Official Vault documentation on this topic](https://www.vaultproject.io/docs/configuration/storage/postgresql.html)

### Configuring Vault to Use the Storage Backend
+ Create a Vault Server Configuration File

```bash
$ sudo cat /etc/vault.hcl

storage "postgresql" {
  connection_url = "postgresql://user:pw@127.0.0.1:5432/secrets?sslmode=disable"
}

path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = "true"
}

disable_mlock = true

log_level = "trace"
```

+ Start the Vault Server

_Note:_ To check the status of Vault at any time, you can run `vault status`. The important
thing to look for is that, at this point, the Vault server should _not_ yet be initialized.

```bash
vault server -config=/etc/vault.hcl
```

+ Initialize Vault

```bash
vault operator init
```

Now, you should see your Unseal Keys and `vault status` should show that the Vault server is initialized.

```bash
Unseal Key 1: eTg5Hdqbs2UpUAE4DD0t+HY0nZ51961svAW0qxRllaaI
Unseal Key 2: jXKwRX41pfRsPzpWZgN0zhqoid9M/rkKKZMH+EjvNt3E
Unseal Key 3: Sf9Phghp7brh+iU3R17vk42GoQ41ia5AReII0sBwelYk
Unseal Key 4: N9eNdz4ZdsYlODa+gVRHzbvZ9YeB33N/fa+qeSP6IXLc
Unseal Key 5: 4mtkNKLvew/eyRBoX6JD/Rk4lxFZGgk86f/CdoMicKMW

Initial Root Token: s.xpmoaOWlDESk5ZQU4yBlzLCR

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated master key. Without at least 3 key to
reconstruct the master key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.
```

+ Unseal Vault to Enable Secrets

You will need to use the Unseal Keys returned from running `vault operator init`.
The values above will not work for you.

```bash
$ vault operator unseal

Unseal Key (will be hidden): eTg5Hdqbs2UpUAE4DD0t+HY0nZ51961svAW0qxRllaaI
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    1/3
Unseal Nonce       f1e46ec4-6877-241e-b994-f3d6222595d2
Version            1.3.0
HA Enabled         false

$ vault operator unseal
Unseal Key (will be hidden): jXKwRX41pfRsPzpWZgN0zhqoid9M/rkKKZMH+EjvNt3E
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    2/3
Unseal Nonce       f1e46ec4-6877-241e-b994-f3d6222595d2
Version            1.3.0
HA Enabled         false

$ vault operator unseal
Unseal Key (will be hidden): Sf9Phghp7brh+iU3R17vk42GoQ41ia5AReII0sBwelYk
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    5
Threshold       3
Version         1.3.0
Cluster Name    vault-cluster-428acf8b
Cluster ID      16c58b38-29f5-d320-a87a-7daeaeef83c3
HA Enabled      false
```

+ Enable `kv` Secrets

```bash
VAULT_TOKEN=s.xpmoaOWlDESk5ZQU4yBlzLCR vault secrets enable -path=secret kv
```

+ Write your first secret!

```bash
VAULT_TOKEN=s.xpmoaOWlDESk5ZQU4yBlzLCR vault kv put secret/creds passcode=my-long-passcode
```

+ Read the key-value secret

```bash
VAULT_TOKEN=s.xpmoaOWlDESk5ZQU4yBlzLCR vault kv get secret/creds
```

_Note:_ [The official documentation for storing `kv` secrets](https://www.vaultproject.io/docs/commands/kv/index.html)
