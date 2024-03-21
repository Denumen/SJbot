    elif DEF_CHECK_MARKETER(MESSAGE_CHATID):
    
        if message.caption :
            MESSAGE_TEXT = message.caption
        elif message.text :
            MESSAGE_TEXT = message.text
        else :
            return
                        
        if MESSAGE_TEXT in ["🔙 cancel" , "/cancel" , "cancel" , "❌ NO ,forget."]  :
            await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER)
            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
            return
        
        
        CHECK_STEP = DEF_CHECK_STEP(MESSAGE_CHATID)
        if CHECK_STEP == "None" :

            if MESSAGE_TEXT == "/start" :
                TEXT = f"""
                تبریک میگم شما با موفقیت به جمع همکاران ما اضافه شدید ! 
                درصورتی که به هرگونه آموزش و یا پشتیبانی نیاز داشتید میتونید به آیدی زیر پیام بدید:
                @suppvm"""
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)

            elif MESSAGE_TEXT == "💬 پشتیبانی" :
                TEXT = f"""
                درصورت نیاز به راهنمایی به آیدی پشتیبانی پیام بدید :
                @suppvm"""
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)
            
            elif MESSAGE_TEXT == "💰 چک کردن اعتبار" :

                # Construct the SQL command to update the user's credit
                sql_command = f"SELECT Credit FROM users WHERE chatid = '{MESSAGE_CHATID}';"

                # Execute the SQL command using the subprocess module
                result = subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], capture_output=True, text=True)

                # Extract the output from the result
                output = result.stdout.strip()

                TEXT = f"""
                اعتبار شما {output} تومان میباشد.
                برای شارژ حساب خود به آیدی پشتیبانی پیام بدید:
                @suppvm"""
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)

            elif MESSAGE_TEXT == "🖼 QR Code" :
                TEXT = "<b>جهت دریافت کد تصویری، لینک سابسکرایب مدنظر خود را وارد نمایید.</b>"
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"qrcode | wait to send link")

            elif MESSAGE_TEXT == "🔍 جستجو" :
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please send me the words.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"search | wait to send words")

            elif MESSAGE_TEXT == "👤 شارژ حساب نماینده" :
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>جهت شارژ حساب نماینده فروش رمز اختصاصی خودرا وارد کنید.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"charge | wait to send credit")
            
            elif MESSAGE_TEXT == "👨🏻‍💻 افزوندن نماینده فروش" :
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>please enter passcode for adding marketer.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"marketer | wait to add marketer")

            elif MESSAGE_TEXT == "👨🏻‍💻 ادمین ها" :
                KEYBOARD_ADMINS = KEYBOARD_ADMINS_LIST(MESSAGE_CHATID)
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select an admin or add a new admin?</b>" , reply_markup=KEYBOARD_ADMINS , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"admins | wait to select or add admin")

            elif MESSAGE_TEXT == "👤 کاربران" :
                WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>لطفا صبور باشید ... ⏳️</b>" , reply_markup=ReplyKeyboardRemove() , parse_mode=enums.ParseMode.HTML)
                TEXT = DEF_ALL_USERS(MESSAGE_CHATID)
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_USERS , parse_mode=enums.ParseMode.HTML)               
                await WAIT_MESSGAE.delete()
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"users | wait to select list")

            elif MESSAGE_TEXT == "🎗 نود ها" :
                KEYBOARD_NODES_LIST = DEF_NODES_LIST(MESSAGE_CHATID)
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Please select node.</b>" , reply_markup=KEYBOARD_NODES_LIST, parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"nodes | wait to select node")

            elif MESSAGE_TEXT == "🎛 مانیتورینگ" :
                BOSS_CHATID , NODE_STATUS , CHECK_NORMAL , CHECK_ERROR = DEF_MONITORING_DATA()
                if NODE_STATUS == "off" :
                    TEXT = f"<b>🔴 Monitoring is <code>off</code></b>"
                    KEYBOARD_MONITORING = KEYBOARD_OFF_MONITORING
                else :
                    TEXT = f"<b>🟢 Monitoring is <code>on</code>\nMonitoring timer : <code>{CHECK_NORMAL} second</code>\nError timer : <code>{CHECK_ERROR} second</code></b>"
                    KEYBOARD_MONITORING = KEYBOARD_ON_MONITORING  
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | wait to select command")
                
            elif MESSAGE_TEXT == "🗃 قالب ها" :
                KEYBOARD_TEMPLATES = KEYBOARD_TEMPLATES_LIST()
                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>نام قالب را وارد کنید.\n(فقط حروف لاتین بدون عدد و ایموجی و غیره ...!)\nمثال :</b> <code>Test</code> ,<code>Ali</code>, <code>Bulk</code>, <code>Free</code>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"templates | wait to select command")
            
            elif MESSAGE_TEXT == "🚀 ساخت کاربر" :
                KEYBOARD_TEMPLATES = KEYBOARD_CREATE_LIST_MARKETER()
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>لطفا یکی از قالب ها را انتخاب کنید یا بصورت دستی کانفیگ مدنظر خودرا وارد کنید.</b>" , reply_markup=KEYBOARD_TEMPLATES , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"create | wait to select command")
                
            elif MESSAGE_TEXT == "🎖 Notice" :
                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>Welcome to the Messages section! This feature has been added with sponsorship the <a href='https://t.me/GrayServer'>Gray</a> collection.❤️ You can visit the Gray collection channel and bot for purchasing servers on an hourly and monthly basis, with a wide variety of locations and specifications, accompanied by clean IPs at the lowest prices.\n\nTo utilize this feature, you first need to create an inbound according to the tutorial on GitHub Wiki or the Telegram channel tutorial for SJbot. Then, in the host setting section of that inbound, write down the texts you desire to be displayed to the user upon completion of the configuration update.\n\nYour Messages is <code>{DEF_GET_MESSAGE_STATUS(MESSAGE_CHATID)}</code></b>" , reply_markup=KEYBOARD_MESSAGES , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"message | wait to select command")
                                
            else :
                TEXT = "<b>دستور مدنظر یافت نشد لطفا از دستورات پیشفرض استفاده نمایید.</b>"
                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)
            

        else :
            MESSAGES_SPLIT = MESSAGE_TEXT.strip().split(" ")
            STEP_SPLIT = CHECK_STEP.strip().split(" ")


            if CHECK_STEP.startswith("qrcode") :
                if CHECK_STEP == "qrcode | wait to send link" :
                    QRCODE_IMG = DEF_CREATE_QRCODE(MESSAGE_TEXT)
                    await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{MESSAGE_TEXT}</pre>" , reply_markup=KEYBOARD_HOME_MARKETER)
                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")


            elif CHECK_STEP.startswith("search") :
                if CHECK_STEP == "search | wait to send words" :
                    WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>لطفا صبور باشید ... ⏳️</b>" , reply_markup=ReplyKeyboardRemove() ,  parse_mode=enums.ParseMode.HTML)
                    TEXT = DEF_SEARCH_USERS(MESSAGE_CHATID , MESSAGE_TEXT)
                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)               
                    await WAIT_MESSGAE.delete()






            elif CHECK_STEP.startswith("marketer") :

                if CHECK_STEP == "marketer | wait to add marketer" :

                    if MESSAGE_TEXT == "112211" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>تلگرام آیدی مدنظر را وارد نمایید :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"marketer | manual")

                    elif re.match(r'(\w+) - ([0-9.]+) GB (\d+) days' , MESSAGE_TEXT) :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                    else:
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                else :

                    if CHECK_STEP.startswith("charge | select") :
                        TEMPLATE_NAME = STEP_SPLIT[3]
                    else :
                        if CHECK_STEP.startswith("marketer | manual") :

                            if len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 3 and len(MESSAGE_TEXT) > 2 :
                                USERNAME = MESSAGE_TEXT
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>مقدار اعتبار پایه مدنظر را بصورت عددی در واحد تومان وارد نمایید.\nمثال : <code>25.5</code>, <code>15</code>, <code>0.5</code>, <code>100</code></b></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"marketer | manual {MESSAGE_TEXT}")

                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 4 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                USERNAME = STEP_SPLIT[3]

                                sql_command = f"INSERT INTO users (chatid, role, name, username, password, domain, step, credit) VALUES ({USERNAME}, 'marketer', 'marketers', 'dfg392gt', 'q31Kt1H3r3N2', 'feed.farsroid.tech:2087', 'None', {MESSAGE_TEXT});"

                                # Execute the SQL command using the subprocess module
                                subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], check=True)
                                #await client.send_message(chat_id=MESSAGE_CHATID , text="<b>charge shod.\nمثال : <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)

                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"تبریک میگم ! نماینده فروش شما با موفقیت اضافه شد." , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")





            elif CHECK_STEP.startswith("charge") :

                if CHECK_STEP == "charge | wait to send credit" :

                    if MESSAGE_TEXT == "112211" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter credit values :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"charge | manual")

                    elif re.match(r'(\w+) - ([0-9.]+) GB (\d+) days' , MESSAGE_TEXT) :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                    else:
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                else :

                    if CHECK_STEP.startswith("charge | select") :
                        TEMPLATE_NAME = STEP_SPLIT[3]
                    else :
                        if CHECK_STEP.startswith("charge | manual") :

                            if len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 3 and len(MESSAGE_TEXT) > 2 :
                                USERNAME = MESSAGE_TEXT
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please charge enter data limit TOMAN.\nمثال : <code>25.5</code>, <code>15</code>, <code>0.5</code>, <code>100</code></b></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"charge | manual {MESSAGE_TEXT}")

                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 4 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                USERNAME = STEP_SPLIT[3]

                                sql_command = f"UPDATE users SET Credit = Credit - {MESSAGE_TEXT} WHERE chatid = {USERNAME};"

                                # Execute the SQL command using the subprocess module
                                subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], check=True)
                                #await client.send_message(chat_id=MESSAGE_CHATID , text="<b>charge shod.\nمثال : <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)

                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"Charge shod" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")





            elif CHECK_STEP.startswith("message") :
                
                if CHECK_STEP == "message | wait to select command" :
                    if MESSAGE_TEXT == "👀 change status" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=DEF_CHANGE_MESSAGER_STATUS(MESSAGE_CHATID) , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")






            elif CHECK_STEP.startswith("admins") :

                if CHECK_STEP == "admins | wait to select or add admin" :

                    if re.search(r"- (SUDO|N\.SUDO)", MESSAGE_TEXT) and len(MESSAGES_SPLIT) == 3 :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select command.</b>" , reply_markup=KEYBOARD_ADMIN , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected admin {MESSAGES_SPLIT[0]} {MESSAGES_SPLIT[2]}")
                    
                    elif MESSAGE_TEXT == "➕ Add new admin" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter new admin username :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | add admin")

                else :

                    if CHECK_STEP.startswith("admins | selected") :

                        if CHECK_STEP.startswith("admins | selected admin") :
                            ADMIN_NAME , ADMIN_SUDO = STEP_SPLIT[4:]

                            if MESSAGE_TEXT == "🔐 Change pass" :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>What is the new password of this admin?</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected change password {ADMIN_NAME} {ADMIN_SUDO}")
                            
                            elif MESSAGE_TEXT == "🔐 Change sudo" :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>are you sure?</b>" , reply_markup=KEYBOARD_YES_OR_NOO , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected change sudo {ADMIN_NAME} {ADMIN_SUDO}")

                            elif MESSAGE_TEXT == "🗑 Delete admin" :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>What!!! are you really?</b>" , reply_markup=KEYBOARD_YES_OR_NOO , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | selected delete this {ADMIN_NAME} {ADMIN_SUDO}")
                        
                        else :
        
                            ADMIN_NAME , ADMIN_SUDO = STEP_SPLIT[5:]
                            if CHECK_STEP.startswith("admins | selected change password") :
                                TEXT = DEF_CHANGE_PASSWORD(MESSAGE_CHATID , ADMIN_NAME , ADMIN_SUDO , MESSAGE_TEXT)
                                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

                            elif CHECK_STEP.startswith("admins | selected change sudo") :
                                if MESSAGE_TEXT == "✅ YES , sure!" :
                                    TEXT = DEF_CHANGE_SUDO(MESSAGE_CHATID,ADMIN_NAME,ADMIN_SUDO,MESSAGE_TEXT)
                                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                            
                            elif CHECK_STEP.startswith("admins | selected delete this") :
                                if MESSAGE_TEXT == "✅ YES , sure!" :
                                    TEXT = DEF_DELETE_ADMIN(MESSAGE_CHATID,ADMIN_NAME)
                                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                    UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                    
                    elif CHECK_STEP.startswith("admins | add admin") :
                        
                        if len(STEP_SPLIT) == 4 :
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter new admin password :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | add admin {MESSAGE_TEXT}")
                        
                        elif len(STEP_SPLIT) == 5 :
                            ADMIN_NAME = STEP_SPLIT[4] 
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select admin is sudo or not?</b>" , reply_markup=KEYBOARD_SUDO , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"admins | add admin {ADMIN_NAME} {MESSAGE_TEXT}")

                        elif len(STEP_SPLIT) == 6 :
                            ADMIN_NAME = STEP_SPLIT[4] 
                            ADMIN_PASS = STEP_SPLIT[5]
                            ADMIN_SUDO = MESSAGE_TEXT == "✅ YES , is sudo!"
                            TEXT = DEF_ADD_ADMIN(MESSAGE_CHATID,ADMIN_NAME,ADMIN_PASS,ADMIN_SUDO)
                            await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                

            elif CHECK_STEP.startswith("users") :

                if CHECK_STEP == "users | wait to select list" :
                
                    if MESSAGE_TEXT in ["✅ Active list" , "❌ Disabled list" , "🕰 Expired" , "🪫 Limited" , "🔌 On Hold"] :
                        WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>لطفا صبور باشید ... ⏳️</b>" , reply_markup=ReplyKeyboardRemove())
                        USERS_LIST = DEF_USERS_LIST_STATUS(MESSAGE_TEXT , MESSAGE_CHATID)
                
                        if not USERS_LIST :
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>هیچ کاربری پیدا نشد. ❌</b>" , reply_markup=KEYBOARD_USERS)
                            await WAIT_MESSGAE.delete()
                            return
                
                        else :
                            PDF_NAME = DEF_CREATE_PDF(USERS_LIST)
                            await client.send_document(chat_id=MESSAGE_CHATID , document=PDF_NAME ,caption=f"<b>List of {len(USERS_LIST)} users</b>" ,file_name=f"suppvm.pdf" , reply_markup=KEYBOARD_USERS)
                            await WAIT_MESSGAE.delete()
                            if os.path.exists(PDF_NAME):
                                os.remove(PDF_NAME)   
                
                    elif MESSAGE_TEXT in [ "👀 Online time list" , "📡 Sub Update list"] :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please select time.</b>" , reply_markup=KEYBOARD_LIST_TIMES)
                        CATAGORY = {"📡 Sub Update list": "sub_updated_at", "👀 Online time list": "online_at"}.get(MESSAGE_TEXT)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID, f"users | wait to time {CATAGORY}")                
                
                else :

                    if CHECK_STEP.startswith("users | wait to time") :
                        

                        if re.match(r'^\d+\s(min|hour|day)$' , MESSAGE_TEXT) :
                            TIME = DEF_CONVERT_TO_SECEND(MESSAGE_TEXT)
                            CATAGORY = STEP_SPLIT[5]
                            WAIT_MESSGAE = await client.send_message(chat_id=MESSAGE_CHATID, text=f"<b>لطفا صبور باشید ... ⏳️</b>" , reply_markup=ReplyKeyboardRemove())
                            USERS_LIST_BACK ,  NOT_USER_LIST = DEF_USERS_TIME_LIST(MESSAGE_CHATID , CATAGORY , TIME)
                            
                            if not USERS_LIST_BACK :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>هیچ کاربری پیدا نشد. ❌</b>" , reply_markup=KEYBOARD_LIST_TIMES)
                            else :
                                USERS_LIST_BACK_PDF = DEF_CREATE_PDF(USERS_LIST_BACK)
                                await client.send_document(chat_id=MESSAGE_CHATID , document=USERS_LIST_BACK_PDF ,caption=f"<b>List of {len(USERS_LIST_BACK)} users</b>" ,file_name=f"suppvm.pdf" , reply_markup=KEYBOARD_LIST_TIMES)
                                if os.path.exists(USERS_LIST_BACK_PDF):
                                    os.remove(USERS_LIST_BACK_PDF)
                            
                            if not NOT_USER_LIST :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>هیچ کاربری پیدا نشد. ❌</b>" , reply_markup=KEYBOARD_LIST_TIMES)
                            else :
                                NOT_IN_LIST_PDF = DEF_CREATE_PDF(NOT_USER_LIST)
                                await client.send_document(chat_id=MESSAGE_CHATID , document=NOT_IN_LIST_PDF ,caption=f"<b>other List of {len(NOT_USER_LIST)} users</b>" ,file_name=f"suppvm.pdf" , reply_markup=KEYBOARD_LIST_TIMES)
                                if os.path.exists(NOT_IN_LIST_PDF):
                                    os.remove(NOT_IN_LIST_PDF)
                            
                            await WAIT_MESSGAE.delete()


            elif CHECK_STEP.startswith("nodes") :

                if CHECK_STEP == "nodes | wait to select node" :
                    
                    if re.match('\(\s*(\d+)\s*\)\s*([^-]+)\s*-\s*([^-]+)', MESSAGE_TEXT) :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>You have chosen {MESSAGES_SPLIT[3]} server.\nwhat operation do you need?</b>" , reply_markup=KEYBOARD_NODE)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"nodes | select node {MESSAGES_SPLIT[1]}")

                else :

                    if CHECK_STEP.startswith("nodes | select node") :
                        NODE_ID = int(STEP_SPLIT[4])

                        if MESSAGE_TEXT == "🔏 Usage Coefficient" :
                            TEXT = "<b>Plase enter a float (0.0) number.\nlike this :</b> <code>0.4</code> , <code>1.2</code> , <code>3.5</code> , <code>8.0</code>"
                            await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"nodes | Usage Coefficient {NODE_ID}")
                            
                        else :

                            if MESSAGE_TEXT == "📊 Status" :
                                TEXT = DEF_STASE_NODE(MESSAGE_CHATID , NODE_ID)
                            elif MESSAGE_TEXT == "✅ Activate" :
                                TEXT = DEF_ACTIVE_NODE(MESSAGE_CHATID , NODE_ID)
                            elif MESSAGE_TEXT == "⚡️ Reconnect" :
                                TEXT = DEF_RECONNECT_NODE(MESSAGE_CHATID , NODE_ID)
                            elif MESSAGE_TEXT == "❌ Disable" :
                                TEXT = DEF_DISABLED_NODE(MESSAGE_CHATID , NODE_ID)

                            await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_NODE , parse_mode=enums.ParseMode.HTML)

                    else :

                        if CHECK_STEP.startswith("nodes | Usage Coefficient") :
                            NODE_ID = int(STEP_SPLIT[4])
                            
                            if len(MESSAGES_SPLIT) == 1 and re.match(r'^-?\d+\.\d+$', MESSAGE_TEXT) :
                                TEXT = DEF_USAGE_COEFFICIENT(float(MESSAGE_TEXT) , MESSAGE_CHATID , NODE_ID)
                                await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_NODE , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"nodes | select node {NODE_ID}")


            elif CHECK_STEP.startswith("monitoring") :

                if CHECK_STEP == "monitoring | wait to select command" :

                    if MESSAGE_TEXT == "🔴 Disable monitoring" :
                        CHANGE = DEF_CHANGE_NODE_STATUS(MESSAGE_CHATID,"off")
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>✅ Your Monitoring is disabled.</b>" , reply_markup=KEYBOARD_OFF_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )

                    elif MESSAGE_TEXT == "🟢 Monitoring activation" :
                        CHANGE = DEF_CHANGE_NODE_STATUS(MESSAGE_CHATID,"on")
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>✅ Your Monitoring is activated.</b>" , reply_markup=KEYBOARD_ON_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                    
                    elif MESSAGE_TEXT == "⏱ Normal timer" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Enter the time you want in seconds.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | timer check_normal")

                    elif MESSAGE_TEXT == "⏱ Error timer" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Enter the time you want in seconds.</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | timer check_error")
                
                else :

                    if CHECK_STEP.startswith("monitoring | timer") :
                        DB_ROW = STEP_SPLIT[3]
                        if len(MESSAGES_SPLIT) == 1 and MESSAGE_TEXT.isnumeric() :
                            CHANGE = DEF_NODE_STATUS(MESSAGE_CHATID , DB_ROW , MESSAGE_TEXT)
                            await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ Your {DB_ROW} timer is changed.</b>" , reply_markup=KEYBOARD_ON_MONITORING , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"monitoring | wait to select command")
                

            elif CHECK_STEP.startswith("templates") :

                if CHECK_STEP == "templates | wait to select command" :

                    if re.match(r'(\w+) - ([0-9.]+) GB (\d+) days' , MESSAGE_TEXT) :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>حذف شود ؟ {MESSAGES_SPLIT[0]} واقعا میخواهید قالب</b>" , reply_markup=KEYBOARD_YES_OR_NOO , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | delete {MESSAGES_SPLIT[0]}")

                    elif MESSAGE_TEXT == "➕ Add new tempalte" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>نام قالب را وارد کنید.\n(فقط حروف لاتین بدون عدد و ایموجی و غیره ...!)\nمثال :</b> <code>Test</code> ,<code>Ali</code>, <code>Bulk</code>, <code>Free</code>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template")

                else :

                    if CHECK_STEP.startswith("templates | delete") :
                        TEMPLATE_NAME = STEP_SPLIT[3]
                        if MESSAGE_TEXT == "✅ YES , sure!" :
                            CHANGE = DEF_TEMPLATES_DELETE(TEMPLATE_NAME)
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>قالب مد نظر با موفقیت حذف شد. ✅</b>" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

                    else :

                        if CHECK_STEP.startswith("templates | add template") :
                            print(STEP_SPLIT)
                            if len(STEP_SPLIT) == 4 and len(MESSAGES_SPLIT) == 1 and re.match("^[A-Za-z]+$" , MESSAGE_TEXT) :
                                if DEF_CHECK_TEMPLATES_NAME(MESSAGE_TEXT) :
                                    return
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>محدودیت حجم را بصورت گیگابایت وارد نمایید.\n مثال :<code>25.5</code>, <code>15</code>, <code>0.5</code>, <code>100</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {MESSAGE_TEXT}")

                            elif len(STEP_SPLIT) == 5 and len(MESSAGES_SPLIT) == 1 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                TEMPLATE_NAME = STEP_SPLIT[4]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>قیمت را در واحد تومان وارد نمایید .\n مثال : <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {TEMPLATE_NAME} {float(MESSAGE_TEXT)}")

                            elif len(STEP_SPLIT) == 6 and len(MESSAGES_SPLIT) == 1 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                TEMPLATE_NAME, TEMPLATE_PRICE = STEP_SPLIT[4:]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>محدودیت زمانی را وارد نمایید (روز)\nمثال :  <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {TEMPLATE_NAME} {TEMPLATE_PRICE} {float(MESSAGE_TEXT)}")

                            elif len(STEP_SPLIT) == 7 and len(MESSAGES_SPLIT) == 1 and MESSAGE_TEXT.isnumeric() :
                                TEMPLATE_NAME , TEMPLATE_PRICE, TEMPLATE_DATA = STEP_SPLIT[4:]
                                INBOUNDS , INBOUNDS_ALL ,INBOUNDS_SELECT = DEF_GET_INBOUNDS(MESSAGE_CHATID)
                                KEYBOARD_INBOUNDS = KEYBOARD_ALL_INBOUNDS(INBOUNDS_ALL , INBOUNDS_SELECT , None , "templates")
                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>اینباند های مدنظر را انتخاب نمایید:</b>" , reply_markup=KEYBOARD_INBOUNDS , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"templates | add template {TEMPLATE_NAME} {TEMPLATE_PRICE} {TEMPLATE_DATA} {MESSAGE_TEXT}")


            elif CHECK_STEP.startswith("create") :

                if CHECK_STEP == "create | wait to select command" :

                    if MESSAGE_TEXT == "🚀 Manual" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter username :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual")

                    elif re.match(r'(\w+) - ([0-9.]+) GB (\d+) days' , MESSAGE_TEXT) :
                        TEMPLATE_NAME = MESSAGES_SPLIT[0]
                        await client.send_message(chat_id=MESSAGE_CHATID , text="<b>Please enter username :</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | select {TEMPLATE_NAME}")
                    
                else :

                    if CHECK_STEP.startswith("create | select") :
                        TEMPLATE_NAME = STEP_SPLIT[3]
                        
                        if len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 4 :
                            await client.send_message(chat_id=MESSAGE_CHATID , text="<b>تعداد اکانت مدنظر را انتخاب کنید.</b>" , reply_markup=KEYBOARD_CREATE_MUCH , parse_mode=enums.ParseMode.HTML)
                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | select {TEMPLATE_NAME} {MESSAGE_TEXT}")
                        
                        elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 5 and MESSAGE_TEXT.isnumeric() :
                            USERNAME = STEP_SPLIT[4]
                            NAME , DATA , DATE , PROXIES , INBOUNDS, PRICE = DEF_TEMPLATES_DATA_ALL(TEMPLATE_NAME)
                            if int(MESSAGE_TEXT) == 1 :
                                # Construct the SQL command to retrieve the user's credit
                                sql_command_credit = f"SELECT Credit FROM users WHERE chatid = {MESSAGE_CHATID};"
                                # Execute the SQL command to retrieve the user's credit using the subprocess module
                                credit_output = subprocess.check_output(['sqlite3', '/SJbot/SJbot.db', sql_command_credit])
                                user_credit = float(credit_output.decode().strip())
                                # Check if user's credit is sufficient
                                if float(user_credit) >= float(PRICE):
                                    USER_SUB = DEF_CREATE_USER(MESSAGE_CHATID , USERNAME , DATA , DATE , json.loads(PROXIES) , json.loads(INBOUNDS))
                                    if not "❌" in USER_SUB :
                                        QRCODE_IMG = DEF_CREATE_QRCODE(USER_SUB)
                                        await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{USER_SUB}</pre>" , reply_markup=KEYBOARD_HOME_MARKETER)
                                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ <code>{USERNAME}</code> | {DATA} GB | {DATE} Days</b>" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)

                                        # Construct the SQL command
                                        sql_command = f"UPDATE users SET Credit = Credit - {PRICE} WHERE chatid = {MESSAGE_CHATID};"

                                        # Execute the SQL command using the subprocess module
                                        subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], check=True)

                                        sql_command = f"INSERT INTO accounts (chatid, username) VALUES ({MESSAGE_CHATID}, '{USERNAME}');"
                                        subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], check=True)

                                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                                    else :
                                        await client.send_message(chat_id=MESSAGE_CHATID , text=USER_SUB , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                                else:
                                    TEXT = """<b>موجودی شما جهت ساخت اشتراک کافی نمیباشد.</b>
                                    <b>لطفا جهت افزایش موجودی خود با پشتیبانی در ارتباط باشید:</b>
                                    <b>@suppvm</b>"""
                                    await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)

                            else :
                                USERNAMES = DEF_USERNAME_STARTER(USERNAME , int(MESSAGE_TEXT))
                                for USERNAME in USERNAMES :
                                    # Construct the SQL command to retrieve the user's credit
                                    sql_command_credit = f"SELECT Credit FROM users WHERE chatid = {MESSAGE_CHATID};"
                                    # Execute the SQL command to retrieve the user's credit using the subprocess module
                                    credit_output = subprocess.check_output(['sqlite3', '/SJbot/SJbot.db', sql_command_credit])
                                    user_credit = float(credit_output.decode().strip())
                                    # Check if user's credit is sufficient
                                    if float(user_credit) >= float(PRICE):

                                        USER_SUB = DEF_CREATE_USER(MESSAGE_CHATID , USERNAME , DATA , DATE , json.loads(PROXIES) , json.loads(INBOUNDS))
                                        if not "❌" in USER_SUB :
                                            QRCODE_IMG = DEF_CREATE_QRCODE(USER_SUB)
                                            await client.send_photo(chat_id=MESSAGE_CHATID , photo=QRCODE_IMG,caption=f"<pre>{USER_SUB}</pre>" , reply_markup=KEYBOARD_HOME_MARKETER)
                                            await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>✅ <code>{USERNAME}</code> | {DATA} GB | {DATE} Days</b>" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                            # Construct the SQL command
                                            sql_command = f"UPDATE users SET Credit = Credit - {PRICE} WHERE chatid = {MESSAGE_CHATID};"

                                            # Execute the SQL command using the subprocess module
                                            subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], check=True)
                                            sql_command = f"INSERT INTO accounts (chatid, username) VALUES ({MESSAGE_CHATID}, '{USERNAME}');"
                                            subprocess.run(['sqlite3', '/SJbot/SJbot.db', sql_command], check=True)

                                        else :
                                            await client.send_message(chat_id=MESSAGE_CHATID , text=USER_SUB , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                            UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")
                                            break
                                    else:
                                        TEXT = "<b>bia pv @extacy . pool nadari </b>"
                                        await client.send_message(chat_id=MESSAGE_CHATID , text=TEXT , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)
                                        await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                        break
                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"🏛" , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")

                    else :

                        if CHECK_STEP.startswith("create | manual") :

                            if len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 3 and len(MESSAGE_TEXT) > 2 :
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>محدودیت حجم را بصورت گیگابایت وارد نمایید.\n مثال :<code>25.5</code>, <code>15</code>, <code>0.5</code>, <code>100</code></b></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {MESSAGE_TEXT}")

                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 4 and re.match("^\d*\.?\d+$" , MESSAGE_TEXT) :
                                USERNAME = STEP_SPLIT[3]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>محدودیت زمانی را وارد نمایید (روز)\nمثال :  <code>1</code>, <code>15</code>, <code>75</code>, <code>150</code></b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {USERNAME} {MESSAGE_TEXT}")
                            
                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 5 and MESSAGE_TEXT.isnumeric() :
                                USERNAME , DATA_LIMIT = STEP_SPLIT[3:]
                                await client.send_message(chat_id=MESSAGE_CHATID , text="<b>how many do you want?</b>" , reply_markup=KEYBOARD_CANCEL , parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {USERNAME} {DATA_LIMIT} {MESSAGE_TEXT}")

                            elif len(MESSAGES_SPLIT) == 1 and len(STEP_SPLIT) == 6 and MESSAGE_TEXT.isnumeric() :
                                USERNAME , DATA_LIMIT , DATE_LIMIT = STEP_SPLIT[3:]
                                INBOUNDS , INBOUNDS__ALL ,INBOUNDS__SELECT = DEF_GET_INBOUNDS(MESSAGE_CHATID)
                                KEYBOARD_INBOUNDS = KEYBOARD_ALL_INBOUNDS(INBOUNDS__ALL , INBOUNDS__SELECT , None , "create")
                                await client.send_message(chat_id=MESSAGE_CHATID , text=f"<b>اینباند های مدنظر را انتخاب نمایید:</b>" , reply_markup=KEYBOARD_INBOUNDS,  parse_mode=enums.ParseMode.HTML)
                                UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,f"create | manual {USERNAME} {DATA_LIMIT} {DATE_LIMIT} {MESSAGE_TEXT}")
            elif CHECK_STEP.startswith("message") :
                
                if CHECK_STEP == "message | wait to select command" :
                    if MESSAGE_TEXT == "👀 change status" :
                        await client.send_message(chat_id=MESSAGE_CHATID , text=DEF_CHANGE_MESSAGER_STATUS(MESSAGE_CHATID) , reply_markup=KEYBOARD_HOME_MARKETER , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True )
                        UPDATE_STEP = DEF_UPDATE_STEP(MESSAGE_CHATID,"None")