import random
import re
import time
import os

import base64
import requests
import requests as r
from io import BytesIO
from PIL import Image
from telegram import MAX_MESSAGE_LENGTH, ParseMode, TelegramError
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.utils.helpers import escape_markdown

import kaga.modules.helper_funcs.fun_strings as fun
from kaga.modules.disable import DisableAbleCommandHandler
from kaga import DEV_USERS, LOGGER, SUDO_USERS, SUPPORT_USERS, dispatcher
from kaga.modules.disable import (
    DisableAbleCommandHandler,
    DisableAbleMessageHandler,
)
from kaga.modules.helper_funcs.alternate import typing_action
from kaga.modules.helper_funcs.extraction import extract_user
from kaga.modules.helper_funcs.filters import CustomFilters
from kaga import dispatcher


@typing_action
def runs(update, context):
    update.effective_message.reply_text(random.choice(fun.RUN_STRINGS))


@typing_action
def slap(update, context):
    args = context.args
    msg = update.effective_message

    # reply to correct message
    reply_text = (
        msg.reply_to_message.reply_text
        if msg.reply_to_message
        else msg.reply_text
    )

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            msg.from_user.first_name, msg.from_user.id
        )

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                slapped_user.first_name, slapped_user.id
            )

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(
            context.bot.first_name, context.bot.id
        )
        user2 = curr_user

    temp = random.choice(fun.SLAP_TEMPLATES)
    item = random.choice(fun.ITEMS)
    hit = random.choice(fun.HIT)
    throw = random.choice(fun.THROW)

    repl = temp.format(
        user1=user1, user2=user2, item=item, hits=hit, throws=throw
    )

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@typing_action
def punch(update, context):
    args = context.args
    msg = update.effective_message

    # reply to correct message
    reply_text = (
        msg.reply_to_message.reply_text
        if msg.reply_to_message
        else msg.reply_text
    )

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            msg.from_user.first_name, msg.from_user.id
        )

    user_id = extract_user(update.effective_message, args)
    if user_id:
        punched_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if punched_user.username:
            user2 = "@" + escape_markdown(punched_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                punched_user.first_name, punched_user.id
            )

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(
            context.bot.first_name, context.bot.id
        )
        user2 = curr_user

    temp = random.choice(fun.PUNCH_TEMPLATES)
    item = random.choice(fun.ITEMS)
    punch = random.choice(fun.PUNCH)

    repl = temp.format(user1=user1, user2=user2, item=item, punches=punch)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@typing_action
def police(update, context):
    message = update.effective_message.reply_text("Wuanjayy...")
    for i in fun.POLICE:
        message.edit_text(i)
        time.sleep(0.5)


@typing_action
def hug(update, context):
    args = context.args
    msg = update.effective_message

    # reply to correct message
    reply_text = (
        msg.reply_to_message.reply_text
        if msg.reply_to_message
        else msg.reply_text
    )

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            msg.from_user.first_name, msg.from_user.id
        )

    user_id = extract_user(update.effective_message, args)
    if user_id:
        hugged_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if hugged_user.username:
            user2 = "@" + escape_markdown(hugged_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                hugged_user.first_name, hugged_user.id
            )

    # if no target found, bot targets the sender
    else:
        user1 = "Awwh! [{}](tg://user?id={})".format(
            context.bot.first_name, context.bot.id
        )
        user2 = curr_user

    temp = random.choice(fun.HUG_TEMPLATES)
    hug = random.choice(fun.HUG)

    repl = temp.format(user1=user1, user2=user2, hug=hug)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@typing_action
def abuse(update, context):
    # reply to correct message
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.ABUSE_STRINGS))
    
    
@typing_action
def changemymind(update, context):
    msg = update.effective_message
    if not msg.reply_to_message:
        msg.reply_text("perlu membalas pesan untuk membuat stiker.")
    else:
        text = msg.reply_to_message.text
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
        url = r.get("message")
        if not url:
            msg.reply_text("Tidak ada URL yang diterima dari API!")
            return
        with open("temp.png", "wb") as f:
            f.write(requests.get(url).content)
        img = Image.open("temp.png")
        img.save("temp.webp", "webp")
        msg.reply_document(open("temp.webp", "rb"))
        os.remove("temp.webp")
        
       
@typing_action
def dice(update, context):
    context.bot.sendDice(update.effective_chat.id)


