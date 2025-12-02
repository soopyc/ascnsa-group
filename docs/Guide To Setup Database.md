## Prerequisites

- Git
- Docker Desktop
- Terminal (cmd, powershell, bash)

## Database Info

```
database: library_app
username: user
password: userresu
```

## Setup

### Step 1: Enter the correct folder

Make sure your terminal is in the project folder. On windows, it should be something like:

```
...\ascnsa-group>
```

---

### Step 2: Start the Docker Container For Database

Stop and remove previous container (Optional)

```powershell
docker compose down -v
```

Start a new container

```powershell
docker compose build
docker compose up -d
```

After starting a new container, you can verify that the database container is running correctly with:

```powershell
docker ps
```

You should see an output that includes a container with a name like `ascnsa-group-db-1`. This confirms the database server is up and running.

---

### Step 2: Create Schema and Add Data (OPTIONAL, SETUP SHOULD BE AUTOMATIC)

Normally, when you run Docker for the first time, the database schema and test data are created automatically using the scripts in `database setup`:

- `01-create-schema.sql` – creates the tables
- `02-add-test-data.sql` – inserts sample data

If you need to re-run them manually (for example to reset the data), you can execute them in this order:

1.  Create the table structures:
    
    ```powershell
    Get-Content "database setup/01-create-schema.sql" | docker exec -i ascnsa-group-db-1 mariadb -uuser -puserresu library_app
    ```

2.  Add the sample test data:

    ```powershell
    Get-Content "database setup/02-add-test-data.sql" | docker exec -i ascnsa-group-db-1 mariadb -uuser -puserresu library_app
    ```

If these commands run without any error text, your database has been successfully built and populated (or reset).

---

### Step 3: Verify The Database

Test if the database has setup correctly.

1.  Log into the database:

    ```powershell
    docker exec -it ascnsa-group-db-1 mariadb -uuser -puserresu library_app
    ```

    If done correctly, your terminal prompt should change to 
    `MariaDB [library_app]>`

2.  Run test queries:

    *   Run any command (such as `SELECT * FROM Books`) to verify if your setup is correct.

3.  Exit the database CLI:
    Once you're satisfied, use `exit;` to exit database CLI.

    ```sql
    exit;
    ```

---

## Troubleshooting 

*   `The '<' operator is reserved...` (Powershell):
    *   Please use the provided command in this guide to setup the database.

*   `command not found: mysql` error:
    *   Our database container is `mariadb`, so the command-line tool is named `mariadb`, not `mysql`. Ensure all your `docker exec` commands use `mariadb`.

*   How do I completely reset my database?
    *   If you want to start over from a completely clean slate, run the following command. This will permanently delete the existing database
    ```powershell
    docker compose down -v
    ```