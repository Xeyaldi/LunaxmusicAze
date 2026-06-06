from pyrogram import filters
from pyrogram import Client as Bot
from pyrogram.types import Message

# ─────────────────────────────────────────
#  /tag komutu — qrupdakı bütün üzvləri tağlayır
#  Yalnız admin istifadə edə bilər
# ─────────────────────────────────────────

@Bot.on_message(filters.command("tag") & filters.group)
async def tag_all(client: Bot, message: Message):
    # Yalnız adminlər istifadə edə bilər
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ("administrator", "creator"):
        return await message.reply_text("❌ Bu komutdan yalnız adminlər istifadə edə bilər.")

    # Komutdan sonra yazılan mətn (məsələn: /tag Salam hamı!)
    custom_text = ""
    if len(message.command) > 1:
        custom_text = " ".join(message.command[1:])

    # Qrupdakı üzvləri topla
    tagged = []
    async for member in client.get_chat_members(message.chat.id):
        # Botları və silinmiş hesabları atla
        if member.user.is_bot or member.user.is_deleted:
            continue
        tagged.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")

    if not tagged:
        return await message.reply_text("❌ Tağlamaq üçün üzv tapılmadı.")

    # Hər mesajda max 5 nəfər tağla (Telegram limiti üçün)
    chunk_size = 5
    header = f"📢 **{custom_text}**\n\n" if custom_text else "📢 **Hamını tağlayıram:**\n\n"

    for i in range(0, len(tagged), chunk_size):
        chunk = tagged[i:i + chunk_size]
        text = (header if i == 0 else "") + " ".join(chunk)
        await message.reply_text(text, disable_web_page_preview=True)
