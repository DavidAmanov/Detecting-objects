#!pip install pyTelegramBotAPI При необходимости
#!pip install imageai При необходимости
#Будьте внимательны с путями до модели, до изображения, до места куда будет сохранятся изображение.
#Код можно использовать в гугл колабе
import telebot
import os


def clear_content(chat_id):
    try:
        for img in images[chat_id]:
            os.remove(img)
    except Exception as e:
        clear_content(chat_id)
    images[chat_id] = []


def detected(image_path):
    from imageai.Detection import ObjectDetection
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("/content/yolov3.pt")  # тут должен быть путь до вашей модели
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=image_path,
                                                 output_image_path="/content/photos/imagenew.jpg",
                                                 minimum_percentage_probability=30)
    import cv2
    from matplotlib import pyplot as plt
    img = cv2.imread("/content/photos/imagenew.jpg", cv2.IMREAD_COLOR) #Путь до вашей картинки
    output_path = "/content/photos/imagenew.jpg" #Путь выхода картинки с определенными объектами
    return output_path

    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_image)


images = dict()

bot = telebot.TeleBot('YOUR TG TOKEN')  # Сюда нужно вбить свой телеграм токен, который вам выдаст BotFather


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Hello, send me photo")


@bot.message_handler(content_types=['photo'])
def photo(message):
    print(message.photo[:-2])
    images[str(message.chat.id)] = []
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        src = "/content/" + file_info.file_path

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        images[str(message.chat.id)].append(src)
    except Exception as e:
        bot.reply_to(message, e)

    print('img: ', images)
    print(images)
    reply_img = ''
    if (len(images[str(message.chat.id)]) == 1):
        reply_img = detected(images[str(message.chat.id)][0])
        images[str(message.chat.id)].append(reply_img)
        bot.send_photo(message.chat.id, open(reply_img, 'rb'))
        clear_content(str(message.chat.id))
    print(images)


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, "Hello, send me photo")


bot.polling(none_stop=True)