import os
from dotenv import load_dotenv
import threading
import pygame
import cv2 
import imutils
import time
import requests

# Load environment variables
load_dotenv()

def initialize_pygame():
    pygame.mixer.init()
    sound_file = 'sound.ogg'
    if not os.path.exists(sound_file):
        print(f"Warning: {sound_file} not found. Sound will not play.")
        return None
    return pygame.mixer.Sound(sound_file)

def play_alarm(sound):
    print("ALARM")
    if sound:
        sound.play()

def send_telegram_message(bot_token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Telegram notification sent: {message}")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

def main():
    # Telegram configuration
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        print("Error: Telegram bot token or chat ID not found in environment variables.")
        return

    alarm_sound = initialize_pygame()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    _, start_frame = cap.read()
    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    alarm_mode_active = True
    motion_detected = False
    last_motion_time = time.time()
    motion_stop_notified = False
    notification_cooldown = 60  # 1 minute cooldown for motion detection messages

    try:
        while True: 
            _, frame = cap.read()
            frame = imutils.resize(frame, width=500)

            if alarm_mode_active: 
                frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

                difference = cv2.absdiff(frame_bw, start_frame)
                threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
                start_frame = frame_bw

                motion = threshold.sum() > 300

                current_time = time.time()

                if motion:
                    last_motion_time = current_time
                    if not motion_detected:
                        motion_detected = True
                        motion_stop_notified = False
                        print("Motion detected!")
                        play_alarm(alarm_sound)
                        threading.Thread(target=send_telegram_message, 
                                         args=(bot_token, chat_id, "Motion detected in your room!")).start()
                elif motion_detected and (current_time - last_motion_time) > 30 and not motion_stop_notified:
                    motion_detected = False
                    motion_stop_notified = True
                    print("No motion for 30 seconds.")
                    threading.Thread(target=send_telegram_message, 
                                     args=(bot_token, chat_id, "No motion detected for 30 seconds.")).start()

                cv2.imshow("View", threshold)
            else: 
                cv2.imshow("View", frame)

            key_pressed = cv2.waitKey(30)
            if key_pressed == ord("t"): 
                alarm_mode_active = not alarm_mode_active
                motion_detected = False
                motion_stop_notified = False
            if key_pressed == ord("q"): 
                break 

    finally:
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()

if __name__ == "__main__":
    main()