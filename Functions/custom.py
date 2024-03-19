from Functions.db import *
from difflib import SequenceMatcher
import requests
import subprocess

def DEF_SEARCH_CUSTOMERID(CHATID, MESSAGE_TEXT):
    # Construct the SQL command
    sql_command = f"SELECT chatid FROM starters WHERE customerid = {MESSAGE_TEXT};"

    # Execute the SQL command using the subprocess module
    result = subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], capture_output=True, text=True, check=True)

    # Extract the result from the output
    tele_id = result.stdout.strip()

    if tele_id:
        TEXT = f"""شماره مشتری : {MESSAGE_TEXT}
        آیدی تلگرام : {tele_id}"""
    else:
        TEXT = "<b>❌ I can't find any telegram ID for this customer ID.</b>"


    return TEXT

