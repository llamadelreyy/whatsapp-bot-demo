import os
import threading
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv('PORT', 8090))
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_WHATSAPP_NUMBER")  # Example: 'whatsapp:+14155238886'

# Twilio client setup
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Flask app
app = Flask(__name__)

# Countdown messaging function
def countdown_messages(to_number):
    def send_message(delay, text):
        threading.Timer(delay, lambda: twilio_client.messages.create(
            from_=TWILIO_PHONE,
            to=to_number,
            body=text
        )).start()

    send_message(1, "3")
    send_message(2, "2")
    send_message(3, "1")

@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    sender = request.form.get('From')  # Format: 'whatsapp:+60xxxxxxxxx'
    incoming_msg = request.form.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Trigger: "hello"
    if incoming_msg == "hello":
        msg.body(
            "Assalamualaikum dan Salam Sejahtera!\n\n"
            "Saya Kuala Kurau AI adalah Ejen AI yang dibangunkan khas untuk membantu Komuniti Kuala Kurau.\n\n"
            "Saya bersedia untuk terus belajar, memahami dan membantu anda mendapatkan pelbagai maklumat berkaitan Kuala Kurau.\n\n"
            "Teruskan pertanyaan anda sama ada berkaitan:\n"
            "- Program\n"
            "- Aktiviti\n"
            "- Bantuan\n"
            "- Cuaca\n"
            "- Aduan\n"
            "- Talian untuk dihubungi\n\n"
            "Saya akan cuba memberikan jawapan berdasarkan maklumat yang saya ada.\n\n"
            "Bersama kita jayakan komuniti digital Kuala Kurau!\n\n"
            "Sila pilih salah satu di bawah:\n"
            "1. Info Kuala Kurau\n"
            "2. Khidmat Bantuan\n"
            "3. Program Semasa"
        )

    # Trigger: "info" or "1"
    elif incoming_msg in ["info", "1"]:
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

    # Trigger: "ya" or "1" after info
    elif incoming_msg in ["ya"]:
        msg.body("Video akan dimainkan dalam 3 saat.")
        countdown_messages(sender)

    # Fallback
    else:
        msg.body("Sila taip: Hello, Info, atau Ya untuk memulakan interaksi.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
