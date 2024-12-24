# AskMe App

## Overview

Welcome to the **AskMe App** repository! This is a web application built with **Django** and **PostgreSQL**. The application allows users to post questions, answer questions, and like content.

#### Created for VK Education [2024, Autumn]

### Features
- **User Authentication**: Register, login, and manage profiles.
- **Questions and Answers**: Users can post questions and answers, each with associated likes.
- **Like System with Anti-Spam Protection**: A user can like each question or answer only once.
- **Pagination**: Large lists of questions or answers are paginated for a smooth user experience.

## Prerequisites

Before you get started, ensure you have the following installed on your machine:

- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Node.js](https://nodejs.org/en/) (for compiling static assets if applicable)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Getting Started

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/val3rkq/askme-mitioglo.git
cd askme-mitioglo
```

### 2. Set Up the Python Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

1. **Open PostgreSQL CLI** or **pgAdmin** and create a new database:
   ```sql
   CREATE DATABASE askme_db;
   CREATE USER askme_user WITH PASSWORD 'your_password';
   ALTER ROLE askme_user SET client_encoding TO 'utf8';
   ALTER ROLE askme_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE askme_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE askme_db TO askme_user;
   ```

2. **Configure Database Settings in Django**:
   In your `settings.py` file, update the `DATABASES` section:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'askme_db',
           'USER': 'askme_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### 5. Run Migrations

Apply the initial migrations to set up your database tables:

```bash
python manage.py migrate
```

### 6. Load Initial Data (Optional)

If you have a script to populate the database, run it:

```bash
python manage.py fill_db [ratio]
```

ratio - is a number of users in db

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to access the application.

## Additional Commands

### Running Tailwind CSS Build (Optional)

If you're using Tailwind CSS for frontend styling, install Node dependencies and run the build:

```bash
npm install
npm run build:css
```

This will compile the Tailwind CSS into the `public/css` directory.

## Project Structure

- **app/**: Django app with models for User, Question, Answer, and Like functionality.
- **templates/**: HTML templates for frontend pages.
- **static/**: Static assets (CSS, JS) used in the project.
- **management/commands**: Custom management commands, including scripts to fill the database.

## Customization

- **Settings**: Modify project settings in `settings.py` as needed.
- **Database Models**: Models for questions, answers, and likes are located in `app/models.py` and enforce uniqueness constraints to prevent like spamming.

## Contributing

If you'd like to contribute, feel free to submit a pull request. For major changes, please open an issue first to discuss what you’d like to change.

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.
