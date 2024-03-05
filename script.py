 #packages
from telegram import *
from telegram.update import Update
from telegram.ext import Updater ,CallbackQueryHandler as cqh
from telegram.ext.commandhandler import CommandHandler as comh
from telegram.ext.messagehandler import MessageHandler as msgh
from telegram.ext.callbackcontext import CallbackContext as cbc
from telegram import KeyboardButton as KB, ReplyKeyboardMarkup as RKM, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM, ReplyKeyboardRemove as RKR
from telegram.ext import Filters
import os
from pandas import DataFrame,read_csv
from psutil import sensors_battery
from getpass import getuser
from pyautogui import screenshot, press 
from subprocess import Popen , call as subcall
from cv2 import VideoCapture , imwrite
import time
from tkinter import *
from webbrowser import open_new_tab


#to run this code you need some more libraries ;)
#written by Hani Torbati
#telegram ID: @finito_cosito or @o21_hani
#instagram ID: hanit.ir


try:
    from TTS import say
except:
    print("TTS.py Not Found!")
    
try:
    from FileHandler import file_handler as cfile
except:
    print("FileHandler.py Not Found!")

#PATHs
main_path = os.getcwd()

#FOLDERs/
BotUsers = f"{main_path}\\BotUsers"
BotInfo = f"{main_path}\\BotInfo"
BotCounters = f"{main_path}\\BotCounters"
ScreenShots = f"{main_path}\\ScreenShots"
CameraShots = f"{main_path}\\CamerShots"
DownLoad = f"{main_path}\\DownLoad"
VoicePlayer = f"{main_path}\\VoicePlayer"


file_paths = [f'{BotCounters}\\screenshot.log',
              f'{BotCounters}\\photo_counter.log',
              f'{BotCounters}\\camera_counter.log',
              f'{BotInfo}\\all.users',
              f'{BotInfo}\\super.users',
              f'{BotInfo}\\info.txt',
              f'{BotInfo}\\mpl_path.log',
              f'{BotInfo}\\sleep.log',
              f'{BotInfo}\\pass.log',
              f'{BotInfo}\\token.txt',
              f'{BotInfo}\\SPT.log']

folder_paths = [BotUsers,BotInfo,BotCounters,ScreenShots,DownLoad,CameraShots,VoicePlayer]

#functions
def csv(path):
    path = str(path)
    if not path.endswith("\\"):
        path += '\\'
    try:
        cfile(f'{path}info.csv','w','user_id,user_name,user_username,login_status,super_user,date,time\n')
        return f'{path}info.csv'
    except FileNotFoundError:
        return 'FNFE'
    

def create_defaults_files():
    for folder_name in folder_paths:
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

    for file_name in file_paths:
        if not os.path.exists(file_name):
            cfile(file_name,"w","0")

    #writing_info
    def set_deafult_info(file,info):
        if cfile(file) == '0':
            cfile(file,'w',info)

    set_deafult_info(f'{BotInfo}\\info.txt','No Info!')
    set_deafult_info(f'{BotInfo}\\mpl_path.log',f'C:\\Users\\{getuser()}\\Music')
    set_deafult_info(f'{BotInfo}\\pass.log','12345')
    set_deafult_info(f'{BotInfo}\\super.users','')
    set_deafult_info(f'{BotInfo}\\all.users','')

create_defaults_files()

def create_files_for_user(path):
    file_paths = ['login_button.log','power.log','power_shutdown.log',
                  'power_signout.log','power_sleep.log','power_lock.log',
                  'upload.log','command.log','download.log',
                  'setting.log','logout.log','stopbot.log','sleepmode.log',
                  'change_password.log','play_voice.log','music_player.log',
                  'shutdown_Timer.log']
    
    for file_name in file_paths:
        cfile(f"{path}\\{file_name}","w","0")

def get_user_status(csv_content,numerical_id,status = 'login'):
    if status == "login":
        return csv_content['login_status'][csv_content['user_id'] == float(numerical_id)].get(0)
    elif status == "super":
        return csv_content['super_user'][csv_content["user_id"]==float(numerical_id)].get(0)
    elif status == "name":
        return csv_content['user_name'][csv_content["user_id"]==float(numerical_id)].get(0)
    elif status == "username":
        return csv_content['user_username'][csv_content["user_id"]==float(numerical_id)].get(0)
    elif status == 'date':
        return csv_content['date'][csv_content["user_id"]==float(numerical_id)].get(0)
    elif status == 'time':
        return csv_content['time'][csv_content["user_id"]==float(numerical_id)].get(0)
    
def get_downloaded_files(status):
    files = os.listdir(DownLoad)
    show = "Your files 👇\n\n"
    uploader_counter = 1

    if status == 'cut':
        for f in files:
            if len(f) > 25:
                f = f[:25]
                f += "..."

            show += f"{uploader_counter} _ {f}\n\n"
            uploader_counter += 1

    elif status == 'full':
        for f in files:
            show += f"{uploader_counter} _ {f}\n\n"
            uploader_counter += 1

    if len(files) == 0:
        show += "No file found!"
    else:
        show += f"\n-choose file number from '1' to '{int(uploader_counter)-1}'..."

    return show


#Buttons

main_button = [[KB("Upload📤"),KB("Download📥")],
               [KB("Command 💬"),KB("Screen 🖥️"),KB("Btr status🔋")],
               [KB("Log out🚶‍♂"),KB("Settings⚙"),KB("Power🔥")],
               [KB("Other options♾️")],
               [KB("Who create me?👻")]]

login_button = [[KB('log in👤')]]

power_button = [[KB("back ⬅️")],
                [KB("shutdown")],
                [KB("lock🔒")],
                [KB("sleep")],
                [KB("sign-out")],
                [KB("shutdown Timer⌛")]]

yn_button = [[KB("no"),KB("yes")]]

cancel_button = [[KB("cancel❌")]]

uploader_button = [[KB("cancel❌"),KB("show files👁️‍🗨️")]]

music_palyer_button = [[KB("show musics👁️‍🗨️")],
              [KB("close❌"),KB("pause⏸️")]]

close_button = [[KB("close❌")]]

setting_button = [[KB('Back ⬅️')],
                  [KB("Stop Bot🚫")],
                  [KB('Sleep Mode😴')],
                  [KB('Avtive Users👤')],
                  [KB("Change Password🔃")],
                  [KB('Super Users🦸')],
                  [KB('Folders📁')],
                  [KB('Counters🔄️')],
                  [KB('Paths🎯')],
                  [KB('Bot Infoℹ️')]]

back_button = [[KB('back ⬅️')]]

wakeup_button = [[KB('WakeUp🙃')]]

options_button = [[IKB('Take shot📸' , callback_data = 'camera_shot')],
                [IKB('Play voice🎵' , callback_data = 'play_voice'),
                IKB('Music player🎵' , callback_data = 'music_player')],
                [IKB('Volume🎚' , callback_data = 'sys_vol')],
                [IKB('Historyℹ️' , callback_data = 'history')]]

uploader_list_button = [[IKB("Show full names👁️‍🗨️" , callback_data = "uploader_list_full_name")],
                        [IKB("hide list" , callback_data = "uploader_list_hide_name")]]

uploader_list_button2 = [[IKB("Show less👁️‍🗨️" , callback_data = "uploader_cutted_name")],
                         [IKB("hide list" , callback_data = "uploader_list_hide_name")]]

uploader_list_button3 = [[IKB("Show list👁️‍🗨️" , callback_data = "uploader_showlist")]]

volume_button = [[IKB('Volume Up➕' , callback_data= 'Volume Up'),
                  IKB('Volume Down➖' , callback_data= 'Volume Down')],
                  [IKB('100%', callback_data= 'Volume 100'),
                   IKB('75%', callback_data= 'Volume 75'),
                   IKB('50%', callback_data= 'Volume 50'),
                   IKB('25%', callback_data= 'Volume 25')],
                  [IKB('Mute🔇', callback_data= 'Volume Mute')],
                  [IKB('Back ⬅️', callback_data= 'Volume Back')]]

