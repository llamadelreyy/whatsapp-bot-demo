import os
import time
import threading
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get port from environment variable
PORT = int(os.getenv('PORT', 8090))  # Default to 8090 if not specified

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_WHATSAPP_NUMBER")  # e.g., 'whatsapp:+14155238886'

# Twilio client
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Flask app setup
app = Flask(__name__)

# Simulated in-memory state store
user_state = {}

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    sender = request.form.get('From')
    incoming_msg = request.form.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Initialize state
    if sender not in user_state:
        user_state[sender] = "INIT"

    state = user_state[sender]

    # Initial greeting
    if state == "INIT":
        if incoming_msg == "hello kurauai!":
            user_state[sender] = "MAIN_MENU"
            msg.body(
                "Assalamualaikum dan Salam Sejahtera YB Chang Lih Kang!\n\n"
                "Saya Kuala Kurau AI adalah Ejen AI yang dibangunkan khas untuk membantu Komuniti Kuala Kurau.\n\n"
                "Saya bersedia untuk terus belajar, memahami dan membantu anda mendapatkan pelbagai maklumat berkaitan Kuala Kurau.\n\n"
                "Saya akan cuba memberikan jawapan berdasarkan maklumat yang saya ada.\n\n"
                "Bersama kita jayakan komuniti digital Kuala Kurau!\n\n"
                "Sila pilih salah satu di bawah:\n"
                "1. Info Kuala Kurau\n"
                "2. Khidmat Bantuan\n"
                "3. Program Semasa"
            )

        else:
            msg.body("Sila taip: Hello KurauAI!")

    # Main menu options
    elif state == "MAIN_MENU":
        if incoming_msg in ["1", "info kuala kurau"]:
            user_state[sender] = "INFO_KUALA_KURAU"
            msg.body(
                "Kuala Kurau ialah pekan nelayan di daerah Kerian, Perak. Terletak di muara Sungai Kurau, "
                "ia terkenal dengan kehidupan kampung yang tenang dan aktiviti perikanan tradisional. "
                "Tarikan utama termasuk pelayaran sungai, makanan laut segar seperti cucur udang dan telur masin, "
                "serta pantai Ban Pecah yang indah. Ia juga memiliki kilang padi Hai Hin dan beberapa homestay "
                "di tengah sawah padi. Lokasinya hanya sejam dari Taiping dan Pulau Pinang, menjadikannya destinasi "
                "santai yang sesuai untuk percutian ringkas sambil menikmati budaya dan keindahan alam.\n\n"
                "Adakah anda ingin tahu lebih lanjut berkenaan Kuala Kurau?\n"
                "1. Ya\n2. Tidak\n3. Kembali ke Laman Utama"
            )
        elif incoming_msg == "2":
            msg.body("Khidmat Bantuan: Sila hubungi 012-3456789 atau layari laman web rasmi.")
        elif incoming_msg == "3":
            msg.body("Program Semasa: Pasar Tani setiap Sabtu, Pesta Makanan Laut bulan hadapan.")
        else:
            msg.body("Sila pilih 1, 2 atau 3.")

    # Info Kuala Kurau follow-up
    elif state == "INFO_KUALA_KURAU":
        if incoming_msg == "1" or incoming_msg == "ya":
            user_state[sender] = "VIDEO"
            msg.body("Video akan dimainkan dalam 3 saat.")

            def countdown(to_number):
                # Ensure that both the 'from_' and 'to' are prefixed with 'whatsapp:'
                for count in ["3", "2", "1"]:
                    time.sleep(1)
                    twilio_client.messages.create(
                        from_=TWILIO_PHONE,  # From number with 'whatsapp:' prefix
                        to=f'whatsapp:{to_number}',  # Recipient with 'whatsapp:' prefix
                        body=count
                    )

            # Ensure to pass the full 'whatsapp:' formatted number
            threading.Thread(target=countdown, args=(sender.split(":")[1],)).start()

        elif incoming_msg == "2" or incoming_msg == "tidak":
            user_state[sender] = "MAIN_MENU"
            msg.body(
                "Okay, kembali ke menu utama.\n"
                "1. Info Kuala Kurau\n2. Khidmat Bantuan\n3. Program Semasa"
            )
        elif incoming_msg == "3" or incoming_msg == "kembali ke laman utama":
            user_state[sender] = "MAIN_MENU"
            msg.body(
                "Laman Utama:\n"
                "1. Info Kuala Kurau\n2. Khidmat Bantuan\n3. Program Semasa"
            )
        else:
            msg.body("Sila pilih:\n1. Ya\n2. Tidak\n3. Kembali ke Laman Utama")

    # Final step
    elif state == "VIDEO":
        msg.body("Terima kasih kerana menggunakan KurauAI!")

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
