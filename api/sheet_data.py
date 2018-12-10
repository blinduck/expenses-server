from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Ssq7UJnrYIFfF0Tv_U_EUhKRjVNSO9CGlMGiSMlZBDk'
SAMPLE_RANGE_NAME = 'Sheet1!A2:K250'

def in_list(list, index, default=None):
    try:
        return list[index]
    except IndexError as e:
        return default

def convert_plus1(val):
    if not val:
        return 0
    if val.strip() == "Yes":
        return 1
    else:
        return len(val.split(','))

def convert_invited_to_dinner(val):
    return val == "Yes"


def get_sheet_service():
    store = file.Storage('api/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('api/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    sheet = service.spreadsheets()
    return sheet

def get_data():
    sheet = get_sheet_service()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values')
    perms = { v[0]: {
        'invitedToDinner': convert_invited_to_dinner(in_list(v, 2)),
        'allowedPlus1': convert_plus1(in_list(v,3)),
        'completed': in_list(v, 4),
        'index': i+2
    } for i,v in enumerate(values)}

    if not values:
        return None
    else:
        return perms

def write_to_row(index, data):
    values = {'values': [data],}

    range = "Sheet1!F{}:K{}".format(index, index)

    sheet = get_sheet_service()
    resp = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range,
        body=values,
        valueInputOption="RAW"
    ).execute()
    return resp


