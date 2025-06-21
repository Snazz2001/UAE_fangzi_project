Before you start:

- Make sure you have Python installed on your system.
- Clone the repo.

## Step 1: Open your Terminal / Command Prompt and navigate to your project directory

## Step 2: Create a Virtual Environment

A virtual environment (venv) isolates your project's dependencies from your system's global Python packages, preventing conflicts.
Action: Run the command to create a virtual environment.

Command:

Bash

**python -m venv venv**

(This creates a folder named venv inside your project directory.)

## Step 3: Activate the Virtual Environment

Activating the venv means that any pip or python commands you run will use the packages and Python interpreter within this specific environment.
Action: Run the activation script specific to your operating system.

On Linux/MacOS

Bash

**source venv/bin/activate**

## Step 4: Install Packages from requirements.txt

Now that your virtual environment is active, you can install the necessary libraries.
Action: Install the packages listed in your requirements.txt.

Command:

Bash

**pip install -r requirements.txt**

## Step 5: Run your FastAPI Service with Uvicorn

Action: Start the Uvicorn server to run your FastAPI application.
Command:

Bash

**uvicorn main:app --reload**

main:app: Tells Uvicorn to look for an application object named app inside the main.py file.

--reload: This is very useful for development. Uvicorn will automatically restart the server whenever you make changes to your code.

## Step 6: Open the Browser to the Specific URL

While Uvicorn is running in your terminal, open another terminal window/tab or proceed to open your web browser.

Action: Open your web browser and navigate to the specified URL.
http://127.0.0.1:8000/properties/search?roi=0.06&cost=1500000.0  (Area will be ignored)

Above, you'll find the instructions for starting the service and calling it directly via a web address. After the service is up and running, 
you also have the option to call it from within your Python code by running request.py
