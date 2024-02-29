Bulk Exchange UserProfile App

Review `high_level_design.pdf` for Project Overview and Approach



Prerequisites

- GCP CLI
- Terraform CLI

------------Setup GCP via TerraForm ----------

1) Create GCP Project

`gcloud projects create --name bulk-exc-profiles --set-as-default`

2) Auth GCP CLI

`gcloud auth application-default login --project $PROJECT_ID`

3) Create Terraform state bucket with versioning

`gsutil mb gs://${PROJECT_ID}-tfstate`
`gsutil versioning set on gs://${PROJECT_ID}-tfstate`

4) Update `terraform/main.tf` with correct `$PROJECT_ID`


5) Startup Terraform

`terraform init`

6) Setup GCP via Terraform

`terraform plan`

`terraform apply`

------------To Run Locally ----------

1) Create a venv to isolate project dependencies:

`python -m venv venv`

2) Activate the Python virtual environment:

`source venv/bin/activate`

3) Install the project dependencies:

`pip install -r requirements.txt`


4) Setup local `.env` file:

```text
SECRET_KEY=<Sercet Key>
DATABASE_URL=sqlite:////tmp/db.sqlite3
DEBUG=on
```

5) Setup database migrations

`python manage.py migrate`

6) Create a superuser:

`python manage.py createsuperuser --username admin --email admin@gmail.com`

7) Run the local server

`python manage.py runserver`


Browse API:

`POST`:`127.0.0.1:8000/auth/login/`

`POST`:`127.0.0.1:8000/auth/register/`

`GET`:`127.0.0.1:8000/profiles/`

`GET`:`127.0.0.1:8000/profiles/<id>`