@typing_action
def shrug(update, context):
    # reply to correct message
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.SHGS))


def decide(update, context):
    args = update.effective_message.text.split(None, 1)
    if len(args) >= 2:  # Don't reply if no args
        reply_text = (
            update.effective_message.reply_to_message.reply_text
            if update.effective_message.reply_to_message
            else update.effective_message.reply_text
        )
        reply_text(random.choice(fun.DECIDE))


def yesnowtf(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    res = r.get("https://yesno.wtf/api")
    if res.status_code != 200:
        return msg.reply_text(random.choice(fun.DECIDE))
    else:
        res = res.json()
    try:
        context.bot.send_animation(
            chat.id, animation=res["image"], caption=str(res["answer"]).upper()
        )
    except BadRequest:
        return


@typing_action
def table(update, context):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.TABLE))


@typing_action
def cri(update, context):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.CRI))


@typing_action
def recite(update, context):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.BEING_LOGICAL))


@typing_action
def gbun(update, context):
    user = update.effective_user
    chat = update.effective_chat

    if update.effective_message.chat.type == "private":
        return
    if (
        int(user.id) in SUDO_USERS
        or int(user.id) in SUPPORT_USERS
        or int(user.id) in DEV_USERS
    ):
        context.bot.sendMessage(chat.id, (random.choice(fun.GBUN)))


@typing_action
def snipe(update, context):
    args = context.args
    try:
        chat_id = str(args[0])
        del args[0]
    except (TypeError, IndexError):
        update.effective_message.reply_text(
            "Tolong beri saya obrolan untuk digemakan!"
        )
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            context.bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Tidak dapat mengirim pesan. Mungkin saya bukan bagian dari grup itu?"
            )
    else:
        update.effective_message.reply_text(
            "Kemana saya harus mengirim??\nBeri aku id obrolan!"
        )


