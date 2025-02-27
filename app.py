from flask import Flask, request, jsonify, render_template  
from eitaa_bot import EitaaBot  
from datetime import datetime  
from khayyam import JalaliDatetime  
import pytz  

app = Flask(__name__)  

token = "توکن"  
bot = EitaaBot(token=token)  

chat_id = "چت ایدی"  


def get_jalali_time():  
    utc_now = datetime.now(pytz.utc)  
    tehran_tz = pytz.timezone('Asia/Tehran')   
    tehran_now = utc_now.astimezone(tehran_tz)   
    jalali_now = JalaliDatetime(tehran_now)  
    return jalali_now.strftime("%Y/%m/%d"), jalali_now.strftime("%H:%M")  

@app.route("/")  
def home():  
    return render_template("index.html")  

@app.route("/send_message", methods=["POST"])  
def send_message():  
    message = request.form.get("message")  
    
    if not message:  
        return jsonify({"status": "error", "message": "لطفاً پیام خود را وارد کنید."})  
    
    
    shamsi_date, shamsi_time = get_jalali_time()  
    
    final_message = f"ناشناس به امیرحسین  👤:\n{message} ⏰\nتاریخ: {shamsi_date} 📅\nساعت: {shamsi_time} ⏲️"  

    try:  
        bot.send_message(chat_id=chat_id, message=final_message)  
        return jsonify({"status": "success", "message": "پیام شما با موفقیت ارسال شد!"})  
    except Exception as e:  
        return jsonify({"status": "error", "message": f"خطا در ارسال پیام: {str(e)}"})  

if __name__ == "__main__":  
    app.run(debug=True)  
