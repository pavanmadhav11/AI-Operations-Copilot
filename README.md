# AI Operations Copilot

AI Operations Copilot is a student project for viewing warehouse stock, asking stock questions in plain language, and adding products to inventory.

## Role structure

| Role | Stock access | Add inventory item | Change stock using the Stock Assistant | Manage account roles |
| --- | --- | --- | --- | --- |
| Employee | View | No | No | No |
| Manager | View | Yes | Yes | No |
| Admin | View | Yes | Yes | Yes |

The backend checks permissions on each protected API route. Hiding a link in the frontend is only for navigation; it is not the permission check.

Each account sees its own chat history, uploaded document list, dashboard activity, and reports. Admins can view system-wide analytics and reports. PDF and spreadsheet uploads are limited to 10 MB, and expanded `.xlsx` workbooks are limited to 50 MB.

## Admin setup

New registrations always receive the employee role. After registering and confirming the intended account, promote it from the project shell with `docker compose exec backend python -m app.bootstrap_admin --email admin@example.com`. This command requires local access to the backend container; the public registration route cannot grant admin access.

An admin can open **User Roles** to give accounts the employee, manager, or admin role. The system does not allow the last admin account to be demoted.

## Monthly business dataset

After the database is running, add the Andhra Pradesh inventory dataset with `docker compose exec backend python -m app.seed_business_data --confirm-business-data`. It covers the latest 30 days and includes 18 products, four stores, stock movement history, expiry batches, conversations, daily receipt PDFs, a monthly sales workbook, supplier quotations, purchase drafts, recommendations, and a pending manager action. Generated files are saved under `backend/business_data/`.

Set these private Render environment variables before creating or updating role accounts. The manager and employee password values should be the credentials provided for the presentation. Keep their values out of source control.

```text
PRESENTATION_PASSWORD
PRESENTATION_MANAGER_PASSWORD
PRESENTATION_EMPLOYEE_PASSWORD
```

`PRESENTATION_PASSWORD` is used only if the database needs a new administrator account. The other two variables update the manager and employee accounts during startup. The existing administrator account is preserved.

`$env:PRESENTATION_PASSWORD="use-a-private-password-of-at-least-12-characters"`

The seeder preserves the existing administrator account and sets the manager and employee accounts to these addresses:

| Role | Email |
| --- | --- |
| Admin | Existing administrator account |
| Manager | `abhiram_manager@gmail.com` |
| Employee | `jeevan_employee@gmail.com` |

Existing user history and stock quantities are retained. Known earlier Northstar records are renamed to the Andhra Pradesh business names. Repeat runs do not duplicate the monthly dataset and keep the manager and employee login accounts set to the addresses above.

## Stock features

- Every signed-in user can view inventory, stock movement history, and expiry alerts.
- The home page shows low-stock alerts in a five-row scrolling window. Each alert explains estimated days remaining and suggests a transfer or reorder quantity.
- Managers and admins can add products, record lot batches, prepare transfers, and ask the Stock Assistant to update a quantity.
- Managers and admins can create warehouse locations from the **Warehouses** page. Create at least one warehouse before adding inventory.
- Stock changes show a preview and require a confirmation. The system records the request, generated SQL or transfer plan, decision, and stock movement.
- Managers can review their own actions. Admins can review actions across all users and manage user roles.
- Batch records include a lot code and expiration date. Managers and admins can write off expired lots, which also reduces warehouse stock and creates a movement record.
- Inventory items can store average daily demand and supplier lead time. The stockout estimate is quantity divided by the entered average daily demand.
- The transfer suggestion checks for stock above the reorder threshold at another warehouse. If available surplus is not enough, it suggests transferring what it can and ordering the remainder.
- Chat answers based on uploaded PDFs cite a source page; answers based on spreadsheets cite a sheet.
- Excel uploads show common data checks. Managers and admins can use a workbook as sales history when it has product, quantity, and date columns. The app calculates average units sold per day across the date range and updates demand estimates for matching products.
- Applying a sales workbook also imports dated sales records. The SQL Generator can rank products by units sold, calculate total units sold for a selected period, and show a daily sales trend.
- Managers and admins can extract supplier details from a PDF quote, correct the extracted fields, and save an editable purchase order draft. The draft is not sent to the supplier.
- The notification bell collects active low-stock, expiry, pending-action, and purchase-draft alerts. Recommendation outcome cards report feedback, transfer/reorder acceptance, purchase drafts, and expired units written off.

The recommendations use simple inventory rules and entered sales history; they are not a trained demand forecasting model. A reorder suggestion or purchase order draft does not send an order to a supplier.

## Project evaluation idea

Use the Andhra Pradesh monthly business dataset with its four stores and dated stock history. Time how long it takes a user to identify a shortage manually and with the dashboard. Check whether the suggested transfer quantity respects source stock, whether a confirmed action updates the correct rows, and whether an Employee is blocked from confirming a change. Record the results instead of claiming time savings without measurements.

## Main technologies

- React and Vite for the website
- FastAPI for the backend API
- PostgreSQL and SQLAlchemy for database storage
- Python for file processing and backend logic
- Groq API for natural-language SQL generation

## Running with Docker Compose

Create a project `.env` file with a strong URL-safe `POSTGRES_PASSWORD` value. Create `backend/.env` with the settings required by `backend/app/core/config.py`, including the matching PostgreSQL URL and Groq API key. Use the Compose database service name in the URL, for example `postgresql://postgres:YOUR_PASSWORD@postgres:5432/ai_copilot`. The database port is published only on localhost for local development.

Run `docker compose up --build` from the project folder. The frontend is served on port 5173 and the API on port 8000.

## Render deployment

The `render.yaml` file creates a web service, static frontend, and private PostgreSQL database. Connect this repository in Render and deploy the Blueprint. Enter `GROQ_API_KEY` when Render prompts for it. The free PostgreSQL instance is suitable for a short presentation deployment, but free database storage expires after Render's free-plan retention period and should not be used for important records. Uploaded files on a free web service can be lost when the service restarts, so use the generated supplier, operations, and goods receipt documents for the presentation.
