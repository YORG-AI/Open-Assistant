# Webapp-Backend

A brief description of the project.

## Installation

1. Clone the repository.
2. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Pre-Commit Hooks
  The pre-commit git hooks consists on run some checks before confirm or commit your staged changes on the local repo, the <i>.pre-commit-config.yml</i> file contains the checks. <br>
  https://pre-commit.com/ <br>
  https://pypi.org/project/pre-commit/ <br>

  To set it up, you need to run this command on the root folder of the project
  ```console
  (venv)$ pre-commit install
  ```

  It runs each time you try to commit your changes, or you can just run it manually
  ```console
  (venv)$ pre-commit run --all-files
  ```


  The following local checks are implemented:

  - Linting with PyLint
  ```console
  (venv)$ pylint *
  ```

## Usage

Start the application using the following command:

    docker-compose up --build

If it fails: "set: illegal option -"

Try this: `sed -i 's/\r$//' entrypoint.sh`

Then, open your web browser and navigate to: http://localhost:8000/docs

## Debug

### VSCode

#### Debug Simple Node/Assignment

1. Add debug configuration in `.vscode/launch.json`

    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "localhost",
            "pathMappings": [
                {
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "/app"
                }
            ]
            }
        ]
    }
    ```

2. Add some breakpoints.

3. Start the application using the following command:

       docker-compose -f docker-compose.debug.yml up

4. Click `Python: Remote Attach` buttom in Run And Debug sidebar.

#### Debug `startup.py`

1. Add debug configuration in `.vscode/launch.json`

    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "localhost",
            "pathMappings": [
                {
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "/app"
                }
            ]
            }
        ]
    }
    ```

2. Run `docker-compose up --build`

3. Run `debug_startup.sh`

4. Click `Python: Remote Attach` buttom in Run And Debug sidebar.


#### Debug Jupyter YKernel

1. Add debug configuration in `.vscode/launch.json`

    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "localhost",
            "pathMappings": [
                {
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "/app"
                }
            ]
            }
        ]
    }
    ```

2. Modify `kernel.json`

```json
{
    "argv": [
        "python",
        "-m",
        "debugpy",
        "--wait-for-client",
        "--listen",
        "0.0.0.0:5678",
        "-m",
        "src.service.ykernel.ykernel",
        "-f",
        "{connection_file}"
    ],
    "display_name": "YKernel"
}
```

3. Run `docker-compose up --build` 

4. Click `Python: Remote Attach` buttom in Run And Debug sidebar.

## Testing

To run the tests, execute the following command:

    docker-compose exec fastapi python -m pytest -s src/tests

## Contributing

1. Fork the repository.
2. Create a new branch:

    ```bash
    git checkout -b my-new-feature
    ```

3. Make changes and commit them:

    ```bash
    git commit -am 'Add some feature'
    ```

4. Push to the branch:

    ```bash
    git push origin my-new-feature
    ```

5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
