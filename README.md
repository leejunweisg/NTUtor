# NTUtor
CZ3002 - Group Assignment (AY20/21)

## Installation
1. Clone the repo into a location of your choice. (e.g. `C:\Users\junwei\Desktop\projectfiles\`)<br/>
The cloned repo will stored at  `C:\Users\junwei\Desktop\projectfiles\NTUtor\`
2. Next, at `C:\Users\junwei\Desktop\projectfiles`, create a new virtual environemnt using venv: `virtualenv venv`<br/>
The virtual environment will be created at: `C:\Users\junwei\Desktop\projectfiles\venv\`
4. Activate the virtual environment: `.\venv\Scripts\activate`<br/>
You should see a `(venv)` prepended to the terminal prompt.
5. Change directory to the cloned repository: `cd NTUtor`
6. Install dependencies using pip: `pip install -r requirements.txt`
7. Installation complete.

## Run Development Server
1. From the root directory, execute: `python manage.py runserver`
3. Navigate to `localhost:8000` on your browser.

## Super User Account
### If needed, create a superuser account from the terminal
1. From the root directory, execute: `python manage.py createsuperuser`
2. Follow the prompts to create a superuser account.

### Or use a pre-created superuser account
Username: `admin123`
password: `password123!`
