from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup as Markup,
    InlineKeyboardButton as Button,
    Message,
    CallbackQuery,
)
from telebot import apihelper
from json import load, dump
from time import sleep
import sqlite3


bot_token = "6893297008:AAH-Z7lseu1gKyxWKHKiBgbuaUqOB2fcbGY"  # YOUR BOT TOKEN
ben = TeleBot(bot_token)

MAIN_OWNER = 5451878368  # YOUR ID
owners_ids = []  # OWNERS IDs
channel = "Darqwap"  # YOUR CHANNEL
owners_ids.insert(0, MAIN_OWNER)
users_db = "./users"
settings_db = "./settings"
admins_db = "./admins"


ADMINS_MARKUP = Markup(
    [
        [Button("- الاحصائيات -", callback_data="statics")],
        [
            Button("- اضافة مستخدم -", callback_data="adduser"),
            Button("- حذف مستخدم -", callback_data="popuser"),
        ],
        [Button("- الوضع الحالي : {} -", callback_data="changemode")],
        [Button("- الادمنيه -", callback_data="get_admins")],
        [
            Button("- اضافة ادمن -", callback_data="add_admin"),
            Button("- حذف ادمن -", callback_data="pop_admin"),
        ],
        [Button("- اذاعه -", callback_data="broadcast")],
        [Button("- الاشتراك الاجباري -", callback_data="force_sub")],
        [Button("- اظهار لوحة الاعضاء -", callback_data="users")],
    ]
)


TO_ADMINS_MARKUP = Markup([[Button("- رجوع -", callback_data="admins")]])


START_MARKUP = Markup(
    [
        [Button("( بحث بالإسم ) ", callback_data="start_sh_name")],
        [Button("( بحث بالرقم )", callback_data="start_sh_phone")],
    ]
)

SH_PHONE_MARKUP = Markup(
    [
        [
            Button("- (بحث آسيا) -", callback_data="sh_phone Asiacell"),
        ],
        [
            Button("- (بحث زين) -", callback_data="sh_phone zain"),
        ],
        [Button("- (بحث الكل) -", callback_data="sh_phone all")],
        [Button("( رجوع ) 🔙", callback_data="users")],
    ]
)

SH_NAME_MARKUP = Markup(
    [
        [
            Button("- (بحث آسيا) -", callback_data="sh_name Asiacell"),
        ],
        [
            Button("- (بحث زين) -", callback_data="sh_name zain"),
        ],
        [Button("- (بحث الكل) -", callback_data="sh_name all")],
        [Button("( رجوع ) 🔙", callback_data="users")],
    ]
)

TO_USERS_MARKUP = Markup([[Button("- رجوع -", callback_data="users")]])


@ben.message_handler(
    commands=["start"],
    chat_types=["private"],
)
def owners_start(message: Message):
    user_id = message.from_user.id
    if user_id in owners_ids + admins:
        mode = "مدفوع" if settings["mode"] == "private" else "مجاني"
        markup = ADMINS_MARKUP
        markup.keyboard[2][0].text = "- الوضع الحالي : {} -".format(mode)
        ben.reply_to(
            message,
            "- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :",
            reply_markup=markup,
        )
    else:
        if users.get(str(user_id)) is None:
            users[str(user_id)] = False
            write(users_db, users)
            ben.send_message(
                MAIN_OWNER,
                "- دخل شخص جديد الى البوت 🔥\n\n- ايديه : %s\n- معرفه: %s\n\n- عدد المستخدمين الكلي: %s"
                % (
                    user_id,
                    (
                        "@" + message.from_user.username
                        if message.from_user.username
                        else "لا يوجد"
                    ),
                    len(users),
                ),
            )
        subscribed = subscription(user_id)
        if subscribed is None:
            return ben.reply_to(
                message,
                "- 🛑 | عذرا عزيزي عليك الاشتراك بقناة البوت أولا..",
                reply_markup=Markup(
                    [[Button("- اشتراك -", url="t.me/%s" % settings["channel"])]]
                ),
            )
        if users.get(str(user_id)) is None:
            users[str(user_id)] = False
            write(users_db, users)
        ben.reply_to(
            message,
            "| : | مرحبا بك عزيزي في بوت بيانات الارقام العراقية..\
             \n| : | يمكنك البحث في جميع قواعد البيانات.. 🔍",
            reply_markup=START_MARKUP,
        )


