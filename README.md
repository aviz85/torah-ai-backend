# AI Language Model Testing Platform

## Overview

This project is an AI Language Model Testing Platform designed to evaluate and compare different language models. It provides a structured way to create tests, run them against various language models, and analyze the results.

## Features

- Create and manage test cases
- Integrate multiple language models
- Run tests and collect results
- Evaluate model performance
- Track costs and manage budgets

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-language-model-testing-platform.git
   cd ai-language-model-testing-platform
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

## Usage

1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Access the admin interface at `http://localhost:8000/admin/` to manage tests, language models, and other data.

3. Use the API endpoints to run tests and retrieve results.

## API Endpoints

- `/api/sources/`: Manage test sources
- `/api/tests/`: Create and manage tests
- `/api/language-models/`: Manage language models
- `/api/test-runs/`: Run tests and retrieve results
- `/api/evaluations/`: Evaluate test results
- `/api/budgets/`: Manage daily budgets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.