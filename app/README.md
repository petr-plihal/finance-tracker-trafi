# Development setup

## Install the application

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

2. Activate the environment:
    ```bash
    source venv/bin/activate
    ```

3. Install dependencies, which also include Flask:
    ```bash
    pip install -r requirements.txt
    ```

## Run the application locally

Go into the `app/` directory, and run the Flask application:
```bash
cd app
flask run --debug
```

The debug option allows for Python code execution from the browser, shows debug info in the browser and automatically refreshes when changes are made to code.