history_button = [[IKB('Camera shots', callback_data='camera shots'),
                   IKB('Screen shots', callback_data='screen shots')],
                   [IKB('Back ⬅️', callback_data= 'history Back')]]


#token & updater
if not cfile(f'{BotInfo}\\token.txt') == '0':
    bot_token = cfile(f'{BotInfo}\\token.txt')

try:
    token_read_status = 1
    updater = Updater(token= bot_token, use_context=True)
except:
    token_read_status = 0


def start(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_name = update.message.chat.full_name
    user_username = update.message.chat.username
    user_folder = f"{BotUsers}\\{user_id}"

    if os.path.isdir(user_folder):
        user_info = read_csv(f"{user_folder}\\info.csv",sep=',',header=0)

        if not str(user_id) in cfile(f'{BotInfo}\\all.users','l'):
            if not str(user_id) in cfile(f'{BotInfo}\\super.users','l'):
                cfile(f'{BotInfo}\\all.users','a+',f'{str(user_id)}\n')

        try:
            if not get_user_status(user_info,user_id,'name') == str(user_name):
                user_info['user_name'][user_info['user_id']==int(user_id)] = user_name
                DataFrame.to_csv(user_info,f"{user_folder}\\info.csv",index_label=False, index=False)
        except:
            user_info['user_name'][user_info['user_id']==int(user_id)] = 'err'
            DataFrame.to_csv(user_info,f"{user_folder}\\info.csv",index_label=False, index=False)

        if not get_user_status(user_info,user_id,'username') == str(user_username):
            user_info['user_username'][user_info['user_id']==int(user_id)] = user_username
            DataFrame.to_csv(user_info,f"{user_folder}\\info.csv",index_label=False, index=False)

        if str(user_id) in cfile(f'{BotInfo}\\super.users','l'):
            user_info['login_status'][user_info['user_id']==int(user_id)] = 'yes'
            user_info['super_user'][user_info['user_id']==int(user_id)] = 'yes'
            DataFrame.to_csv(user_info,f'{user_folder}\\info.csv',index_label=False, index=False)

        if get_user_status(user_info,user_id) == 'yes':
            create_files_for_user(user_folder)
            context.bot.send_message(chat_id= user_id,
                                    text= f"Hi {str(user_name)}",
                                    reply_markup= RKM(main_button,resize_keyboard=True, one_time_keyboard=True))
        else:
            create_files_for_user(user_folder)
            context.bot.send_message(chat_id= user_id,
                                    text= f"Hello {str(user_name)}",
                                    reply_markup= RKM(login_button,resize_keyboard=True, one_time_keyboard=True))
    else:
        if not str(user_id) in cfile(f'{BotInfo}\\all.users','l'):
            if not str(user_id) in cfile(f'{BotInfo}\\super.users','l'):
                cfile(f'{BotInfo}\\all.users','a+',f'{str(user_id)}\n')

        os.mkdir(user_folder)
        csv_dir = csv(user_folder)

        now_time = time.localtime()
        t_time = time.strftime("%m/%d/%Y,%H:%M:%S", now_time)

        if not csv_dir == 'FNFE':
            if not str(user_id) in cfile(f'{BotInfo}\\super.users','l'):
                if cfile(csv_dir,"a+",f"{str(user_id)},{str(user_name)},{str(user_username)},no,no,{t_time}") == "ERR => can't write":
                    cfile(csv_dir,"a+",f"{str(user_id)},err,{str(user_username)},no,no,{t_time}")
                context.bot.send_message(chat_id= user_id,
                                 text= f"Hello {str(user_name)}",
                                 reply_markup= RKM(login_button,resize_keyboard=True, one_time_keyboard=True))
            else:
                if cfile(csv_dir,"a+",f"{str(user_id)},{str(user_name)},{str(user_username)},yes,yes,{t_time}") == "ERR => can't write":
                    cfile(csv_dir,"a+",f"{str(user_id)},err,{str(user_username)},yes,yes,{t_time}")
                context.bot.send_message(chat_id = user_id,text=f"Hey {str(user_name)}",
                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

            create_files_for_user(user_folder)
        else:
            print('FNFE')


def info(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_name = update.message.chat.full_name
    user_username = update.message.chat.username
    user_folder = f"{BotUsers}\\{user_id}"

    if os.path.exists(f"{user_folder}\\info.csv"):
        user_info = read_csv(f"{user_folder}\\info.csv",sep=',',header=0)
        DateLogin = get_user_status(user_info,user_id,'date')
        TimeLogin = get_user_status(user_info,user_id,'time')

        if get_user_status(user_info,user_id) == 'yes':
            LoginStatus = '✅'
        else:
            LoginStatus = '❌'

        if get_user_status(user_info,user_id,'super') == 'yes':
                SuperUser = '✅'
                BotPass = cfile(f'{BotInfo}\\pass.log')
        else:
            SuperUser = '❌'
            BotPass = 'Access Denid⛔'
    else:
        DateLogin = ''

    update.message.reply_text(f"""--User Infoℹ️
User: @{get_user_status(user_info,user_id,'username')}
ID: {str(user_id)}
Log in: {LoginStatus}
Super User: {SuperUser}
Fisrt Start Date: {DateLogin}-{TimeLogin}

--Bot Infoℹ️
Path: {main_path}
Bot Pass: {BotPass}
""")
    

def Owner(update: Update, context: cbc):
    update.message.reply_text("<a href='https://t.me/Finito_cosito'>Hani</a>")

def queryHandler(update: Update, context: cbc):
    query = update.callback_query.data
    user_id = update.callback_query.message.chat.id
    user_name = update.callback_query.message.chat.full_name
    user_username = update.callback_query.message.chat.username
    user_folder = f"{BotUsers}\\{user_id}"
    user_info = read_csv(f"{user_folder}\\info.csv",sep=',',header=0)

    if get_user_status(user_info,user_id) == 'yes':
        if query == 'uploader_list_full_name':
            list_content = get_downloaded_files('full')
            update.callback_query.message.edit_text(list_content, reply_markup = IKM(uploader_list_button2))

        elif query == 'uploader_cutted_name' or query == 'uploader_showlist':
            list_content = get_downloaded_files('cut')
            update.callback_query.message.edit_text(list_content, reply_markup = IKM(uploader_list_button))
            
        elif query == 'uploader_list_hide_name':
            update.callback_query.message.edit_text('List is hide!', reply_markup = IKM(uploader_list_button3))

        elif query.startswith('remove_active_user_'):
            query = query[19:]
            try:
                get_user_info = read_csv(f'{BotUsers}\\{query}\\info.csv')
                get_user_info['login_status'][get_user_info["user_id"]==float(query)] = 'no'
                DataFrame.to_csv(get_user_info,f'{BotUsers}\\{query}\\info.csv',index_label=False, index=False)
                update.callback_query.message.reply_text(f'User: {query}\n\nSuccessfuly Removed✅')
            except:
                update.callback_query.message.reply_text(f"User: {query}\n\Can't Remove ❌")

        elif query == 'camera_shot':
            update.callback_query.message.edit_text('Please wait📸...')

            cnt = cfile(f'{BotCounters}\\camera_counter.log')
            path = f'{CameraShots}\\{str(user_id)}_({cnt}).png'

            if os.path.exists(path):
                while True:
                    cnt += 1
                    if not os.path.exists(path):
                        break

            cfile(f'{BotCounters}\\camera_counter.log','w',str(int(cnt) + 1))

            cam_port = 0
            cam = VideoCapture(cam_port)

            result, image = cam.read()

            if result:
                imwrite(f'{CameraShots}\\{str(user_id)}_({cnt}).png', image)
                context.bot.send_photo(chat_id=user_id, photo = open(path,'rb'))
                update.callback_query.message.delete()

            context.bot.send_message(chat_id = user_id,text="---  OTHER OPTIONS 👇  ---",
            reply_markup = IKM(options_button))

        elif query == 'play_voice':
            create_files_for_user(user_folder)
            cfile(f'{user_folder}\\play_voice.log','w','1')
            context.bot.send_message(chat_id = user_id,text="Voice Player Is Running...",
            reply_markup = RKM(close_button,resize_keyboard=True,one_time_keyboard=True))
            
        elif query == 'music_player':
            create_files_for_user(user_folder)
            cfile(f'{user_folder}\\music_player.log','w','1')
            context.bot.send_message(chat_id = user_id,text="Music Player Is Running...",
            reply_markup = RKM(music_palyer_button,resize_keyboard=True,one_time_keyboard=True))
            
        elif query == 'sys_vol':
            update.callback_query.message.edit_text("--- Volume Setting---",reply_markup = IKM(volume_button))

        elif query == 'Volume Up':
            for i in range(3):
                press('volumeup')

        elif query == 'Volume Down':
            for i in range(3):
                press('volumedown')
            
        elif query == 'Volume Back':
            update.callback_query.message.edit_text("---  OTHER OPTIONS 👇  ---",reply_markup = IKM(options_button))

        elif query == 'Volume Mute':
            for i in range(50):
                press('volumedown')

        elif query == 'Volume 100':
            for i in range(50):
                press('volumeup')

        elif query == 'Volume 75':
            for i in range(50):
                press('volumedown')
            for i in range(37):
                press('volumeup')

        elif query == 'Volume 50':
            for i in range(50):
                press('volumedown')
            for i in range(25):
                press('volumeup')
            
        elif query == 'Volume 25':
            for i in range(50):
                press('volumedown')
            for i in range(12):
                press('volumeup')

        elif query == 'AU Back':
            update.callback_query.message.delete()
            create_files_for_user(user_folder)
            cfile(f"{user_folder}\\setting.log","w",'1')
            context.bot.send_message(chat_id = user_id,text='Setting⚙',
            reply_markup = RKM(setting_button, resize_keyboard=True,one_time_keyboard=True))
    
        elif query.lower() == 'history':
            update.callback_query.message.edit_text("--- History---",reply_markup = IKM(history_button))

        elif query.lower() == 'screen shots':
            screenshots_path = f'{main_path}\\ScreenShots'
            
            user_screenshots = []
            for filename in os.listdir(screenshots_path):
                if f'{user_id}_' in filename:
                    user_screenshots.append(f'{screenshots_path}\\{filename}')
                    
            if not user_screenshots:
                update.callback_query.message.reply_text('You have no screenshots')
                return
            
            for screenshot in user_screenshots:
                try:
                    context.bot.send_photo(chat_id=user_id, photo=open(screenshot, 'rb'))
                except Exception as e:
                    print(f'Error sending {screenshot}: {e}')
                    
            update.callback_query.message.reply_text('Screenshots sent')

        elif query.lower() == 'camera shots':
            screenshots_path = f'{main_path}\\CamerShots'
            
            user_screenshots = []
            for filename in os.listdir(screenshots_path):
                if f'{user_id}_' in filename:
                    user_screenshots.append(f'{screenshots_path}\\{filename}')
                    
            if not user_screenshots:
                update.callback_query.message.reply_text('You have no CamerShots')
                return
            
            for screenshot in user_screenshots:
                try:
                    context.bot.send_photo(chat_id=user_id, photo=open(screenshot, 'rb'))
                except Exception as e:
                    print(f'Error sending {screenshot}: {e}')
                    
            update.callback_query.message.reply_text('CamerShots sent')

        elif query.lower() == 'history back':
            update.callback_query.message.edit_text("---  OTHER OPTIONS 👇  ---",reply_markup = IKM(options_button))
    else:
        update.callback_query.message.delete()
        context.bot.send_message(chat_id= user_id, text='Login First⛔',
                                 reply_markup = RKM(login_button,resize_keyboard=True, one_time_keyboard=True))


def user_message(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_name = update.message.chat.full_name
    user_username = update.message.chat.username
    user_folder = f"{BotUsers}\\{user_id}"
    user_msg = update.message.text
    if not os.path.exists(f"{user_folder}\\info.csv"):
        update.message.reply_text('⭕Error: User Info Not Found\nTo Fix It /start Bot Again.')
    else:
        user_info = read_csv(f"{user_folder}\\info.csv",sep=',',header=0)
    
    
    sleep_mode_status = cfile(f'{BotInfo}\\sleep.log')

    if not sleep_mode_status == '1':
        if get_user_status(user_info,user_id) == 'yes':
            power_selected = cfile(f'{user_folder}\\power.log')
            upload_selected = cfile(f'{user_folder}\\upload.log')
            download_selected = cfile(f'{user_folder}\\download.log')
            setting_selected = cfile(f"{user_folder}\\setting.log")
            logout_selected = cfile(f"{user_folder}\\logout.log")
            cmd_selected = cfile(f"{user_folder}\\command.log")
            voiceplayer_selected = cfile(f'{user_folder}\\play_voice.log')
            music_palyer_selected = cfile(f'{user_folder}\\music_player.log')
            
            if power_selected == '1':
                power_shutdown_selected = cfile(f'{user_folder}\\power_shutdown.log')
                power_sleep_selected = cfile(f'{user_folder}\\power_sleep.log')
                power_signout_selected = cfile(f'{user_folder}\\power_signout.log')
                power_lock_selected = cfile(f'{user_folder}\\power_lock.log')
                power_shutdowntimer_selected = cfile(f'{user_folder}\\shutdown_Timer.log')

                if power_shutdown_selected == '1':
                    if user_msg == 'no':
                        cfile(f'{user_folder}\\power_shutdown.log','w','0')
                        context.bot.send_message(chat_id=user_id , text="ok" ,
                                                 reply_markup = RKM(power_button,resize_keyboard=True,one_time_keyboard=True))
                    elif user_msg == 'yes':
                        cfile(f'{user_folder}\\power_shutdown.log','w','0')
                        cfile(f'{user_folder}\\power.log','w','0')
                        context.bot.send_message(chat_id = user_id,text="shuting down...",
                        reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True)) 
                        os.system("shutdown -s")
                    else:
                        update.message.reply_text('Invalid!')

                elif power_lock_selected == '1':
                    if user_msg == 'no':
                        cfile(f'{user_folder}\\power_lock.log','w','0')
                        context.bot.send_message(chat_id=user_id , text="ok" ,
                                                 reply_markup = RKM(power_button,resize_keyboard=True,one_time_keyboard=True))
                    elif user_msg == 'yes':
                        cfile(f'{user_folder}\\power_lock.log','w','0')
                        cfile(f'{user_folder}\\power.log','w','0')
                        try:
                            os.system("Rundll32.exe user32.dll,LockWorkStation")
                            context.bot.send_message(chat_id = user_id,text="PC LOCKED🔒",
                            reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                        except:
                            context.bot.send_message(chat_id = user_id,text="ERROR HAPPEND❌",
                            reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                    else:
                        update.message.reply_text('Invalid!')
                
                elif power_sleep_selected == '1':
                    if user_msg == 'no':
                        cfile(f'{user_folder}\\power_sleep.log','w','0')
                        context.bot.send_message(chat_id=user_id , text="ok" ,
                                                 reply_markup = RKM(power_button,resize_keyboard=True,one_time_keyboard=True))
                    elif user_msg == 'yes':
                        cfile(f'{user_folder}\\power_sleep.log','w','0')
                        cfile(f'{user_folder}\\power.log','w','0')
                        context.bot.send_message(chat_id = user_id,text="sleeping...",
                        reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True)) 
                        os.system("shutdown.exe /h")
                    else:
                        update.message.reply_text('Invalid!')

                elif power_signout_selected == '1':
                    if user_msg == 'no':
                        cfile(f'{user_folder}\\power_signout.log','w','0')
                        context.bot.send_message(chat_id=user_id , text="ok" ,
                                                reply_markup = RKM(power_button,resize_keyboard=True,one_time_keyboard=True))
                    elif user_msg == 'yes':
                        cfile(f'{user_folder}\\power_signout.log','w','0')
                        cfile(f'{user_folder}\\power.log','w','0')
                        context.bot.send_message(chat_id = user_id,text="signing out...",
                        reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True)) 
                        os.system("shutdown -l")
                    else:
                        update.message.reply_text('Invalid!')

                elif power_shutdowntimer_selected == '1':
                    if user_msg == "cancel❌":
                        cfile(f'{user_folder}\\shutdown_Timer.log','w','0')
                        context.bot.send_message(chat_id=user_id , text="ok" ,
                                                reply_markup = RKM(power_button,resize_keyboard=True,one_time_keyboard=True))
                        
                    elif user_msg.isnumeric():
                        #cfile(f'{BotInfo}\\SPT.log','w',user_msg)
                        cfile(f'{user_folder}\\shutdown_Timer.log','w','0')
                        cfile(f'{user_folder}\\power.log','w','0')
                        #subcall(f'{main_path}\\SPT.pyw',shell=True)
                        context.bot.send_message(chat_id=user_id , text="⭕This part is not availble" ,
                                                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                    else:
                        update.message.reply_text('Unknown!')
                
                else:
                    if user_msg == 'sign-out':
                        cfile(f'{user_folder}\\power_signout.log','w','1')
                        context.bot.send_message(chat_id = user_id ,
                                                text="Are you sure?",
                                                reply_markup = RKM(yn_button,resize_keyboard=True,one_time_keyboard=True))

                    elif user_msg == 'shutdown':
                        cfile(f'{user_folder}\\power_shutdown.log','w','1')
                        context.bot.send_message(chat_id = user_id ,
                                                text="Are you sure?",
                                                reply_markup = RKM(yn_button,resize_keyboard=True,one_time_keyboard=True))

                    elif user_msg == 'sleep':
                        cfile(f'{user_folder}\\power_sleep.log','w','1')
                        context.bot.send_message(chat_id = user_id ,
                                                text="Are you sure?",
                                                reply_markup = RKM(yn_button,resize_keyboard=True,one_time_keyboard=True))
                        
                    elif user_msg == 'lock🔒':
                        cfile(f'{user_folder}\\power_lock.log','w','1')
                        context.bot.send_message(chat_id = user_id ,
                                                text="Are you sure?",
                                                reply_markup = RKM(yn_button,resize_keyboard=True,one_time_keyboard=True))
                        
                    elif user_msg == "shutdown Timer⌛":
                        cfile(f'{user_folder}\\shutdown_Timer.log','w','1')
                        context.bot.send_message(chat_id = user_id ,
                                                text="How many minutes?",
                                                reply_markup = RKM(cancel_button,resize_keyboard=True,one_time_keyboard=True))

                    elif user_msg == "back ⬅️":
                        cfile(f"{user_folder}\\power.log","w",'0')
                        context.bot.send_message(chat_id = user_id,text="chose options👇",
                        reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

            elif upload_selected == '1':
                if user_msg == "cancel❌":
                    cfile(f"{user_folder}\\upload.log","w",'0')

                    context.bot.send_message(chat_id = user_id,text="chose options👇",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
            
            elif download_selected == '1':
                if user_msg == "cancel❌":
                    cfile(f'{user_folder}\\download.log','w','0')
                    context.bot.send_message(chat_id = user_id,text="chose options👇",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "show files👁️‍🗨️":
                    msg = update.message.reply_text("please wait ...")

                    list_content = get_downloaded_files('cut')

                    context.bot.edit_message_text(chat_id=user_id, 
                            message_id=msg.message_id,
                            text=list_content , reply_markup = IKM(uploader_list_button))

                else:
                    files = os.listdir(DownLoad)
                    if user_msg.isnumeric() and int(user_msg) <= len(files) and int(user_msg) > 0:
                        pr_msg = update.message.reply_text("Preparation...",reply_markup=RKR())
                        context.bot.deleteMessage(chat_id=user_id, 
                                message_id=pr_msg.message_id)

                        ld_msg = update.message.reply_text("Loading file...")
                        user_file_selection = files[int(user_msg)-1]
                        selected_file_dir = f'{DownLoad}\\' + user_file_selection 

                        cfile(f'{user_folder}\\download.log','w','0')

                        if user_file_selection.endswith('.jpg') or user_file_selection.endswith('.png'):
                            try:
                                context.bot.edit_message_text(chat_id=user_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploading photo📷...")


                                context.bot.send_photo(chat_id = user_id, photo = open(selected_file_dir,'rb'), caption = user_file_selection)

                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploaded successfuly ✅")

                                context.bot.send_message(chat_id = user_id,text="chose options👇",
                                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                            except:
                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text = "Can't upload photo📷! ❌")
                                
                        elif user_file_selection.endswith('.mp4'):
                            try:
                                context.bot.edit_message_text(chat_id=user_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploading video🎬...")


                                context.bot.send_video(chat_id=user_id, video=open(selected_file_dir, 'rb'), supports_streaming=True, timeout=360)

                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploaded successfuly ✅")
                                
                                context.bot.send_message(chat_id = user_id,text="chose options👇",
                                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                            except:
                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text = "Can't upload video🎬! ❌")
                                
                        elif user_file_selection.endswith('.mp3'):
                            try:
                                context.bot.edit_message_text(chat_id=user_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploading audio🎵...")


                                context.bot.send_audio(chat_id = user_id,
                                                    audio=open(selected_file_dir, 'rb'),
                                                    timeout=360, caption = user_file_selection)

                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploaded successfuly ✅")

                                context.bot.send_message(chat_id = user_id,text="chose options👇",
                                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                            except:
                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text = "Can't upload audio🎵! ❌")
                        
                        else:
                            try:
                                context.bot.edit_message_text(chat_id=user_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploading file...")


                                context.bot.send_document( chat_id = update.message.chat.id,
                                                        document = open(selected_file_dir,'rb'),
                                                        timeout=360, filename=user_file_selection,
                                                        caption = files[int(user_msg)-1])

                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text="Uploaded successfuly ✅")
                                
                                context.bot.send_message(chat_id = user_id,text="chose options👇",
                                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                            except:
                                context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                        message_id=ld_msg.message_id,
                                        text = "Can't upload file! ❌")
                    
                    else: 
                        update.message.reply_text('You Can Not Do This❌')
                        
            elif setting_selected == '1':
                setting_stopbot_selected = cfile(f"{user_folder}\\stopbot.log")
                setting_sleepmode_selected = cfile(f"{user_folder}\\sleepmode.log")
                setting_change_password_selected = cfile(f'{user_folder}\\change_password.log')

                if setting_stopbot_selected == '1':
                    if user_msg == 'no':
                        cfile(f"{user_folder}\\stopbot.log",'w','0')
                        context.bot.send_message(chat_id = user_id,text="OK",
                        reply_markup = RKM(setting_button,resize_keyboard=True,one_time_keyboard=True))
                    elif user_msg == 'yes':
                        cfile(f"{user_folder}\\stopbot.log",'w','0')
                        cfile(f"{user_folder}\\setting.log",'w','0')
                        context.bot.send_message(chat_id = user_id,text="Bot Stoped By Super User⛔",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                        updater.stop()
                    else:
                        update.message.reply_text('Unknown!')

                elif setting_sleepmode_selected == '1':
                    if user_msg == 'no':
                        cfile(f"{user_folder}\\sleepmode.log",'w','0')
                        context.bot.send_message(chat_id = user_id,text="OK",
                        reply_markup = RKM(setting_button,resize_keyboard=True,one_time_keyboard=True))
                    elif user_msg == 'yes':
                        cfile(f"{user_folder}\\sleepmode.log",'w','0')
                        cfile(f"{user_folder}\\sleepmode.log",'w','0')
                        cfile(f'{BotInfo}\\sleep.log','w','1')
                        context.bot.send_message(chat_id = user_id,text="Sleep Mode Turned On By Super User😴",
                                    reply_markup = RKM(wakeup_button,resize_keyboard=True,one_time_keyboard=True))
                    else:
                        update.message.reply_text('Unknown!')
                
                elif setting_change_password_selected == '1':
                    if user_msg == 'cancel❌':
                        cfile(f'{user_folder}\\change_password.log','w','0')
                        context.bot.send_message(chat_id = user_id,text="OK",
                        reply_markup = RKM(setting_button,resize_keyboard=True,one_time_keyboard=True))
                    else:
                        try:
                            cfile(f'{BotInfo}\\pass.log','w',user_msg)
                            cfile(f'{user_folder}\\change_password.log','w','0')
                            context.bot.send_message(chat_id = user_id,text="Passwoed Changed Successfuly✅",
                            reply_markup = RKM(setting_button,resize_keyboard=True,one_time_keyboard=True))
                        except:
                            update.message.reply_text('Error: Bad Pass❌')                        

                elif user_msg == 'Back ⬅️':
                    cfile(f"{user_folder}\\setting.log","w",'0')
                    context.bot.send_message(chat_id = user_id,text="chose options👇",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == 'Stop Bot🚫':
                    cfile(f'{user_folder}\\stopbot.log','w','1')
                    context.bot.send_message(chat_id = user_id,text="Are you sure?",
                    reply_markup = RKM(yn_button,resize_keyboard=True,one_time_keyboard=True))
                    
                elif user_msg == 'Sleep Mode😴':
                    cfile(f'{user_folder}\\sleepmode.log','w','1')
                    context.bot.send_message(chat_id = user_id,text="Are you sure?",
                    reply_markup = RKM(yn_button,resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == 'Avtive Users👤':
                    active_users_id = []
                    for user in cfile(f'{BotInfo}\\all.users','l'):
                        try:
                            user_csv = read_csv(f'{BotUsers}\\{user}\\info.csv',sep=',',header=0)
                            if get_user_status(user_csv,user) == 'yes':
                                active_users_id.append(user)
                        except:
                            active_users_id.append('Unknown!')

                    if len(active_users_id) == 0:
                        msg_content = 'No Normal User Is Avtive !'
                        context.bot.send_message(chat_id = update.message.chat.id,text=msg_content,
                        reply_markup = RKM(setting_button, resize_keyboard=True,one_time_keyboard=True))
                    else:
                        msg_content = 'Active Users:\n\n'
                        active_users_remove_button = []
                        for ev in active_users_id:
                            try:
                                get_usn = read_csv(f'{BotUsers}\\{ev}\\info.csv',sep=',',header=0)
                                get_name = get_user_status(get_usn,ev,'username')
                            except:
                                get_usn = 'Unknown!'
                            msg_content += f'id: {ev}\nusername: @{get_name}\n\n'
                            active_users_remove_button.append([IKB(ev, callback_data=f'remove_active_user_{ev}')])

                        msg_content+= 'Top to remove👇'
                        active_users_remove_button.append([IKB('Back ⬅️', callback_data='AU Back')])

                        context.bot.send_message(chat_id = update.message.chat.id,text=msg_content,
                        reply_markup = IKM(active_users_remove_button))

                elif user_msg == 'Change Password🔃':
                    cfile(f'{user_folder}\\change_password.log','w','1')
                    context.bot.send_message(chat_id = user_id,text="Send New Password🔑",
                    reply_markup = RKM(cancel_button,resize_keyboard=True,one_time_keyboard=True))
                    
                elif user_msg == 'Super Users🦸':
                    super_users = cfile(f'{BotInfo}\\super.users','l')
                    msg_content = 'All Super Users:\n\n'
                    for ev in super_users:
                        get_user_info = read_csv(f'{BotUsers}\\{ev}\\info.csv',sep=',',header=0)
                        get_user_info = get_user_info['user_username'][get_user_info['user_id']==float(ev)].get(0)
                        msg_content += f'{ev} - @{get_user_info}\n'
                    update.message.reply_text(msg_content)

                elif user_msg == 'Bot Infoℹ️':
                    update.message.reply_text(cfile(f'{BotInfo}\\info.txt'))

                elif user_msg == 'Folders📁':
                    folders_msg = f"""
Main Folder: {main_path}

Users Folder: {BotUsers}
Info Folder: {BotInfo} 
Counters Folder: {BotCounters}
ScreenShots Folder: {ScreenShots}
CameraShots Folder: {CameraShots}
Downloads Folder: {DownLoad}
VoicePlayer Folder: {VoicePlayer}
"""
    
                    update.message.reply_text(folders_msg)

                elif user_msg == 'Counters🔄️':
                    counters_path = BotCounters
                    
                    counter_files = os.listdir(counters_path)
                    
                    counters_msg = 'Bot Counters:\n'
                    
                    for file_name in counter_files:
                        if file_name.endswith('.log'):
                            counter_name = file_name[:-4].replace('_',' ').title()
                            counter_value = cfile(f'{counters_path}\\{file_name}')
                            
                            counters_msg += f'\n{counter_name}:\n{counter_value}\n'

                    update.message.reply_text(counters_msg)

                elif user_msg == 'Paths🎯':
                    Music_Player_Path = cfile(f'{BotInfo}\\mpl_path.log')
                    paths_msg = f"""
Main Path: {main_path}

Folders Paths:
---Users Path: {BotUsers}  

---Info Path: {BotInfo}

---Counters Path: {BotCounters}

---ScreenShots Path: {ScreenShots}

---CameraShots Path: {CameraShots} 

---Downloads Path: {DownLoad}

---VoicePlayer Path: {VoicePlayer}

---User Music Folder: {Music_Player_Path}

File paths:
"""

                    for i in file_paths:
                        paths_msg += f'\n---{i}\n'
                    update.message.reply_text(paths_msg)

            elif logout_selected == '1':
                if user_msg == 'no':
                    cfile(f"{user_folder}\\logout.log",'w','0')
                    context.bot.send_message(chat_id = user_id,text="OK",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                elif user_msg == 'yes':
                    cfile(f"{user_folder}\\logout.log",'w','0')
 
                    user_info['login_status'][user_info["user_id"]==float(user_id)] = 'no'
                    DataFrame.to_csv(user_info, f"{user_folder}\\info.csv", index_label=False, index=False)

                    context.bot.send_message(chat_id = user_id,text="You loged out❕",
                                reply_markup = RKM(login_button,resize_keyboard=True,one_time_keyboard=True))
                else:
                    update.message.reply_text('Unknown!')

            elif cmd_selected == '1':
                if user_msg == 'close❌':
                    cfile(f"{user_folder}\\command.log",'w','0')
                    context.bot.send_message(chat_id = user_id,text="cmd Closed🆑",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                else:
                    low = user_msg.lower()

                    if user_msg.endswith(".exe"):
                        try:
                            Popen([user_msg])
                            update.message.reply_text("program opend successfuly ✅")
                        except:
                            update.message.reply_text("Error happend! ❌")

                    elif user_msg.lower() == "taskmgr":
                        update.message.reply_text("you can't do this! ❌\nbecuase if you run task manager, telegram bot will stop! ")
                    
                    elif low.endswith('taskmgr.exe"'):
                        update.message.reply_text("you can't do this! ❌\nbecuase if you run task manager, telegram bot will stop! ")

                    elif low.endswith('task manager.lnk"') or user_msg.endswith('task manager.ink"'):
                        update.message.reply_text("you can't do this! ❌\nbecuase if you run task manager, telegram bot will stop! ")


                    else:
                        try:
                            os.system(user_msg)
                            update.message.reply_text("✅‌")
                        except:
                            update.message.reply_text("❌‌")

            elif voiceplayer_selected == '1':
                if user_msg == 'close❌':
                    cfile(f'{user_folder}\\play_voice.log','w','0')
                    context.bot.send_message(chat_id = user_id,text="Voice Player Closed🆑",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                else:
                    try:
                        say(user_msg)
                        update.message.reply_text('🔉‌')
                    except:
                        update.message.reply_text('⭕ERR: TTS')
            
            elif music_palyer_selected == '1':
                if user_msg == 'close❌':
                    cfile(f'{user_folder}\\music_player.log','w','0')
                    context.bot.send_message(chat_id = user_id,text="Music Player Closed Successfuly🆑",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == 'pause⏸️':
                    try:
                        os.system("taskkill /f /im Microsoft.Media.Player.exe")
                    except:
                        pass
                    update.message.reply_text("paused.")

                elif user_msg == 'show musics👁️‍🗨️':
                    msg = update.message.reply_text("Loading Files...")
                    path = cfile(f'{BotInfo}\\mpl_path.log')
                    if not str(path).endswith('\\'):
                        path += '\\'
                    files = os.listdir(path)

                    musics = []
                    play_counter = 1
                    show = "Musics List 👇\n\n"

                    for music in files:
                        if music.endswith(".mp3"):
                            musics.append(path + music)
                            if len(music) > 23:
                                music = music[:23]
                                music += "..."

                            show += f"{play_counter} _ {music}\n\n"
                            play_counter += 1

                    if len(musics) == 0:
                        show += 'No Music Found!'
                    else:
                        show += f"\n-Choose Music Number From '1' To '{int(play_counter)-1}'..."

                    context.bot.edit_message_text(chat_id=user_id, 
                                                  message_id=msg.message_id, text=show)
                    
                else:
                    path = cfile(f'{BotInfo}\\mpl_path.log')
                    files = os.listdir(path)
                    musics = []
                    for music in files:
                        if str(music).endswith(".mp3"):
                            musics.append(music)

                    if user_msg.isnumeric() and int(user_msg) <= len(musics) and int(user_msg) > 0:
                        selected_music = musics[int(user_msg)-1]
                        music_dir = path + '\\' +selected_music 
                    
                        subcall(f"{music_dir}",shell=True)
                        update.message.reply_text(f"Playing {selected_music}🎵 ...")
                    else:
                        update.message.reply_text("Invalid ❌")

            else:
                if user_msg == "Power🔥":
                    cfile(f"{user_folder}\\power.log","w",'1')
                    context.bot.send_message(chat_id = user_id,text="power options👇",
                    reply_markup = RKM(power_button,resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "Upload📤":
                    cfile(f"{user_folder}\\upload.log","w",'1')
                    context.bot.send_message(chat_id = user_id,text="Ok. Now send your data...",
                    reply_markup = RKM(cancel_button,resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "Download📥":
                    cfile(f"{user_folder}\\download.log","w",'1')
                    context.bot.send_message(chat_id = user_id,text="Ok. send file num...",
                    reply_markup = RKM(uploader_button, resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "Btr status🔋":
                    try:
                        def convertTime(seconds):
                            minutes, seconds = divmod(seconds, 60)
                            hours, minutes = divmod(minutes, 60)
                            return "%d:%02d:%02d" % (hours, minutes, seconds)

                        battery = sensors_battery()
                        plg_h = battery.power_plugged

                        if plg_h == "False" or plg_h == False:
                            plg = "No Charging ❌"
                        else:
                            plg = "Charging ✅"

                        if plg == "Charging ✅":
                            tleft = "-plugged in 🔌"
                        else:
                            if battery.percent == "100" or battery.percent == 100:
                                tleft = "-Fully charge "
                            else:
                                tleft = convertTime(battery.secsleft)

                        if battery.percent > 30:
                            imo = "🔋"
                        else:
                            imo = "🪫"


                        update.message.reply_text(f"""'{getuser()}' Battery🔋

Battery level : {battery.percent}% {imo}
Power plugged in : {plg}
Battery left : {tleft}""")

                        context.bot.send_message(chat_id = user_id,text="chose options👇",
                        reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))

                    except:
                        update.message.reply_text("Can't chek battery startus 🚫")

                elif user_msg == "Screen 🖥️":
                    screen_pleasewait = update.message.reply_text("please wait...")

                    try:
                        screenshot_counter = int(cfile(f'{BotCounters}\\screenshot.log'))
                        cfile(f'{BotCounters}\\screenshot.log','w', str(screenshot_counter+1))

                        myScreenshot = screenshot()
                        myScreenshot.save(f"{ScreenShots}\\{str(user_id)}_({screenshot_counter}).png")

                        context.bot.send_photo(chat_id= user_id, photo= open(f"{ScreenShots}\\{str(user_id)}_({screenshot_counter}).png",'rb'))

                        context.bot.deleteMessage(chat_id= user_id, 
                                message_id= screen_pleasewait.message_id)
                    except:
                        context.bot.edit_message_text(chat_id=user_id, 
                                        message_id= screen_pleasewait.message_id,
                                        text="⭕Can't take picture!")

                elif user_msg == "Command 💬":
                    cfile(f"{user_folder}\\command.log","w",'1')
                    context.bot.send_message(chat_id = user_id,text="Ok. 'CMD' is running...",
                    reply_markup = RKM(close_button, resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "Settings⚙":
                    if get_user_status(user_info,user_id,'super') == 'yes':
                        cfile(f"{user_folder}\\setting.log","w",'1')
                        context.bot.send_message(chat_id = user_id,text='Identity Confirmed✅',
                        reply_markup = RKM(setting_button, resize_keyboard=True,one_time_keyboard=True))
                    else:
                        context.bot.send_message(chat_id = user_id,text='Only Super Users Can Change setting🚫',
                        reply_markup = RKM(main_button, resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "Log out🚶‍♂": 
                    cfile(f"{user_folder}\\logout.log","w",'1')
                    context.bot.send_message(chat_id = user_id,text="Are you sure?",
                    reply_markup = RKM(yn_button, resize_keyboard=True,one_time_keyboard=True))

                elif user_msg == "Who create you?":
                    context.bot.send_message(chat_id = user_id, text = "Publisher: <a href='https://t.me/finito_cosito'>Hani Torbati</a>", parse_mode = ParseMode.HTML)

                elif user_msg == "Other options♾️":
                    context.bot.send_message(chat_id = user_id,text="---  OTHER OPTIONS 👇  ---",
                    reply_markup = IKM(options_button))

                elif user_msg.lower() == 'my id':
                    update.message.reply_text(str(user_id))

                elif user_msg.lower() == 'user report txt':
                    if get_user_status(user_info,user_id,'super') == 'yes':
                        msg = update.message.reply_text("Creating file...")
                        cfile(f'{BotInfo}\\user report.txt','w','')
                        users = os.listdir(BotUsers)
                        umsg = f'{str(len(users))} User Founded!'

                        for ev in users:
                            user_csv = read_csv(f"{BotUsers}\\{ev}\\info.csv",sep=',',header=0)

                            User_Name = get_user_status(user_csv,ev,'name')
                            try:
                                with open(f'{BotInfo}\\temp','w') as f:
                                    f.write(User_Name)
                            except:
                                User_Name = 'Error'

                            User_UserName = get_user_status(user_csv,ev,'username')
                            if get_user_status(user_csv,ev,'login') == 'yes':
                                User_Login = 'yes'
                            else:
                                User_Login = 'no'

                            if get_user_status(user_csv,ev,'super') == 'yes':
                                User_Super = 'yes'
                            else:
                                User_Super = 'no'

                            User_Date = get_user_status(user_csv,ev,'date')
                            User_Time = get_user_status(user_csv,ev,'time')

                            User_Info_Handler = f"""ID: {ev}
Name: {User_Name}
Username: @{User_UserName}
Login: {User_Login}
Super: {User_Super}
Date: {User_Date}
Time: {User_Time}


"""
                            file = cfile(f'{BotInfo}\\user report.txt','a+',User_Info_Handler)
                        try:
                            context.bot.send_document(chat_id = user_id,
                                                      document = open(file ,'rb'),
                                                      timeout=360, filename='user report.txt')
                            
                            context.bot.delete_message(chat_id=user_id, message_id=msg.message_id)
                        except:
                            context.bot.edit_message_text(chat_id=user_id, 
                                                          message_id=msg.message_id,
                                                          text="⭕Something happend!",
                                                          caption=umsg)

                elif user_msg.lower() == 'user report':
                    if get_user_status(user_info,user_id,'super') == 'yes':

                        users = os.listdir(BotUsers)
                        umsg = f'{str(len(users))} User Founded!\n\n\n'

                        for ev in users:
                            user_csv = read_csv(f"{BotUsers}\\{ev}\\info.csv",sep=',',header=0)

                            User_Name = get_user_status(user_csv,ev,'name')

                            User_UserName = get_user_status(user_csv,ev,'username')

                            if get_user_status(user_csv,ev,'login') == 'yes':
                                User_Login = '✅'
                            else:
                                User_Login = '❌'

                            if get_user_status(user_csv,ev,'super') == 'yes':
                                User_Super = '✅'
                            else:
                                User_Super = '❌'

                            User_Date = get_user_status(user_csv,ev,'date')
                            User_Time = get_user_status(user_csv,ev,'time')

                            User_Info_Handler = f"""ID: {ev}
Name: {User_Name}
Username: @{User_UserName}
Login: {User_Login}
Super: {User_Super}
Date: {User_Date}
Time: {User_Time}


"""
                            umsg += User_Info_Handler
                        update.message.reply_text(umsg)

                elif user_msg == "Who create me?👻":
                    context.bot.send_message(chat_id = user_id, text = "Publisher: <a href='https://t.me/finito_cosito'>Hani Torbati</a>", parse_mode = ParseMode.HTML)

                else:
                    pass
        
        else:
            login_button_status = cfile(f"{user_folder}\\login_button.log")

            if user_msg == "log in👤":
                cfile(f"{user_folder}\\login_button.log",'w','1')
                update.message.reply_text("OK. Now send your ENTRY ID...",
                                        reply_markup=RKM(cancel_button,resize_keyboard=True,one_time_keyboard=True))

            elif user_msg == "cancel❌":
                cfile(f"{user_folder}\\login_button.log",'w','0')
                update.message.reply_text("OK.",
                                        reply_markup=RKM(login_button,resize_keyboard=True,one_time_keyboard=True))

            elif login_button_status == '1':
                bot_password = cfile(f"{BotInfo}\\pass.log")

                if user_msg == bot_password:
                    user_info['login_status'][user_info['user_id'] == int(user_id)] = 'yes'
                    DataFrame.to_csv(user_info,f"{user_folder}\\info.csv",index_label=False, index=False)
                    
                    create_files_for_user(user_folder)

                    context.bot.send_message(chat_id= user_id,text="you are loged in now ✅",
                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                else:
                    update.message.reply_text("Invalid ENTRY ID ❌")

            elif user_msg.lower() == 'my id':
                update.message.reply_text(str(user_id))

            else:
                context.bot.send_message(chat_id= user_id,
                                        text="⚠️First you must log in to use bot!",
                                        reply_markup = RKM(login_button,resize_keyboard=True,one_time_keyboard=True))
    
    else:
        if get_user_status(user_info,user_id,'super') == 'yes':
            if user_msg == 'WakeUp🙃':
                cfile(f'{BotInfo}\\sleep.log','w','0')
                create_files_for_user(user_folder)
                context.bot.send_message(chat_id = user_id,text="I'm Awake😀",
                reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
            else:
                update.message.reply_text('🤔')
        
        else:
            update.message.reply_text('😴')


def photo_handler(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_folder = f"{BotUsers}\\{user_id}"
    print(update)

    upload_selected = cfile(f'{user_folder}\\upload.log')

    if upload_selected == '1':
        pr_msg = update.message.reply_text("Preparation...",reply_markup=RKR())
        context.bot.deleteMessage(chat_id=user_id, 
                message_id=pr_msg.message_id)
        
        dn_msg = update.message.reply_text("Downloading photo📷...")

        cnt = int(cfile(f'{BotCounters}\\photo_counter.log'))

        if os.path.exists(f'{DownLoad}\\pic{str(cnt)}.jpg'):
            while True:
                cnt += 1
                if not os.path.exists(f'{DownLoad}\\pic{str(cnt)}.jpg'):
                    break
        
        try:
            userpic = update.message.photo[3].file_id
            objpic = context.bot.get_file(userpic)
            objpic.download(f'{DownLoad}\\pic{str(cnt)}.jpg')
            cfile(f'{BotCounters}\\photo_counter.log','w',str(cnt+1))
            cfile(f'{user_folder}\\upload.log','w','0')
            context.bot.edit_message_text(chat_id=user_id,
                                                  message_id=dn_msg.message_id,
                                                  text="Photo Saved ✅")
            
            context.bot.send_message(chat_id = user_id,text="chose options👇",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
        except:
            try:
                userpic = update.message.photo[2].file_id
                objpic = context.bot.get_file(userpic)
                objpic.download(f'{DownLoad}\\pic{str(cnt)}.jpg')
                cfile(f'{BotCounters}\\photo_counter.log','w',str(cnt+1))
                cfile(f'{user_folder}\\upload.log','w','0')
                context.bot.edit_message_text(chat_id=user_id,
                                                  message_id=dn_msg.message_id,
                                                  text="Photo Saved ✅")
                
                context.bot.send_message(chat_id = user_id,text="chose options👇",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
            except:
                try:
                    userpic = update.message.photo[1].file_id
                    objpic = context.bot.get_file(userpic)
                    objpic.download(f'{DownLoad}\\pic{str(cnt)}.jpg')
                    cfile(f'{BotCounters}\\photo_counter.log','w',str(cnt+1))
                    cfile(f'{user_folder}\\upload.log','w','0')
                    context.bot.edit_message_text(chat_id=user_id,
                                                  message_id=dn_msg.message_id,
                                                  text="Photo Saved ✅")
                    
                    context.bot.send_message(chat_id = user_id,text="chose options👇",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                except:
                    context.bot.edit_message_text(chat_id=user_id,
                                                  message_id=dn_msg.message_id,
                                                  text="Can't download picture ❌")

    else:
        update.message.reply_text("Can't save ❌")


def video_handler(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_folder = f"{BotUsers}\\{user_id}"
    user_filesize = update.message.video.file_size
    user_fileid = update.message.video.file_id

    upload_selected = cfile(f'{user_folder}\\upload.log')

    if upload_selected == '1':
        try:
            if not os.path.exists(f"{DownLoad}\\{str(user_fileid)}.mp4"):
                cheking_msg = update.message.reply_text("cheking video🎬...")

                if user_filesize > 15000000:
                    context.bot.edit_message_text(chat_id=user_id, 
                            message_id=cheking_msg.message_id,
                            text="File is bigger than 15MB ❌ \n send again.")
                else:
                    pr_msg = update.message.reply_text("Preparation...",reply_markup=RKR())
                    context.bot.deleteMessage(chat_id=user_id, 
                            message_id=pr_msg.message_id)
                    
                    context.bot.edit_message_text(chat_id=user_id, 
                            message_id=cheking_msg.message_id,
                            text="Downloading video🎬...")
                    try:
                        with open(f"{DownLoad}\\{str(user_fileid)}.mp4", 'wb') as f:
                            context.bot.get_file(update.message.video).download(out=f)
                            
                        context.bot.edit_message_text(chat_id=user_id, 
                                message_id=cheking_msg.message_id,
                                text=f"Successfuly saved ✅ \n\n File name: {str(user_fileid)}")
                        
                        cfile(f'{user_folder}\\upload.log','w','0')

                        context.bot.send_message(chat_id = user_id,text="chose options👇",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                    except:
                        context.bot.edit_message_text(chat_id=user_id, 
                                message_id=cheking_msg.message_id,
                                text="Can't download video ❌")
            else:
                context.bot.edit_message_text(chat_id=user_id, 
                                message_id=cheking_msg.message_id,
                                text="Can't save data becuase file is curently exist❕")
                
        except:
            context.bot.edit_message_text(chat_id=user_id, 
                            message_id=cheking_msg.message_id,
                            text="Incomplete operation ❌")
            
    else:
        update.message.reply_text("Can't save ❌")


def audio_handler(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_folder = f"{BotUsers}\\{user_id}"
    user_filename = update.message.audio.file_name

    upload_selected = cfile(f'{user_folder}\\upload.log')

    if upload_selected == '1':
        try:
            if not os.path.exists(f"{DownLoad}\\{str(user_filename)}"):
                pr_msg = update.message.reply_text("Preparation...",reply_markup=RKR())
                context.bot.deleteMessage(chat_id=user_id, 
                        message_id=pr_msg.message_id)
                    
                dn_msg = update.message.reply_text("Downloading audio🎵...")

                try:
                    with open(f"{DownLoad}\\{str(user_filename)}.mp3", 'wb') as f:
                            context.bot.get_file(update.message.audio).download(out=f)

                    context.bot.edit_message_text(chat_id=user_id, 
                            message_id=dn_msg.message_id,
                            text=f"Successfuly saved ✅ \n\n File name: {str(user_filename)}")
                                    
                    cfile(f'{user_folder}\\upload.log','w','0')

                    context.bot.send_message(chat_id = user_id,text="chose options👇",
                            reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
                except:
                    context.bot.edit_message_text(chat_id=user_id, 
                                    message_id=dn_msg.message_id,
                                    text="Can't download audio ❌")
        except:
               context.bot.edit_message_text(chat_id=user_id, 
                            message_id=dn_msg.message_id,
                            text="Incomplete operation ❌")
    else:
        update.message.reply_text("Can't save ❌")


def document_handler(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_folder = f"{BotUsers}\\{user_id}"
    user_filename = update.message.document.file_name

    upload_selected = cfile(f'{user_folder}\\upload.log')

    if upload_selected == '1':
    
        pr_msg = update.message.reply_text("Preparation...",reply_markup=RKR())
        context.bot.deleteMessage(chat_id=user_id, 
                message_id=pr_msg.message_id)
        
        dn_msg = update.message.reply_text("Downloading file📁...")

        try:
            context.bot.get_file(update.message.document)

            with open(f"{DownLoad}\\{str(user_filename)}", 'wb') as f:
                context.bot.get_file(update.message.document).download(out=f)

            context.bot.edit_message_text(chat_id=user_id,
            message_id=dn_msg.message_id,
            text=f"Successfuly saved ✅ \n\n File name: {str(user_filename)}")

            cfile(f'{user_folder}\\upload.log','w','0')

            context.bot.send_message(chat_id = user_id,text="chose options👇",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
        except:
            context.bot.edit_message_text(chat_id=user_id, 
                                          message_id=dn_msg.message_id,
                                          text="Can't download file ❌")
    else:
        update.message.reply_text("Can't save ❌")


def voice_handler(update: Update, context: cbc):
    user_id = update.message.chat.id
    user_folder = f"{BotUsers}\\{user_id}"

    upload_selected = cfile(f'{user_folder}\\upload.log')
    voiceplayer_selected = cfile(f'{user_folder}\\play_voice.log')

    if upload_selected == '1':
        try:            

            pr_msg = update.message.reply_text("Preparation...",reply_markup=RKR())
            context.bot.deleteMessage(chat_id=user_id, 
                    message_id=pr_msg.message_id)
            
            dn_msg = update.message.reply_text("Downloading voice🎙️...")
            try:
                with open(f"{DownLoad}\\{update.message.voice.file_unique_id}.mp3", 'wb') as f:
                    context.bot.get_file(update.message.voice).download(out=f)

                context.bot.edit_message_text(chat_id = user_id,
                                            message_id = dn_msg.message_id,
                                            text=f"Successfuly saved ✅ \n\n File name: {str(update.message.voice.file_unique_id)}.mp3")
                cfile(f'{user_folder}\\upload.log','w','0')

                context.bot.send_message(chat_id = user_id,text="chose options👇",
                                    reply_markup = RKM(main_button,resize_keyboard=True,one_time_keyboard=True))
            except:
                context.bot.edit_message_text(chat_id = user_id,
                                            message_id = dn_msg.message_id,
                                            text="Can't download voice ❌")
        except:
            context.bot.edit_message_text(chat_id = user_id,
                                          message_id = dn_msg.message_id,
                                          text="Incomplete operation ❌")
    elif voiceplayer_selected == '1':
        try:            
            dn_msg = update.message.reply_text("Downloading voice🎙️...")
            try:
                with open(f"{VoicePlayer}\\{update.message.voice.file_unique_id}.mp3", 'wb') as f:
                    context.bot.get_file(update.message.voice).download(out=f)

                subcall(f"{VoicePlayer}\\{update.message.voice.file_unique_id}.mp3",shell=True)
                context.bot.edit_message_text(chat_id = user_id,
                                            message_id = dn_msg.message_id,
                                            text='🔉‌')
            except:
                context.bot.edit_message_text(chat_id = user_id,
                                            message_id = dn_msg.message_id,
                                            text="Can't download voice ❌")
        except:
            context.bot.edit_message_text(chat_id = user_id,
                                          message_id = dn_msg.message_id,
                                          text="Incomplete operation ❌")
            
    else:
        update.message.reply_text("Can't save ❌")

try:
    updater.dispatcher.add_handler(comh('start',start))
    updater.dispatcher.add_handler(comh('info',info))
    updater.dispatcher.add_handler(cqh(queryHandler))
    updater.dispatcher.add_handler(msgh(Filters.text, user_message))
    updater.dispatcher.add_handler(msgh(Filters.photo, photo_handler))
    updater.dispatcher.add_handler(msgh(Filters.video, video_handler))
    updater.dispatcher.add_handler(msgh(Filters.audio, audio_handler))
    updater.dispatcher.add_handler(msgh(Filters.document, document_handler))
    updater.dispatcher.add_handler(msgh(Filters.voice, voice_handler))
except:
    pass

class BotGUI:

    def __init__(self, master):
        # Bot state
        self.master = master
        master.title("My Bot")
        self.is_active = False

        # Create widgets
        self.input = Entry(master, width=40) # Input box
        self.input.insert(0, "Bot Token")
        self.input.grid(row=0, column=0, columnspan=2)

        self.btn_submit = Button(master, text="Submit Token", command=lambda: self.submit_input(self.input.get())) # Submit button
        self.btn_submit.grid(row=0, column=2)

        self.btn_start = Button(master, text="Start Bot", command=self.start_bot) # Start button
        self.btn_start.grid(row=2, column=0)

        self.btn_stop = Button(master, text="Stop Bot", command=self.stop_bot) # Stop button
        self.btn_stop.grid(row=2, column=1)

        self.indicator = Label(master, text="Bot Status", bg="red", fg="white") # Status indicator
        self.indicator.grid(row=2, column=2)

        self.logs = Text(master, width=60, height=10) # Text console
        self.logs.grid(row=3, column=0, columnspan=3)

        self.publisher = Label(master, text="Powered by Hani Torbati", cursor="hand2")
        self.publisher.grid(row=4 , column=0, columnspan= 3)

        url= r'https://t.me/finito_cosito'
        def open_url(url):
            open_new_tab(url)

        self.publisher.bind("<Button-1>", lambda e: open_url(url))

        # Log example message
        if token_read_status != 0:
            self.log("Bot is ready!")
        else:
            self.indicator["bg"] = "orange"
            self.log("Token Not Found!")
            self.btn_start["state"] = DISABLED 

    def start_bot(self):           
        try:
            updater.start_polling()
            self.indicator["bg"] = "green"
            self.log("Bot is online!")
        except:
            self.indicator["bg"] = "orange"
            self.log("Network Error!")

    def stop_bot(self):
        updater.stop()
        self.indicator["bg"] = "red"
        self.log("Bot is offline!")


    def submit_input(self, message):
        try:
            user_token_input = self.input.get()
            cfile(f'{BotInfo}\\token.txt',"w",user_token_input)
            self.log('Token saved. please restart the Bot.')
        except:
            self.log('can not save Token!')
            self.log(f'Please save it by your self in \n {BotInfo}\\token.txt')

    def log(self, message):
        self.logs.insert(END, message + "\n")

    


root = Tk()
app = BotGUI(root)
root.mainloop()
