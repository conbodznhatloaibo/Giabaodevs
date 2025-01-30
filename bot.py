import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Nhập token bot của bạn tại đây (KHÔNG chia sẻ token công khai)
TOKEN = '7930110174:AAG25HyJQVyuxc4eLlkhzCpVZVJ9dHt0X3s'

API_URL = 'https://api.natnetwork.sbs/likeff?id='
API_SPAM_URL = 'https://api.natnetwork.sbs/spamsms?phone={}&count={}'

# Danh sách ID Admin (Chỉ admin mới có quyền sử dụng mute/unmute)
ADMIN_IDS = [6364889098]

# Hệ thống quản lý người dùng VIP
VIP_USERS = []

try:
    with open('vip_users.txt', 'r') as f:
        VIP_USERS = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    pass


# Lưu dưới dạng tập hợp để thêm/xóa nhanh hơn

# Hệ thống quản lý người dùng
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh khởi động bot"""
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {
            'name': update.effective_user.full_name,
            'id': user_id
        }
    await update.message.reply_text(f'Chào bạn, tôi là Bot của Gia Bảo!\n\n📌 **ID của bạn:** `{user_id}`', parse_mode="Markdown")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lấy ID của người dùng hoặc từ reply/tag"""
    user_id = None
    if update.message.reply_to_message:
        # Nếu tin nhắn là reply, lấy ID người dùng trong tin nhắn đó
        user_id = update.message.reply_to_message.from_user.id
    elif update.message.entities:
        # Nếu có tag người dùng, lấy ID người được tag
        for entity in update.message.entities:
            if entity.type == "mention":
                username = update.message.text[entity.offset:entity.offset + entity.length]
                user_id = (await context.bot.get_chat(username)).id
    if user_id is None:
        user_id = update.effective_user.id
    # Nếu không reply hay tag thì trả về ID của người gửi
    await update.message.reply_text(f"📌 **ID của bạn:** `{user_id}`", parse_mode="Markdown")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hiển thị menu chính với tất cả các lệnh"""
    keyboard = [
        [InlineKeyboardButton("🔹 Buff Like", callback_data="buff_like")],
        [InlineKeyboardButton("📞 Spam SMS", callback_data="spamsms")],
        [InlineKeyboardButton("⚡ Spam VIP", callback_data="spamvip")],
        [InlineKeyboardButton("ℹ️ Lấy ID của tôi", callback_data="myid")],
        [InlineKeyboardButton("🔇 Im lặng (Mute)", callback_data="mute"), InlineKeyboardButton("🔊 Mở khóa (Unmute)", callback_data="unmute")],
        [InlineKeyboardButton("📝 Thêm VIP User", callback_data="addvip"), InlineKeyboardButton("❌ Xóa VIP User", callback_data="removevip")],
        [InlineKeyboardButton("📖 Hướng dẫn sử dụng", callback_data="huong_dan")],
        [InlineKeyboardButton("🔍 Lấy ID người dùng (reply/tag)", callback_data="get_user_id")],
    ]
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_file_id = "files.catbox.moe/v3rd0v.mp4"
    await update.message.reply_video(video=video_file_id, caption=f""" 
┏━━━━━━━━━━━━━━━━━━━━━━━━━ 
┃ 💮 𝙈𝙚𝙣𝙪 𝘽𝙤𝙩 💮 
┃•/𝘽𝙪𝙛𝙛𝙇𝙞𝙠𝙚 
┃•/𝙨𝙥𝙖𝙢𝙨𝙢𝙨 
┃•/𝙨𝙥𝙖𝙢𝙫𝙞𝙥 (𝙑𝙞𝙥 𝙐𝙨𝙚𝙧) 
┃•/𝙢𝙮𝙞𝙙 
┃•/𝙢𝙪𝙩𝙚 (𝘼𝙙𝙢𝙞𝙣) 
┃•/𝙪𝙣𝙢𝙪𝙩𝙚 (𝘼𝙙𝙢𝙞𝙣) 
┃•/𝙖𝙙𝙙𝙫𝙞𝙥 (𝘼𝙙𝙢𝙞𝙣) 
┃•/𝙧𝙚𝙢𝙤𝙫𝙚𝙫𝙞𝙥 (𝘼𝙙𝙢𝙞𝙣) 
┃•/𝙢𝙚𝙣𝙪   
┃/layid
┗━━━━━━━━━━━━━━━━━━━━━━━━━ 
""")

async def handle_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý các callback từ menu"""
    query = update.callback_query
    await query.answer()

    if query.data == "spamsms":
        await query.edit_message_text("📞 *Chức năng Spam SMS*\n\nVui lòng sử dụng lệnh /spamsms <số điện thoại> <số lượng> để thực hiện.")
    elif query.data == "spamvip":
        await query.edit_message_text("⚡ *Chức năng Spam VIP*\n\nVui lòng sử dụng lệnh /spamvip <số điện thoại> <số lượng> để thực hiện.")
    elif query.data == "myid":
        await query.edit_message_text("ℹ️ *Lấy ID của bạn*\n\nVui lòng sử dụng lệnh /myid để lấy ID người dùng.")
    elif query.data == "mute":
        await query.edit_message_text("🔇 *Chức năng Mute*\n\nVui lòng sử dụng lệnh /mute <user_id> để im lặng người dùng.")
    elif query.data == "unmute":
        await query.edit_message_text("🔊 *Chức năng Unmute*\n\nVui lòng sử dụng lệnh /unmute <user_id> để mở khóa người dùng.")
    elif query.data == "addvip":
        await query.edit_message_text("📝 *Thêm VIP User*\n\nVui lòng sử dụng lệnh /addvip <user_id> để thêm người dùng vào VIP.")
    elif query.data == "removevip":
        await query.edit_message_text("❌ *Xóa VIP User*\n\nVui lòng sử dụng lệnh /removevip <user_id> để xóa người dùng khỏi VIP.")
    elif query.data == "huong_dan":
        await query.edit_message_text("📖 *Hướng dẫn sử dụng*\n\nChức năng bot bao gồm: Buff Like, Spam SMS, Spam VIP, Mute/Unmute, và thêm/xóa người dùng VIP.")