@ben.callback_query_handler(
    func=lambda call: call.data in ["adduser", "popuser", "add_admin", "pop_admin"]
)
def add_pop_user(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins:
            return ben.edit_message_text(
                message_id=callback.message.id,
                chat_id=user_id,
                text="- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات",
            )
        else:
            if callback.data in ["add_admin", "pop_admin"]:
                return ben.answer_callback_query(
                    callback.id, "- لا يمكنك استخدام هذه الميزهّ!", show_alert=True
                )
    settings["get_id"][str(user_id)] = callback.data
    write(settings_db, settings)
    ben.edit_message_text(
        message_id=callback.message.id,
        chat_id=user_id,
        text="- حسنا عزيزي قم بارسال ايدي المستخدم!",
        reply_markup=TO_ADMINS_MARKUP,
    )


@ben.callback_query_handler(func=lambda call: call.data == "changemode")
def change_mode(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in owners_ids + admins:
        return ben.edit_message_text(
            message_id=callback.message.id,
            chat_id=user_id,
            text="- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات",
        )
    settings["mode"] = "public" if settings["mode"] == "private" else "private"
    write(settings_db, settings)
    mode = "مدفوع" if settings["mode"] == "private" else "مجاني"
    ben.answer_callback_query(callback.id, f"- تم تغيير الوضع الى {mode}")
    markup = ADMINS_MARKUP
    markup.keyboard[2][0].text = "- الوضع الحالي : {} -".format(mode)
    ben.edit_message_text(
        message_id=callback.message.id,
        chat_id=user_id,
        text="- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :",
        reply_markup=markup,
    )


@ben.callback_query_handler(func=lambda call: call.data == "admins")
def to_admins(callback: CallbackQuery):
    user_id = callback.from_user.id
    for setting in settings:
        if setting in ["mode", "channel"]:
            continue
        elif setting in [
            "get_num",
            "get_name_asia",
            "get_name_zain",
            "get_name_all",
            "get_all",
            "get_broadcast",
            "get_channel",
            "get_zain",
        ]:
            if user_id in settings[setting]:
                settings[setting].remove(user_id)
        elif settings[setting].get(str(user_id)):
            del settings[setting][str(user_id)]
    if user_id not in owners_ids + admins:
        return ben.edit_message_text(
            message_id=callback.message.id,
            chat_id=user_id,
            text="- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات",
        )
    mode = "مدفوع" if settings["mode"] == "private" else "مجاني"
    markup = ADMINS_MARKUP
    markup.keyboard[2][0].text = "- الوضع الحالي : {} -".format(mode)
    ben.edit_message_text(
        message_id=callback.message.id,
        chat_id=user_id,
        text="- مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :",
        reply_markup=markup,
    )


@ben.message_handler(
    content_types=["text"],
    chat_types=["private"],
    func=lambda msg: settings["get_id"].get(str(msg.from_user.id)),
)
def get_id(message: Message):
    data = settings["get_id"][str(message.from_user.id)]
    if data == "adduser":
        if users.get(message.text):
            ben.reply_to(
                message, "- العضو موجود بالبوت من قبل!", reply_markup=TO_ADMINS_MARKUP
            )
        else:
            users[message.text] = True
            write(users_db, users)
            ben.reply_to(
                message, "- تم اضافة العضو للبوت بنجاح!", reply_markup=TO_ADMINS_MARKUP
            )
    elif data == "popuser":
        if users.get(message.text) is None:
            ben.reply_to(
                message,
                "- العضو غير موجود بالبوت ليتم حذفه!",
                reply_markup=TO_ADMINS_MARKUP,
            )
        else:
            users[message.text] = False
            write(users_db, users)
            ben.reply_to(
                message, "- تم حذف العضو من البوت!", reply_markup=TO_ADMINS_MARKUP
            )
    elif data == "add_admin":
        if not message.text.isnumeric():
            ben.reply_to(message, "- الايدي غير صالح!", reply_markup=TO_ADMINS_MARKUP)
        elif int(message.text) in admins:
            ben.reply_to(
                message, "- الادمن موجود بالبوت من قبل!", reply_markup=TO_ADMINS_MARKUP
            )
        else:
            try:
                ben.get_chat(int(message.text))
            except:
                ben.reply_to(
                    message,
                    "- لم يتم ايجاد هذا المستخدم!",
                    reply_markup=TO_ADMINS_MARKUP,
                )
                del settings["get_id"][str(message.from_user.id)]
                write(settings_db, settings)
                return
            admins.append(int(message.text))
            write(admins_db, admins)
            ben.reply_to(
                message,
                "- تم اضافة المستخدم لقائمة الادمنيه!",
                reply_markup=TO_ADMINS_MARKUP,
            )
    elif data == "pop_admin":
        if not message.text.isnumeric():
            ben.reply_to(message, "- الايدي غير صالح!", reply_markup=TO_ADMINS_MARKUP)
        elif int(message.text) not in admins:
            ben.reply_to(
                message,
                "- المستخدم ليس من ادمنية البوت!",
                reply_markup=TO_ADMINS_MARKUP,
            )
        else:
            try:
                ben.get_chat(int(message.text))
            except:
                ben.reply_to(
                    message,
                    "- لم يتم ايجاد هذا المستخدم!",
                    reply_markup=TO_ADMINS_MARKUP,
                )
                del settings["get_id"][str(message.from_user.id)]
                write(settings_db, settings)
                return
            admins.remove(int(message.text))
            write(admins_db, admins)
            ben.reply_to(
                message,
                "- تم حذف المستخدم من قائمة الادمنيه",
                reply_markup=TO_ADMINS_MARKUP,
            )
    del settings["get_id"][str(message.from_user.id)]
    write(settings_db, settings)


@ben.callback_query_handler(
    func=lambda callback: callback.data == "statics"
    and callback.from_user.id in (owners_ids + admins)
)
def statics(callback: CallbackQuery):
    ben.answer_callback_query(
        callback.id, "- جاري الحصول على البيانات... -", show_alert=True
    )
    caption = "- حسنا عزيزي اليك احصائيات البوت!\n\n"
    vips = 0
    norm = 0
    for user in users:
        if users[user]:
            vips += 1
        else:
            norm += 1
    caption += "- عدد المستخدمين الكلي: %s\n" % len(users)
    caption += "- عدد المستخدمين المشتركين بالبوت: %s\n" % vips
    caption += "- عدد المستخدمين غير المشتركين بالبوت: %s\n" % norm
    ben.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.id,
        text=caption,
        reply_markup=TO_ADMINS_MARKUP,
    )


@ben.callback_query_handler(
    func=lambda callback: callback.data == "get_admins"
    and callback.from_user.id in (owners_ids + admins)
)
def get_admins(callback: CallbackQuery):
    ben.answer_callback_query(
        callback.id, "- جاري الحصول على البيانات... -", show_alert=True
    )
    caption = "- حسنا عزيزي اليك ادمنية البوت!\n\n"
    for admin in admins:
        user = ben.get_chat(admin)
        caption += "- [%s](https://t.me/%s)\n" % (user.first_name, user.username)
    ben.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.id,
        text=caption,
        reply_markup=TO_ADMINS_MARKUP,
        disable_web_page_preview=True,
        parse_mode="MARKDOWN",
    )


