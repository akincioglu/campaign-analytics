# Campaign Analytics

Campaign Analytics is a Django application designed to manage and analyze campaign data. The application allows you to upload data from CSV files and perform various analyses.

## Features

- Upload data from CSV files
- Calculate conversion rates
- Analyze status distribution
- Evaluate category performance
- Aggregate filtered data

## Technologies

- Django
- Django Rest Framework
- PostgreSQL
- Python

## Getting Started

#### Requirements

- Python 3.9 or higher
- PostgreSQL
- pip

#### Installation

1. Clone this repository:

```bash
  git clone https://github.com/akincioglu/campaign-analytics.git
  cd campaign-analytics
```

2. Create and activate a virtual environment:

```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
  pip install -r requirements.txt
```

4. Create a `.env` file and add the necessary environment variables:

```bash
  DB_NAME=your_db_name
  DB_USER=your_user
  DB_PASSWORD=your_password
  DB_HOST=your_host
  DB_PORT=your_port
  API_VERSION=v1
```

5. Create the database and apply migrations:

```bash
  python manage.py migrate
```

6. Start the server:

```bash
  python manage.py runserver
```

## API Endpoints

#### CSV Upload

**Description**: Uploads a CSV file and adds the data to the database.

```http
  POST /api/analytics/upload-csv/
```

| Parameter | Type   | Description                           |
| :-------- | :----- | :------------------------------------ |
| `file`    | `file` | **Required**. The CSV file to upload. |

#### Conversion Rate

**Description**: Returns the conversion rate for each customer_id and specifies the highest and lowest conversion rates.

```http
  GET /api/conversion-rate/
```

#### Status Distribution

**Description**: Returns the distribution of statuses for campaign data.

```http
  GET /api/status-distribution/
```

#### Category Type Performance

**Description**: Returns total performance metrics for a specific category and type.

```http
  GET /api/category-type-performance/
```

#### Filtered Aggregation

**Description**: Returns aggregated data for a specified date range and category.

```http
  GET /api/filtered-aggregation/
```

| Parameter    | Type     | Description                                |
| :----------- | :------- | :----------------------------------------- |
| `start_date` | `string` | **Required**. The start date (YYYY-MM-DD). |
| `end_date`   | `string` | **Required**. The end date (YYYY-MM-DD).   |
| `category`   | `string` | **Required**. The category to filter by.   |
