# AutoPocket

A simple CLI to automate working with the Pocket API and crawled newssites.

## Usage

Ensure you have python3.7+ installed. Then, clone this repository, install the package requirements and run cli.py

### Clone the Repo

The repo can be cloned from terminal/powershell, with: 

```bash
> git clone https://github.com/brandontkessler/AutoPocket.git
```

### Set up Virtual Environment

The full setup and instructions are in the code below:

```bash
> # navigate into AutoPocket directory
> cd AutoPocket
>
> # create a virtual environment
> python -m venv venv
>
> # activate the virtual environment
> source venv/bin/activate # linux/mac
> .\venv\Scripts\activate # powershell
>
> # You will know the venv has been activated
> #   as it will 
>
> # install package depencies
> pip install -r requirements.txt
```

### Run the Script

Run the cli script with the following:

```bash
> python cli.py
```