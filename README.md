# Image RSA encryption
This is a Python script for a Telegram Bot that can encrypt and decrypt messages using RSA cryptography, as well as convert messages to and from binary format and images.

![image_2023-02-19_21-43-33](https://user-images.githubusercontent.com/87757968/219971293-4937f831-d9cc-4eb2-9958-21234d676b06.png)

To run the script, you will need to have Python 3 installed on your machine, as well as the following libraries:

-   telepot
-   numpy
-   pillow
-   rsa
-   time
-   requests
-   (urllib3)

You can install the libraries using pip:

`pip install telepot numpy pillow rsa requests urllib3` 

To use the bot, you will need to create a Telegram Bot and obtain a Bot Token from BotFather. You can then replace the placeholder value for `BOT_TOKEN` with your own token.

The bot listens for messages from users and performs different actions depending on the content of the message. If the message is a document, the bot will download the file and convert it to a binary string, which it will then attempt to decrypt using the RSA private key. If the decryption is successful, the bot will send the decrypted message back to the user. If the message is text, the bot will encrypt the message using the RSA public key, convert the encrypted message to a binary string, and then generate an image file from the binary string. The bot will then send the image file to the user.

Note that the script includes code for using a proxy server, which is only necessary if you are using a free PythonAnywhere account. If you are not using a proxy server, you can remove this code.

To run the script, simply execute it from the command line:

`python3 telegram_bot.py` 

The script will run indefinitely, listening for messages from users. To stop the script, you can use `Ctrl + C` in the command line.

![visitors](https://visitor-badge.glitch.me/badge?page_id=NpFHs.rsa_in_image_bot&left_color=green&right_color=blue)

