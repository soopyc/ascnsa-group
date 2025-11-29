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
docker compose up -d
```

After starting a new container, you can verify that the database container is running correctly with:

```powershell
docker ps
```

You should see an output that includes a container with a name like `ascnsa-group-db-1`. This confirms the database server is up and running.

---

### Step 2: Create Schema and Add Data

Execute our SQL scripts to setup the database structure and fill in test data.

These commands must be run in the correct order.

1.  Create the table structures:
    
    *This command executes the `create database.sql` script, you can find the script in `...\ascnsa-group\database setup\`*

    ```powershell
    Get-Content "database setup/create database.sql" | docker exec -i ascnsa-group-db-1 mariadb -uuser -puserresu library_app
    ```

2.  Add the sample test data:
    *This command executes the `add test data.sql` script*, you can find the script in `...\ascnsa-group\database setup\`*

    ```powershell
    Get-Content "database setup/add test data.sql" | docker exec -i ascnsa-group-db-1 mariadb -uuser -puserresu library_app
    ```

If these commands run without any error text, your database has been successfully built and populated.

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