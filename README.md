# lcd_whiteboard

## What does this project do?
- This project develops a desktop application that has been tested on macOS 12.5.1 and Raspberry Pi OS (Legacy, 32-bit) Debian Bullseye. If installed on compatible hardware, this application provides a touchscreen whiteboard interface. Users can draw on the whiteboard, and it has the added ability to send an image of the whiteboard to anybody's phone via MMS. It uses Twilio (a cloud communications platform) to send these messages. Additionally, Ngrok (a tunneling service) is used to expose the "recipient signup page" to the internet. Users can scan a QR code displayed on the whiteboard UI to access the signup page. By entering their phone number, they are added as a potential recipient to recieve the image of the whiteboard via MMS.

## Why is this project useful?
- This project is useful as it has the potential to enhance classroom settings. Many students face the challenge of trying to listen to their teacher, while simultaneously copying notes. With this techonology, students would be able to add themselves as a recipient at the beginning of class, focus all their attention on the teacher, and the teacher can send the notes directly to the students afterward.

## How can users get started?
- Users will have to make a Twilio account (https://www.twilio.com/en-us) and Ngrok account (https://ngrok.com/), both of which offer free tiers. Then make a file called wb_accounts_config.pkl that contains a python dictionary object with the following information: {'twilio_account_sid': '<your_sid>', 'twilio_auth_token': '<your_twilio_auth_token>', 'twilio_number': '+1XXXXXXXXXX', 'ngrok_auth_token': '<your_ngrok_auth_token>'}. Place this file at  "src/server_side/backend/configs/wb_accounts_config.pkl".

## General workflow:
1. Draw on whiteboard.

![2](https://github.com/user-attachments/assets/fedff052-f458-4c88-b926-41ea57fdf78d)

2. Display QR code.

![3](https://github.com/user-attachments/assets/4aca19e8-d25a-4f0a-b63c-f0bc6282367d)

3. Enter phone number.

![4](https://github.com/user-attachments/assets/72503f9a-1e1c-41cc-9ffc-aeea4181f026)

4. Send image to recipients.

![5](https://github.com/user-attachments/assets/6356fb5d-7c65-4943-9f95-95775b465323)

5. Recieve image on phone.

![6](https://github.com/user-attachments/assets/ab936ac9-bf45-47e8-a7d5-f051eeb8fc3a)