@typing_action
def copypasta(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("Saya butuh pesan untuk membuat pasta.")
    else:
        emojis = [
            "😂",
            "😂",
            "👌",
            "✌",
            "💞",
            "👍",
            "👌",
            "💯",
            "🎶",
            "👀",
            "😂",
            "👓",
            "👏",
            "👐",
            "🍕",
            "💥",
            "🍴",
            "💦",
            "💦",
            "🍑",
            "🍆",
            "😩",
            "😏",
            "👉👌",
            "👀",
            "👅",
            "😩",
            "🚰",
        ]
        reply_text = random.choice(emojis)
        # choose a random character in the message to be substituted with 🅱️
        b_char = random.choice(message.reply_to_message.text).lower()
        for c in message.reply_to_message.text:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        message.reply_to_message.reply_text(reply_text)


@typing_action
def clapmoji(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("Saya butuh pesan untuk bertepuk tangan!")
    else:
        reply_text = "👏 "
        reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
        reply_text += " 👏"
        message.reply_to_message.reply_text(reply_text)


@typing_action
def owo(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("Saya butuh pesan untuk meme.")
    else:
        faces = [
            "(・`ω´・)",
            ";;w;;",
            "owo",
            "UwU",
            ">w<",
            "^w^",
            r"\(^o\) (/o^)/",
            "( ^ _ ^)∠☆",
            "(ô_ô)",
            "~:o",
            ";____;",
            "(*^*)",
            "(>_",
            "(♥_♥)",
            "*(^O^)*",
            "((+_+))",
        ]
        reply_text = re.sub(r"[rl]", "w", message.reply_to_message.text)
        reply_text = re.sub(r"[ｒｌ]", "ｗ", message.reply_to_message.text)
        reply_text = re.sub(r"[RL]", "W", reply_text)
        reply_text = re.sub(r"[ＲＬ]", "Ｗ", reply_text)
        reply_text = re.sub(r"n([aeiouａｅｉｏｕ])", r"ny\1", reply_text)
        reply_text = re.sub(r"ｎ([ａｅｉｏｕ])", r"ｎｙ\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"Ｎ([ａｅｉｏｕＡＥＩＯＵ])", r"Ｎｙ\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(faces), reply_text)
        reply_text = re.sub(r"！+", " " + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
        reply_text += " " + random.choice(faces)
        message.reply_to_message.reply_text(reply_text)


@typing_action
def stretch(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("Aku butuh pesan untuk streeeeeeetch.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])",
            (r"\1" * count),
            message.reply_to_message.text,
        )
        if len(reply_text) >= MAX_MESSAGE_LENGTH:
            return message.reply_text(
                "Hasil pesan ini terlalu panjang untuk telegram!"
            )

        message.reply_to_message.reply_text(reply_text)


def me_too(update, context):
    message = update.effective_message
    reply = random.choice(
        ["Aku juga terima kasih", "Haha ya, aku juga", "Sama lol", "Aku irl"]
    )
    message.reply_text(reply)


def goodnight(update, context):
    message = update.effective_message
    reply = random.choice(fun.GDNIGHT)
    message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def goodmorning(update, context):
    message = update.effective_message
    reply = random.choice(fun.GDMORNING)
    message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    
    
@typing_action
def thonkify(update, context):
    from kaga.modules.helper_funcs.thonkify_dict import thonkifydict

    chat = update.effective_chat
    message = update.effective_message
    if not message.reply_to_message:
        msg = message.text.split(None, 1)[1]
    else:
        msg = message.reply_to_message.text

    # the processed photo becomes too long and unreadable +
    # the telegram doesnt support any longer dimensions +
    # you have the lulz
    if (len(msg)) > 39:
        message.reply_text("Pikirkan sendiri!")
        return

    tracking = Image.open(BytesIO(base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAYAAAOACAYAAAAZzQIQAAAALElEQVR4nO3BAQ0AAADCoPdPbQ8HFAAAAAAAAAAAAAAAAAAAAAAAAAAAAPwZV4AAAfA8WFIAAAAASUVORK5CYII=')))  # base64 encoded empty image(but longer)

    # remove characters thonkify can't parse
    for character in msg:
        if character not in thonkifydict:
            msg = msg.replace(character, "")

    x = 0
    y = 896
    image = Image.new('RGBA', [x, y], (0, 0, 0))
    for character in msg:
        value = thonkifydict.get(character)
        addedimg = Image.new('RGBA', [x + value.size[0] + tracking.size[0], y], (0, 0, 0))
        addedimg.paste(image, [0, 0])
        addedimg.paste(tracking, [x, 0])
        addedimg.paste(value, [x + tracking.size[0], 0])
        image = addedimg
        x = x + value.size[0] + tracking.size[0]

    maxsize = 1024, 896
    if image.size[0] > maxsize[0]:
        image.thumbnail(maxsize, Image.ANTIALIAS)

    # put processed image in a buffer and then upload cause async
    with BytesIO() as buffer:
        buffer.name = 'cache/image.png'
        image.save(buffer, 'PNG')
        buffer.seek(0)
        context.bot.send_sticker(chat_id=message.chat_id, sticker=buffer)
        
        
@typing_action
def changemymind(update, context):
    msg = update.effective_message
    if not msg.reply_to_message:
        msg.reply_text("perlu membalas pesan untuk membuat stiker.")
    else:
        text = msg.reply_to_message.text
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
        url = r.get("message")
        if not url:
            msg.reply_text("No URL was received from the API!")
            return
        with open("temp.png", "wb") as f:
            f.write(requests.get(url).content)
        img = Image.open("temp.png")
        img.save("temp.webp", "webp")
        msg.reply_document(open("temp.webp", "rb"))
        os.remove("temp.webp")


@typing_action
def trumptweet(update, context):
    msg = update.effective_message
    if not msg.reply_to_message:
        msg.reply_text("perlu membalas pesan ke tweet")
    else:
        text = msg.reply_to_message.text
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
        url = r.get("message")
        if not url:
            msg.reply_text("No URL was received from the API!")
            return
        with open("temp.png", "wb") as f:
            f.write(requests.get(url).content)
        img = Image.open("temp.png")
        img.save("temp.webp", "webp")
        msg.reply_document(open("temp.webp", "rb"))
        os.remove("temp.webp")


__help__ = """
Beberapa meme untuk bersenang-senang atau apa pun!

 × /shrug | /cri: Angkat bahu atau ToT.
 × /decide: Jawab secara acak ya tidak dll.
 × /abuse: Menyalahgunakan yang terbelakang!
 × /table: Membalik meja...
 × /runs: Balas string acak dari serangkaian balasan.
 × /slap: Tampar pengguna, atau ditampar jika bukan balasan.
 × /pasta: Meme copypasta terkenal, coba dan lihat
 × /clap: Tepuk tangan pada pesan seseorang!
 × /owo: UwU-fy seluruh teks XD.
 × /roll: Melempar dadu.
 × /recite: Kutipan logis untuk mengubah hidup Anda
 × /stretch:  streeeeeeetch iiiiiiit.
 × /warm: Peluk pengguna dengan hangat, atau peluk jika bukan balasan.
 × /punch: Pukul pengguna, atau dapatkan pukulan jika bukan balasan.
 × /police: Berikan Animasi sirene Polisi
 × thonkify: Membuat text thonkify

*Meme berbasis regex:*

`/decide` bisa juga digunakan dengan regex jika suka: `kaga Apa? <pertanyaan>: menjawab acak "Yes, No" dll.`

Beberapa filter regex lainnya adalah:
`saya juga` | `selamat pagi` | `selamat malam`.

KagaRobot akan membalas string acak sesuai saat kata-kata ini digunakan!
Semua filter regex dapat dinonaktifkan jika Anda tidak ingin ... suka: `/disable sayajuga`.

"""

__mod_name__ = "Memes"

SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug, run_async=True)
DECIDE_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(eve)"), decide, friendly="decide", run_async=True
)
SNIPE_HANDLER = CommandHandler(
    "snipe",
    snipe,
    pass_args=True,
    filters=CustomFilters.sudo_filter,
    run_async=True,
)
ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse, run_async=True)
POLICE_HANDLER = DisableAbleCommandHandler("police", police, run_async=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, run_async=True)
SLAP_HANDLER = DisableAbleCommandHandler(
    "slap", slap, pass_args=True, run_async=True
)
PUNCH_HANDLER = DisableAbleCommandHandler(
    "punch", punch, pass_args=True, run_async=True
)
HUG_HANDLER = DisableAbleCommandHandler(
    "warm", hug, pass_args=True, run_async=True
)
GBUN_HANDLER = CommandHandler("gbun", gbun, run_async=True)
TABLE_HANDLER = DisableAbleCommandHandler("table", table, run_async=True)
CRI_HANDLER = DisableAbleCommandHandler("cri", cri, run_async=True)
CHANGEMYMIND_HANDLER = DisableAbleCommandHandler("changemymind", changemymind, run_async=True)
PASTA_HANDLER = DisableAbleCommandHandler("pasta", copypasta, run_async=True)
CLAP_HANDLER = DisableAbleCommandHandler("clap", clapmoji, run_async=True)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo, run_async=True)
STRECH_HANDLER = DisableAbleCommandHandler("stretch", stretch, run_async=True)
MEETOO_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(saya juga)"), me_too, friendly="sayajuga", run_async=True
)
RECITE_HANDLER = DisableAbleCommandHandler("recite", recite, run_async=True)
DICE_HANDLER = DisableAbleCommandHandler("roll", dice, run_async=True)
YESNOWTF_HANDLER = DisableAbleCommandHandler(
    "decide", yesnowtf, run_async=True
)
GDMORNING_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(selamat pagi)"),
    goodmorning,
    friendly="selamatpagi",
    run_async=True,
)
GDNIGHT_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(selamat malam)"),
    goodnight,
    friendly="selamatmalam",
    run_async=True,
)
THONKIFY_HANDLER = DisableAbleCommandHandler("thonkify", thonkify, run_async=True)
CHANGEMYMIND_HANDLER = DisableAbleCommandHandler("changemymind", changemymind, run_async=True)
TRUMPTWEET_HANDLER = DisableAbleCommandHandler("trumptweet", trumptweet, run_async=True)


dispatcher.add_handler(POLICE_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(PUNCH_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(GBUN_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)
dispatcher.add_handler(RECITE_HANDLER)
dispatcher.add_handler(CRI_HANDLER)
dispatcher.add_handler(PASTA_HANDLER)
dispatcher.add_handler(CLAP_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRECH_HANDLER)
dispatcher.add_handler(MEETOO_HANDLER)
dispatcher.add_handler(DICE_HANDLER)
dispatcher.add_handler(YESNOWTF_HANDLER)
dispatcher.add_handler(GDMORNING_HANDLER)
dispatcher.add_handler(GDNIGHT_HANDLER)
dispatcher.add_handler(CHANGEMYMIND_HANDLER)
dispatcher.add_handler(THONKIFY_HANDLER)
dispatcher.add_handler(CHANGEMYMIND_HANDLER)
dispatcher.add_handler(TRUMPTWEET_HANDLER)
