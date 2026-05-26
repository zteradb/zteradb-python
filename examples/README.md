# Technical Onboarding: Pre-Requisite Schema Setup

This guide walks you through configuring the database blueprint required to run our custom engine query examples.
You will build four core schemas directly within your developer dashboard.

## 📋 Before You Begin
1. Log into your **ZTeraDB Dashboard**.
2. Note the strict schema dependency chain: **user** ➡️ **user_profile** and **product** ➡️ **order** (target schemas must exist before creating foreign key fields).
3. Ensure the exact cases for types (e.g., `varchar`, `boolean`, `decimal`) match your engine's mapping parameters.

Please execute these **3 Steps** in the exact order listed below to ensure all cross-schema foreign key relations are resolved correctly.

---

## Step 1: Understand the Schema Architecture

Before entering data into the dashboard, visualize how the schemas connect to one another through your dashboard's relation fields:

```text
+------------------+               +-----------------------+
|       user       |1             1|     user_profile      |
+------------------+---------------+-----------------------+
| id (PK)          |               | id (PK)               |
| email            |               | user [FK -> user]     |
| password         |               | address               |
| status           |               | profile_image         |
+------------------+---------------+-----------------------+
          |
          | 1
          |
          | 0..*
+------------------+
|      order       |
+------------------+
| id (PK)          |
| status           |
| create_date      |
| update_date      |
| user [FK]        |------0..*-----+
| product [FK]     |               |
+------------------+               | 1
                                   |
                            +---------------+
                            |    product    |
                            +---------------+
                            | id (PK)       |
                            | name          |
                            | description   |
                            | quantity      |
                            | price         |
                            | create_date   |
                            | update_date   |
                            | status        |
                            +---------------+
```

The `order` schema acts as a central transaction ledger, using native Foreign Key fields to link back to a single `user` and a single `product`.
Meanwhile, `user_profile` maintains a clean 1:1 relationship with the primary user schema.

* **user ─── user_profile** (One-to-One Relation)
    * Linked by: `user_profile.user` (Foreign key field targeting `user`)
    
* **user ─── order** (One-to-Many Relation)
    * Linked by: `order.user` (Foreign key field targeting `user`)
    
* **product ─── order** (One-to-Many Relation)
    * Linked by: `order.product` (Foreign key field targeting `product`)


---

## Step 2: Build the Schemas (Step-by-Step)

Navigate to your **Schema Engine Dashboard** and create the schemas sequentially. 

### 1. Create the `user` Schema
*This schema handles authentication credentials and basic account visibility flags.*

#### Schema Fields
| NAME | TYPE | LENGTH | DEFAULT | COMMENT | EXTRA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | Auto increment integer | 10 | *None* | Unique internal user identifier | primary key, not null |
| **email** | varchar | 255 | *None* | Primary login identifier | not null, unique |
| **password** | varchar | 255 | *None* | Sized to support modern secure hash strings | not null |
| **status** | boolean | *None* | true | Tracks if account is active or disabled | not null |

---

### 2. Create the `user_profile` Schema
*This schema stores extended user metadata. It requires the `user` schema to exist first.*

#### Schema Fields
| NAME | TYPE | LENGTH | DEFAULT | COMMENT | EXTRA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | Auto increment integer | 10 | *None* | Unique profile identifier | primary key, not null |
| **address** | varchar | 255 | *None* | Physical delivery destination | not null |
| **profile_image** | varchar | 255 | *None* | Path or URL to user avatar image | |

#### Schema Relation Fields
| FIELD NAME | TARGET SCHEMA | TYPE | ON DELETE | COMMENT | EXTRA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **user** | user | Foreign key field | Delete this schema | Ties the profile metadata to a specific user | |

---

### 3. Create the `product` Schema
*This schema serves as your application's master catalog, keeping track of active item pricing and stock levels.*

#### Schema Fields
| NAME | TYPE | LENGTH | DEFAULT | COMMENT | EXTRA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | Auto increment integer | 10 | *None* | Unique internal product identifier | primary key, not null |
| **name** | varchar | 255 | *None* | Public-facing name of the item | not null |
| **description** | text | *None* | *None* | Thorough item details and specifications | |
| **quantity** | small integer | 3 | 0 | Available physical inventory units | not null |
| **price** | decimal | 10,2 | *None* | Currency field configured for accurate math | not null |
| **create_date** | datetime field | *None* | *None* | Auto-generated timestamp on creation | auto_now_add |
| **update_date** | datetime field | *None* | *None* | Auto-updated timestamp on modification | auto_now |
| **status** | boolean field | *None* | true | Toggles product visibility on the storefront | |

---

### 4. Create the `order` Schema
*This schema tracks individual transactions. It requires both the `user` and `product` schemas to exist first.*

#### Schema Fields
| NAME | TYPE | LENGTH | DEFAULT | COMMENT | EXTRA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | Auto increment integer | 10 | *None* | Master checkout invoice tracker | primary key, not null |
| **status** | varchar | 50 | 'Pending' | Handles lifecycle processing states | not null |
| **create_date** | datetime field | *None* | *None* | Auto-generated timestamp of checkout | auto_now_add |
| **update_date** | datetime field | *None* | *None* | Auto-updated timestamp of status shift | auto_now |

#### Schema Relation Fields
| FIELD NAME | TARGET SCHEMA | TYPE | ON DELETE | COMMENT | EXTRA |
| :--- |:--------------| :--- | :--- | :--- | :--- |
| **user** | user          | Foreign key field | Delete this schema | References the buyer who initiated checkout | |
| **product** | product       | Foreign key field | Delete this schema | References the specific item purchased | |

---

## Step 3: Verify and Troubleshoot

Before jumping into the code query samples, execute this quick health check to ensure your environment is configured perfectly:

* **Dependency Check:** Did you map the Relation Fields using the explicit **Foreign key field** type option? If done correctly, your custom query engine will automatically resolve join requests across these nodes.
* **Cascading Logic Test:** The `ON DELETE` rules are set to **Delete this schema** (Cascade). If you wipe out a mock user account during testing, the custom engine will safely clean up the dependent `user_profile` and `order` documents automatically, keeping your sandboxed environment free of broken references.

**You are now fully prepared.** You can move on to the next section of the documentation to execute custom data queries against this structural layout.
