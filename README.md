# Motion Detection System with Telegram Notifications

This project implements a motion detection system using a computer's camera. When motion is detected, it sends notifications via Telegram and plays an alarm sound.

## Prerequisites

- Python 3.6+
- OpenCV
- Pygame
- A Telegram bot token and chat ID

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/motion-detection-system.git
   cd motion-detection-system
   ```

2. Install required packages:
   ```
   pip install python-dotenv opencv-python imutils pygame requests
   ```

3. Create a `.env` file in the project root and add your Telegram bot token and chat ID:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

4. Ensure you have an `alarm_sound.wav` file in the project directory. If you don't have one, see the "Alarm Sound" section below.

## Usage

Run the script:
```
python motion_detector.py
```

- The system will start in active mode, monitoring for motion.
- Press 'T' to toggle the alarm mode on/off.
- Press 'Q' to quit the program.

## Alarm Sound

The system uses a file named `alarm_sound.wav` for the audible alarm. If you don't have this file:

1. You can download a free .wav sound file from various online sources.
2. Rename the downloaded file to `alarm_sound.wav`.
3. Place it in the same directory as the Python script.

Alternatively, you can modify the `initialize_pygame()` function in the script to use a different sound file name.

## Customization

- Adjust the `notification_cooldown` variable to change how often notifications are sent.
- Modify the motion detection sensitivity by changing the threshold values in the main loop.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).