@ben.callback_query_handler(
    func=lambda callback: callback.data == "broadcast"
    and callback.from_user.id in (owners_ids + admins)
)
def broadcast(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins:
            return ben.edit_message_text(
                message_id=callback.message.id,
                chat_id=user_id,
                text="- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات",
            )
        else:
            return ben.answer_callback_query(
                callback.id, "- لا يمكنك استخدام هذه الميزهّ!", show_alert=True
            )
    settings["get_broadcast"].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        chat_id=user_id,
        message_id=callback.message.id,
        text="- حسنا عزيزي قم بارسال رسالة الاذاعه الان.",
        reply_markup=TO_ADMINS_MARKUP,
    )


@ben.message_handler(
    chat_types=["private"],
    content_types=["photo", "text", "audio", "voice", "video", "sticker", "document"],
    func=lambda message: message.from_user.id in settings["get_broadcast"],
)
def get_broadcast(message: Message):
    user_id = message.from_user.id
    settings["get_broadcast"].remove(user_id)
    write(settings_db, settings)
    ben.reply_to(message, "- جاري الاذاعه!", reply_markup=TO_ADMINS_MARKUP)
    banned_me = 0
    for user in users:
        try:
            ben.copy_message(
                chat_id=int(user), from_chat_id=user_id, message_id=message.id
            )
        except:
            banned_me += 1
    ben.reply_to(
        message,
        "- تمت الاذاعه بنجاح الى : %s\n\n- الاشخاص الذين قاموا بحظر البوت: %s"
        % (len(users) - banned_me, banned_me),
    )


