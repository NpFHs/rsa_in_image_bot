import os

import telepot
import numpy
from PIL import Image
import rsa
import time
import requests

import urllib3

# # You can leave this bit out if you're using a paid PythonAnywhere account
# proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#     'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
# telepot.api._onetime_pool_spec = (
#     urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# # end of the stuff that's only needed for free accounts

BOT_TOKEN = "6251350454:AAFVGRmcdfWbXFT1V_BVs174RSYnGcRFBDo"

bot = telepot.Bot(BOT_TOKEN)  # NOQA
public_key, private_key = rsa.newkeys(2048)

image_path = "image_file.png"


def bin_to_image(bin_msg):
    # create blank image
    image_arr = numpy.zeros((1, 256, 3), dtype=numpy.uint8)
    counter = 0
    for bin_char in bin_msg.split():
        bin_tuple = (bin_char[:2], bin_char[2:5], bin_char[5:8])
        image_arr[0][counter] = bin_tuple
        counter += 1
    height = 16
    width = 16
    image_arr = image_arr.reshape((height, width, 3))
    image = Image.fromarray(image_arr)
    image.save(image_path)


def image_to_bin(path):
    image = Image.open(path)
    image_arr = numpy.asarray(image)  # NOQA
    image_arr = image_arr.reshape((1, 256, 3))
    bin_msg = ""
    for bin_tuple in image_arr[0]:
        fixed_size_bin_tuple = str(bin_tuple).strip("[] ").split()
        bin_char = ""
        for fixed_size_bin in fixed_size_bin_tuple:
            bin_char += fixed_size_bin.zfill(3)
        bin_char = bin_char[1:]
        bin_msg = f"{bin_msg} {bin_char}"
    bin_msg = bin_msg.strip(" ")
    return bin_msg


def get_file(file_id):
    file_path = bot.getFile(file_id)["file_path"]
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    r = requests.get(file_url)
    create_file = open(f"./files/{file_path}", "x")
    create_file.close()
    with open(f"./files/{file_path}", "wb") as img:
        img.write(r.content)
    return f"./files/{file_path}"


def bin_to_dec(bin_num):
    str_num = str(bin_num)
    counter = len(str_num) - 1
    dec_num = 0
    for i in str_num:
        dec_num += int(i) * (2 ** counter)
        counter -= 1
    return dec_num


def encrypt(msg):
    enc_msg = rsa.encrypt(msg.encode(), public_key)
    return enc_msg


def decrypt(enc_msg):
    org_msg = rsa.decrypt(enc_msg, private_key)
    return org_msg.decode()


def msg_to_bytes(msg):
    bytes_list = []
    for char in msg:
        # bin_char = str(bin(char))[2:].zfill(16)
        bin_char = str(bin(char))[2:].zfill(8)
        bytes_list.append(bin_char)
    bytes_msg = " ".join(bytes_list)
    return bytes_msg


def bytes_to_msg(bin_msg):
    org_msg_list = []
    for i in bin_msg.split(" "):
        hex_msg = hex(bin_to_dec(i))[2:].zfill(2)
        org_msg_list.append(bytes.fromhex(hex_msg))
    return b"".join(org_msg for org_msg in org_msg_list)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == "document":
        file_path = get_file(msg["document"]["file_id"])
        bin_msg = image_to_bin(file_path)
        enc_msg = bytes_to_msg(bin_msg)
        try:
            org_msg = decrypt(enc_msg)
            response = org_msg
        except rsa.pkcs1.DecryptionError:
            response = "Decryption failed"
        os.remove(file_path)
        bot.sendMessage(chat_id, response)

    elif content_type == "text":
        enc_msg = encrypt(msg["text"])
        bin_msg = msg_to_bytes(enc_msg)
        bin_to_image(bin_msg)
        bot.sendDocument(chat_id, document=open("image_file.png", "rb"))
        response = "done."
        bot.sendMessage(chat_id, response)


bot.message_loop(handle)

print('Listening ...')

# Keep the program running.
while True:
    time.sleep(10)
