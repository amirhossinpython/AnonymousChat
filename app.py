from flask import Flask,request,jsonify,render_template
from eitaa_bot import EitaaBot
from datetime import datetime  
from khayyam import JalaliDatetime  
import pytz  

app =Flask(__name__)

token = "bot248965:6fb76dfd-667d-4e1d-9644-daee02b47469"
bot = EitaaBot(token=token)

chat_id = "10462629"

utc_now = datetime.now(pytz.utc)  
tehran_tz = pytz.timezone('Asia/Tehran') 
tehran_now = utc_now.astimezone(tehran_tz) 


jalali_now = JalaliDatetime(tehran_now)  


shamsi_date = jalali_now.strftime("%Y/%m/%d")  
shamsi_time = jalali_now.strftime("%H:%M")  



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
  
    
    message = request.form.get("message")
    message = f"ناشناس به امیرحسین  👤:\n{message} ⏰\nتاریخ: {shamsi_date} 📅\nساعت: {shamsi_time} ⏲️"  
    
    if not message:
        return jsonify({"status": "error", "message": "لطفاً پیام خود را وارد کنید."})
    
    try :
        bot.send_message(chat_id=chat_id, message=message)  
        
        return jsonify({"status": "success", "message": "پیام شما با موفقیت ارسال شد!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در ارسال پیام: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
    
                               

