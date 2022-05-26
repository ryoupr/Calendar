from xmlrpc.client import DateTime
import PySimpleGUI as sg
import os
from tabnanny import check
from tracemalloc import start
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import datetime

# Import user func
from timeFormatCheck import timeFormatCheck
from dateFormatCheck import dateFormatCheck
from makeDateTime import makeDateTime
from generateDateTimeFromUserImput import generateDateTimeFromUserImput
from datetimeMaster import *
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    # Theme = DarkAmber
    sg.theme("DarkAmber")
    # 項目名サイズ
    sizeTypeA = 9
    buttonWidth = 50
    buttonHaight = 2
    datetimeBoxSize = 4
    layout = [
        [sg.Text("概要", size=(sizeTypeA)),
         sg.InputText("", size=(98), key="summary")],
        [sg.Text("場所", size=(sizeTypeA)), sg.InputText(
            "", size=(98), key="location")],
        [sg.Text("説明", size=(sizeTypeA)), sg.InputText(
            "", size=(98), key=("description"))],
        [sg.Text("開始年月日", size=(sizeTypeA)), sg.InputText(thisYear(), size=(datetimeBoxSize), key="startYear"), sg.Text("年"),
         sg.InputText(thisMonth(), size=(datetimeBoxSize), key=("startMonth")), sg.Text("月"), sg.InputText(thisDay(), size=(datetimeBoxSize), key=("startDate")), sg.Text("日")],
        [sg.Text("開始時間", size=(sizeTypeA)), sg.InputText("", size=(datetimeBoxSize), key=("startHour")),
         sg.Text("時"), sg.InputText("", size=(datetimeBoxSize), key=("startMinute")), sg.Text("分")],
        [sg.Text("", size=(sizeTypeA)), sg.Text("↓↓↓")],
        [sg.Text("終了年月日", size=(sizeTypeA)), sg.InputText(thisYear(), size=(datetimeBoxSize), key="endYear"), sg.Text(
            "年", ), sg.InputText(thisMonth(), size=(datetimeBoxSize), key=("endMonth")), sg.Text("月", ), sg.InputText(thisDay(), size=(datetimeBoxSize), key=("endDate")), sg.Text("日")],
        [sg.Text("終了時間", size=(sizeTypeA)), sg.InputText("", size=(datetimeBoxSize), key=("endHour")),
         sg.Text("時"), sg.InputText("", size=(datetimeBoxSize), key="endMinute"), sg.Text("分")], [sg.Text(size=(98), key=("result"))],
        [sg.Button("登録", key="Submit", size=(buttonWidth, buttonHaight)), sg.Button(
            "取消", key="Cancell", size=(buttonWidth, buttonHaight))]
    ]

    window = sg.Window("GoogleCalendarに予定を追加", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancell":
            break

        if event == "Submit":
            print("送信ボタンが押されました")
            # CLI版のmain.pyの中身を移植
            calendarEvent = {
                'summary': "",
                'location': "",
                'description': "",
                'start': {
                    'dateTime': "",
                    'timeZone': 'Japan',
                },
                'end': {
                    'dateTime': "",
                    'timeZone': 'Japan',
                },
            }

        # insert calendar event
            calendarEvent["summary"] = values["summary"]
            calendarEvent["location"] = values["location"]
            calendarEvent['description'] = values["description"]
            # todo dateTime入力情報からを生成する式を作成し変更後挿入する
            calendarEvent["start"]["dateTime"] = generateDateTimeFromUserImput(
                values["startYear"], values["startMonth"], values["startDate"], values["startHour"], values["startMinute"])
            calendarEvent["end"]["dateTime"] = generateDateTimeFromUserImput(
                values["endYear"], values["endMonth"], values["endDate"], values["endHour"], values["endMinute"]
            )
            print(calendarEvent)
            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            service = build('calendar', 'v3', credentials=creds)

            calendarEvent = service.events().insert(calendarId='ke37d1obkoa9ihbjghnc52ui54@group.calendar.google.com',
                                                    body=calendarEvent).execute()
            print("""
        ---------------------------------------
        Script succesfully!
        event id = """+calendarEvent['id'] + """
        ---------------------------------------
        """)
            window["result"].update("予定の追加は正常に終了しました！！")
            break
    window.close()
    print(f'eventは{event}')
    print(f'valuesは{values}')


if __name__ == "__main__":
    main()