async def buff_like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buff like cho người dùng"""
    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng cung cấp ID người dùng. Ví dụ: /bufflike <id>")
        return
    user_id = context.args[0]
    response = requests.get(f"{API_URL}{user_id}")
    if response.status_code == 200:
        await update.message.reply_text(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💮 Attack Successfully Sent 💮
┃ PHONE     • [{user_id}]
┃ COUNT     • [90-100 like]
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""") 
    else:
        await update.message.reply_text("Có lỗi xảy ra, vui lòng thử lại.")
        
        
async def spamsms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Spam SMS cho người dùng"""
    if len(context.args) < 2:
        await update.message.reply_text("Vui lòng cung cấp số điện thoại và số lượng. Ví dụ: /spamsms <số điện thoại> <số lượng>")
        return
    phone = context.args[0]
    count = int(context.args[1])
    if count > 20:
        await update.message.reply_text("Số lượng tối đa là 20 lần.")
        return
    response = requests.get(API_SPAM_URL.format(phone, count))
    if response.status_code == 200:
        await update.message.reply_text(f"Attack {phone} Số Lần {count}.")
    else:
        await update.message.reply_text("Có lỗi xảy ra, vui lòng thử lại.")

async def spamvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Spam SMS cho VIP users"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này!")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Vui lòng cung cấp số điện thoại và số lượng. Ví dụ: /spamvip <số điện thoại> <số lượng>")
        return
    phone = context.args[0]
    count = int(context.args[1])
    if count > 200:
        await update.message.reply_text("Số lượng tối đa là 200 lần.")
        return
    if update.effective_user.id in VIP_USERS:
        response = requests.get(API_SPAM_URL.format(phone, count))
        if response.status_code == 200:
            await update.message.reply_text(f"Attack {phone} Số Lần {count}.")
        else:
            await update.message.reply_text("Có lỗi xảy ra, vui lòng thử lại.")
    else:
        await update.message.reply_text("Bạn không phải là VIP user!")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Im lặng người dùng"""
    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng cung cấp ID người dùng để im lặng. Ví dụ: /mute <user_id>")
        return
    user_id = int(context.args[0])
    if user_id in users:
        await context.bot.restrict_chat_member(update.message.chat.id, user_id, permissions=ChatPermissions())
        await update.message.reply_text(f"Đã im lặng người dùng {user_id}.")
    else:
        await update.message.reply_text("Không tìm thấy người dùng!")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mở khóa người dùng"""
    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng cung cấp ID người dùng để mở khóa. Ví dụ: /unmute <user_id>")
        return
    user_id = int(context.args[0])
    if user_id in users:
        await context.bot.restrict_chat_member(update.message.chat.id, user_id, permissions=ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"Đã mở khóa người dùng {user_id}.")
    else:
        await update.message.reply_text("Không tìm thấy người dùng!")

async def addvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Thêm người dùng vào VIP"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này!")
        return
    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng cung cấp ID người dùng để thêm vào VIP. Ví dụ: /addvip <user_id>")
        return
    user_id = int(context.args[0])
    VIP_USERS.add(user_id)
    await update.message.reply_text(f"Đã thêm người dùng {user_id} vào VIP.")

async def removevip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xóa người dùng khỏi VIP"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này!")
        return
    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng cung cấp ID người dùng để xóa khỏi VIP. Ví dụ: /removevip <user_id>")
        return
    user_id = int(context.args[0])
    if user_id in VIP_USERS:
        VIP_USERS.remove(user_id)
        await update.message.reply_text(f"Đã xóa người dùng {user_id} khỏi VIP.")
    else:
        await update.message.reply_text("Người dùng không phải là VIP.")            
def main():
    """Hàm khởi động bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Thêm các handler cho bot
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('myid', myid))
    application.add_handler(CommandHandler('bufflike', buff_like))
    application.add_handler(CommandHandler('spamsms', spamsms))
    application.add_handler(CommandHandler('spamvip', spamvip))
    application.add_handler(CommandHandler('mute', mute))
    application.add_handler(CommandHandler('unmute', unmute))
    application.add_handler(CommandHandler('addvip', addvip))
    application.add_handler(CommandHandler('removevip', removevip))
    
    # Xử lý các callback từ menu
    application.add_handler(CallbackQueryHandler(handle_menu_callback))

    # Chạy bot
    application.run_polling()

if __name__ == '__main__':
    main()
    