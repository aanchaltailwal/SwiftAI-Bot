import telebot
from loguru import logger
import os
import requests
from collections import Counter
import openai
import ffmpeg
import shutil

YOLO_URL = 'http://yolo5-service:8081'


class Bot:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.bot.set_update_listener(self._bot_internal_handler)

        self.current_msg = None

    def _bot_internal_handler(self, messages):
        """Bot internal messages handler"""
        for message in messages:
            self.current_msg = message
            self.handle_message(message)

    def start(self):
        """Start polling msgs from users, this function never returns"""
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        logger.info(f'Telegram Bot information\n\n{self.bot.get_me()}')

        self.bot.infinity_polling()

    def send_text(self, text):
        self.bot.send_message(self.current_msg.chat.id, text)

    def send_text_with_quote(self, text, message_id):
        self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)

    def is_current_msg_photo(self):
        return self.current_msg.content_type == 'photo'

    def is_current_msg_video(self):
        return self.current_msg.content_type == 'video'

    def download_user_photo(self, quality=2):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2]
        :return:
        """
        if not self.is_current_msg_photo():
            raise RuntimeError(
                f'Message content of type \'photo\' expected, but got {self.current_msg.content_type}')

        file_info = self.bot.get_file(self.current_msg.photo[quality].file_id)
        data = self.bot.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def download_user_video(self, quality=2):
        if not self.is_current_msg_video():
            raise RuntimeError(f'Message content of type \'video\' expected, but got {self.current_msg.content_type}')

        file_info = self.bot.get_file(self.current_msg.video.file_id)
        data = self.bot.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_image(self,image,caption,message_id):
        self.bot.send_photo(self.current_msg.chat.id, photo=image, caption=caption, reply_to_message_id=message_id)

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        self.send_text(f'Your original message: {message.text}')




class QuoteBot(Bot):
    def handle_message(self, message):
        logger.info(f'Incoming message: {message}')

        if message.text != 'Please don\'t quote me':
            self.send_text_with_quote(message.text, message_id=message.message_id)




class ObjectDetectionBot(Bot):
    def handle_message(self, message):
        logger.info(f'Incoming message: {message}')

        if message.chat.type == 'private' or ():
            if self.is_current_msg_photo():
                self.detect_objects()
            if self.is_current_msg_video():
                self.detect_objects_in_video()


    def detect_objects(self):
        photo_path = self.download_user_photo()

        # Send the photo to the YOLO service for object detection
        res = requests.post(f'{YOLO_URL}/predict', files={
            'file': (photo_path, open(photo_path, 'rb'), 'image/png')
        })

        if res.status_code == 200:
            detections = res.json()
            logger.info(f'response from detect service with {detections}')

            # calc summary
            element_counts = Counter([l['class'] for l in detections])
            summary = 'Objects Detected:\n'
            for element, count in element_counts.items():
                summary += f"{element}: {count}\n"

            self.send_text_with_quote(summary, message_id=self.current_msg.message_id)

            # Delete the photo file
            os.remove(photo_path)

        else:
            self.send_text('Failed to perform object detection. Please try again later.')


    def detect_objects_in_video(self):
        if self.is_current_msg_video():
            video_path = self.download_user_video()

            if os.path.exists('frames'):
                shutil.rmtree('frames')

            os.mkdir('frames')

            output_file = 'frames/output_%04d.jpg'
            framerate = '1'
            ffmpeg.input(video_path).output(output_file, r=framerate).run()

            frame_predictions = []  # List to store predictions for each frame

            for root, dirs, files in os.walk('frames'):
                for file in files:
                    if file.endswith('.jpg'):
                        image_path = os.path.join(root, file)

                        res = requests.post(f'{YOLO_URL}/predict', files={
                            'file': (image_path, open(image_path, 'rb'), 'image/png')
                        })

                        if res.status_code == 200:
                            predictions = res.json()
                            logger.info(f'Response from detect service with {predictions}')
                            frame_predictions.append(predictions)

                        else:
                            self.send_text('Failed to perform object detection on some frames. Please try again later.')

            # Aggregate predictions into a dictionary
            aggregated_predictions = Counter()
            for predictions in frame_predictions:
                aggregated_predictions.update([obj['class'] for obj in predictions])

            summary = 'Objects Detected:\n'
            for element, count in aggregated_predictions.items():
                summary += f"{element}\n"

            self.send_text_with_quote(summary, message_id=self.current_msg.message_id)

            # Delete the video file
            os.remove(video_path)

        else:
            self.send_text('Please send a video for object detection.')


    def search_gpt(self, query):
        # Generate a response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7, )

        response = completion.choices[0].message.content

        return response


    def draw_image(self, query):
        # Generate a response
        response = openai.Image.create(
            prompt=query,
            n=1,
            size="256x256"
        )

        image_url = response['data'][0]['url']

        return image_url




if __name__ == '__main__':

    _token = os.getenv("_token")


    openai.api_key = os.getenv("openAi_key")

    my_bot = ObjectDetectionBot(_token)


    @my_bot.bot.message_handler(commands=['start'])
    def handle_start(message):
        my_bot.send_text('Welcome to the SwiftAI Bot. Click on /help to get started.')


    @my_bot.bot.message_handler(commands=['help'])
    def handle_help(message):
        help_text = 'How to use the bot:\n\n' \
                    '/start - Start the bot and get a welcome message\n' \
                    '/help - Get instructions on how to use the bot\n' \
                    '/yolo - Tag an image with this command to detect objects\n' \
                    '/vid - Tag a video with this command to detect objects\n' \
                    '/chatgpt - Write a query to search on ChatGPT\n' \
                    '/draw - Generate an image based on a prompt\n'
        my_bot.send_text(help_text)


    @my_bot.bot.message_handler(commands=['yolo'])
    def handle_yolo(message):
        if message.reply_to_message and message.reply_to_message.photo:
            my_bot.current_msg = message.reply_to_message
            my_bot.detect_objects()
        else:
            my_bot.send_text('Please tag an image for object detection.')


    @my_bot.bot.message_handler(commands=['vid'])
    def handle_vid(message):
        if message.reply_to_message and message.reply_to_message.video:
            my_bot.current_msg = message.reply_to_message
            my_bot.detect_objects_in_video()
        else:
            my_bot.send_text('Please tag a video for object detection.')



    @my_bot.bot.message_handler(commands=['chatgpt'])
    def handle_chatgpt(message):
        # Extract the query by removing '/chatgpt' from the start of the message text
        query = message.text.replace('/chatgpt', '').strip()
        # Call the gpt() function with the extracted query
        response = my_bot.search_gpt(query)

        my_bot.send_text_with_quote(response, message_id=message.message_id)


    @my_bot.bot.message_handler(commands=['draw'])
    def handle_draw(message):
        # Extract the prompt by removing '/draw' from the start of the message text
        query = message.text.replace('/draw', '').strip()
        # Call the gpt() function with the extracted query
        image_url = my_bot.draw_image(query)

        if image_url:
            caption="Prompt: "+query.capitalize()
            my_bot.send_image(image_url,caption, message_id=message.message_id)
        else:
            my_bot.send_text_with_quote("Failed to generate the image.",message_id=message.message_id)



    my_bot.start()