@ben.callback_query_handler(
    func=lambda callback: callback.data == "force_sub"
    and callback.from_user.id in owners_ids + admins
)
def force_sub(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in owners_ids + admins:
        return ben.edit_message_text(
            message_id=callback.message.id,
            chat_id=user_id,
            text="- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات",
        )
    ben.edit_message_text(
        chat_id=user_id,
        message_id=callback.message.id,
        text="- قناة الاشتراك الحاليه : @%s\n- يمكنك تغيير قناة الاشتراك من خلال الزر التالي: "
        % (settings["channel"]),
        reply_markup=Markup(
            [
                [Button("- تغيير قناة الاشتراك -", callback_data="change_force")],
                [Button("- رجوع -", callback_data="admins")],
            ]
        ),
    )


@ben.callback_query_handler(
    func=lambda callback: callback.data == "change_force"
    and callback.from_user.id in owners_ids + admins
)
def change_force(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in owners_ids:
        if user_id not in admins:
            return ben.edit_message_text(
                message_id=callback.message.id,
                chat_id=user_id,
                text="- عذرا عزيزي لم يعد بامكانك الوصول لهذه الصلاحيات",
            )
        else:
            return ben.answer_callback_query(
                callback.id, "- لا يمكنك استخدام هذه الميزهّ!", show_alert=True
            )
    settings["get_channel"].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        chat_id=user_id,
        message_id=callback.message.id,
        text="- حسنا عزيزي قم بارسال قناة الاشتراك الجديده",
        reply_markup=TO_ADMINS_MARKUP,
    )


@ben.message_handler(
    content_types=["text"],
    chat_types=["private"],
    func=lambda message: message.from_user.id in settings["get_channel"],
)
def get_channel(message: Message):
    user_id = message.from_user.id
    settings["get_channel"].remove(user_id)
    write(settings_db, settings)
    nchannel = (
        message.text.replace("http", "")
        .replace("https", "")
        .replace("t.me", "")
        .replace("/", "")
        .replace("@", "")
    )
    try:
        ben.get_chat("@" + nchannel)
    except:
        return ben.reply_to(
            message,
            "- عذرا عزيزي لم استطع الوصول لهذه القناه",
            reply_markup=TO_ADMINS_MARKUP,
        )
    settings["channel"] = nchannel
    write(settings_db, settings)
    ben.reply_to(
        message,
        "- تم تحديث قناة الاشتراك الاجباري!\n\n- تأكد من رفعي مشرف بالقناه الجديده!",
        reply_markup=TO_ADMINS_MARKUP,
    )
    ben.send_message(
        MAIN_OWNER,
        "- تم تغيير قناة الاشتراك الاجباري بواسطة : [%s](t.me/%s)"
        % (message.from_user.first_name, message.from_user.username),
    )


@ben.callback_query_handler(func=lambda call: call.data == "start_sh_phone")
def start_sh_phone(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not users.get(str(user_id)) and settings["mode"] == "private":
        ben.answer_callback_query(
            callback.id,
            "🛑 | عذرا عزيزي يجب عليك الاشتراك من خلال المالك..",
            show_alert=True,
        )
        return
    ben.edit_message_text(
        "🔍 |  اختر قاعدة البيانات المناسبة للبحث من فضلك..",
        user_id,
        callback.message.id,
        reply_markup=SH_PHONE_MARKUP,
    )


@ben.callback_query_handler(func=lambda call: call.data == "start_sh_name")
def start_sh_phone(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not users.get(str(user_id)) and settings["mode"] == "private":
        ben.answer_callback_query(
            callback.id,
            "🛑 | عذرا عزيزي يجب عليك الاشتراك من خلال المالك..",
            show_alert=True,
        )
        return
    ben.edit_message_text(
        "🔍 |  اختر قاعدة البيانات المناسبة للبحث من فضلك..",
        user_id,
        callback.message.id,
        reply_markup=SH_NAME_MARKUP,
    )


@ben.callback_query_handler(func=lambda call: call.data.startswith("sh_phone"))
def sh_phone(callback: CallbackQuery):
    user_id = callback.from_user.id
    type = (
        "get_num"
        if "Asia" in callback.data
        else ("get_zain" if "all" not in callback.data else "get_all")
    )
    print(type)
    settings[type].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.from_user.id,
        text="🔍 | حسنا عزيزي قم بإرسال رقم هاتف الشخص..",
        reply_markup=TO_USERS_MARKUP,
    )


@ben.callback_query_handler(func=lambda call: call.data.startswith("sh_name"))
def sh_name(callback: CallbackQuery):
    user_id = callback.from_user.id
    settings[
        (
            "get_name_asia"
            if "Asia" in callback.data
            else ("get_name_zain" if "all" not in callback.data else "get_name_all")
        )
    ].append(user_id)
    write(settings_db, settings)
    ben.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.from_user.id,
        text="🔍 | حسنا عزيزي قم بإرسال اسم اسم الشخص..",
        reply_markup=TO_USERS_MARKUP,
    )


@ben.message_handler(
    content_types=["text"],
    chat_types=["private"],
    func=lambda msg: msg.from_user.id
    in (
        settings["get_num"]
        + settings["get_zain"]
        + settings["get_all"]
        + settings["get_name_all"]
        + settings["get_name_asia"]
        + settings["get_name_zain"]
    ),
)
def get_data(message: Message):
    user_id = message.from_user.id
    type = (
        "zain"
        if user_id in settings["get_zain"] or user_id in settings["get_name_zain"]
        else (
            "asia"
            if user_id in settings["get_num"] or user_id in settings["get_name_asia"]
            else "all"
        )
    )
    print(type)
    if user_id in settings["get_zain"] + settings["get_num"] + settings["get_all"]:
        settings[(
            "get_zain"
            if type == "zain"
            else ("get_num" if type == "asia" else "get_all")
        )].remove(user_id)
        is_phone = True
    else:
        settings[
            (
                "get_name_zain"
                if type == "zain"
                else ("get_name_asia" if type == "asia" else "get_name_all")
            )
        ].remove(user_id)
        is_phone = False
    write(settings_db, settings)
    if is_phone:
        phone = message.text
        if type == "asia":
            phone = phone[1] + "." + phone[2:]
    else:
        full_name = message.text
        if len(full_name.split()) not in [2, 3]:
            return ben.reply_to(
                message,
                "❌ | الاسم غير صح",
                reply_markup=TO_USERS_MARKUP,
            )
    wait = ben.reply_to(message, "🔍 | جاري البحث..")
    if type == "asia":
        if is_phone:
            query = f'SELECT * FROM MAIN_DATA WHERE PHONE LIKE "{phone}%"'
        else:
            query = f'SELECT * FROM MAIN_DATA WHERE NAME LIKE "{full_name}%"'
    elif type == "zain":
        if is_phone:
            query = f'SELECT * FROM info WHERE phone LIKE "{phone}%"'
        else:
            query = f'SELECT * FROM info WHERE name LIKE "{full_name}%"'
    else:
        if is_phone:
            query1 = f'SELECT * FROM MAIN_DATA WHERE PHONE LIKE "{phone}%"'
            query2 = f'SELECT * FROM info WHERE phone LIKE "{phone}%"'
        else:
            query1 = f'SELECT * FROM MAIN_DATA WHERE NAME LIKE "{full_name}%"'
            query2 = f'SELECT * FROM info WHERE name LIKE "{full_name}%"'
    if type != "all":
        connection = sqlite3.connect("zain.db" if type == "zain" else "Asiacell.db")
        connection.text_factory = str
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    else:
        connection1 = sqlite3.connect("Asiacell.db")
        connection1.text_factory = str
        cursor1 = connection1.cursor()
        try:
            cursor1.execute(query1)
            rows1 = cursor1.fetchall()
        except:
            rows1 = []
        connection2 = sqlite3.connect("zain.db")
        connection2.text_factory = str
        cursor2 = connection2.cursor()
        try:
            cursor2.execute(query2)
            rows2 = cursor2.fetchall()
        except:
            rows2 = []
        sperator = len(rows1) - 1 if len(rows1) < 1 else 0
        rows = rows1 + rows2
    if not len(rows) or rows is None or rows == False:
        return ben.edit_message_text(
            message_id=wait.id,
            chat_id=user_id,
            text="❌ | لم يتم ايجاد اي نتائج..",
            reply_markup=TO_USERS_MARKUP,
        )
    index = 1
    for row in rows:
        row = list(row)
        ctype = (
            "zain"
            if type == "all" and index > sperator
            else ("asia" if type == "all" and index <= sperator else type)
        )
        try:
            ben.reply_to(
                message,
                (
                    "[ ] الاسم الثلاثي: [ `%s` ]\n[ ] المحافظه : [ `%s` ]\n[ ] رقم البطاقه : [ `%s` ]\n[ ] تاريخ الميلاد: [ `%s` ]\n[ ] رقم الهاتف : [ `%s` ]"
                    % (
                        row[0],
                        row[1],
                        row[-1] if row[-1] != "" else "غير معروف",
                        row[3][:8],
                        "0" + row[2].replace(".", "")[:10],
                    )
                    if ctype != "zain"
                    else "[ ] الإسم الثلاثي: [ `%s` ]\n[ ] رقم الهاتف : [ `%s` ]\n[ ] كود الدولة: [ +964 ]\n[ ] نوع الخط: [ زين العراق ]\n[ ] العنوان : [ `%s` ]"
                    % (row[1], row[0], row[-1])
                ),
            )
        except apihelper.ApiTelegramException as e:
            if (
                "A request to the Telegram API was unsuccessful. Error code: 429. Description: Too Many Requests: retry after"
                in str(e)
            ):
                time = int(str(e).rsplit(maxsplit=1)[1])
                sleep(time)
                ben.reply_to(
                    message,
                    (
                        "[ ] الاسم الثلاثي: [ `%s` ]\n[ ] المحافظه : [ `%s` ]\n[ ] رقم البطاقه : [ `%s` ]\n[ ] تاريخ الميلاد: [ `%s` ]\n[ ] رقم الهاتف : [ `%s` ]"
                        % (
                            row[0],
                            row[1],
                            row[-1] if row[-1] != "" else "غير معروف",
                            row[3][:8],
                            "0" + row[2].replace(".", "")[:10],
                        )
                        if ctype != "zain"
                        else "[ ] الإسم الثلاثي: [ `%s` ]\n[ ] رقم الهاتف : [ `%s` ]\n[ ] كود الدولة: [ +964 ]\n[ ] نوع الخط: [ زين العراق ]\n[ ] العنوان : [ `%s` ]"
                        % (row[1], row[0], row[-1])
                    ),
                )
                continue
            else:
                ben.reply_to(message, "❌ | حدث خطأ ما أثناء البحث..")
                continue
        index += 1
    if type == "all":
        connection1.close()
        connection2.close()
    else:
        connection.close()
    ben.delete_message(user_id, wait.id)
    ben.reply_to(message, "✔ | انتهى البحث..", reply_markup=TO_USERS_MARKUP)


@ben.callback_query_handler(func=lambda call: call.data == "users")
def to_users(callback):
    user_id = callback.from_user.id
    for setting in settings:
        if setting in ["mode", "channel"]:
            continue
        elif setting in [
            "get_num",
            "get_name_asia",
            "get_name_zain",
            "get_name_all",
            "get_all",
            "get_broadcast",
            "get_channel",
            "get_zain",
        ]:
            if user_id in settings[setting]:
                settings[setting].remove(user_id)
        elif settings[setting].get(str(user_id)):
            del settings[setting][str(user_id)]
    ben.edit_message_text(
        message_id=callback.message.id,
        chat_id=user_id,
        text="| : | مرحبا بك عزيزي في بوت بيانات الارقام العراقية..\
             \n| : | يمكنك البحث في جميع قواعد البيانات.. 🔍",
        reply_markup=START_MARKUP,
    )


read = lambda path: load(open(path))
write = lambda path, data: dump(data, open(path, "w"), indent=4, ensure_ascii=False)


def subscription(user_id):
    try:
        member = ben.get_chat_member("@" + settings["channel"], user_id)
    except:
        return ben.send_message(MAIN_OWNER, "- هناك مشكله بالاشتراك الاجباري")
    if member.status in ["creator", "member", "administrator"]:
        return True
    return


def main():
    global users, settings, admins
    import os

    if not os.path.exists(users_db):
        write(users_db, {})
    if not os.path.exists(settings_db):
        write(
            settings_db,
            {
                "mode": "private",
                "get_id": {},
                "get_name_asia": [],
                "get_name_zain": [],
                "get_name_all": [],
                "get_broadcast": [],
                "channel": channel,
                "get_channel": [],
                "get_num": [],
                "get_zain": [],
                "get_all": [],
            },
        )
    if not os.path.exists(admins_db):
        write(admins_db, [])
    settings = read(settings_db)
    for setting in settings:
        if isinstance(settings[setting], list):
            settings[setting] = []
    write(settings_db, settings)
    users = read(users_db)
    admins = read(admins_db)
    print("[+] Started")
    ben.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
# 𝗪𝗥𝗜𝗧𝗧𝗘𝗡 𝗕𝗬 : @ppppp_pf
# 𝗦𝗢𝗨𝗥𝗖𝗘 : @O780000
