import PySimpleGUI as sg
import qrcode
import requests
from datetime import date
import os
import json

sala = '210'

layout = [
    [sg.Image(key="-IMAGE-", size=(200, 100))],
    [sg.Text("No results, generate QR Code", key="-TEXT")],
    [sg.Button("Generate QR Code")]
]

window = sg.Window("QRCode Generator", layout, size=(480, 320))


def generate_qr_code(link):
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    file_name = "qr_code" + ".png"
    path = os.path.join(os.getcwd(), file_name)
    img.save(path)
    return path


while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Generate QR Code":
        url ='https://5889-2001-818-eaff-300-141d-35f-abb3-b06.eu.ngrok.io/api/v1/qrCode/' + sala
        response = requests.get(url)
        response_dict = json.loads(response.text)
        id = 0
        print(response_dict['schedules'])
        #printfor item in my_list:
        for item in response_dict['schedules']:
            if item['id']:
                print(item['id'])
                id = item['id']

        qr = {'id': id}
        qr_code_image_path = generate_qr_code(json.dumps(qr))
        window["-IMAGE-"].update(filename=qr_code_image_path)
        window["-TEXT"].hide_row()

window.close()
