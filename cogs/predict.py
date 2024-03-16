import tensorflow as tf
import numpy as np
import discord
from discord.ext import commands
import json
import requests
from PIL import Image
import shutil
import os
#from music import predicted #creating errors, need to change cog ordering to fix this

from main import bot_chan

class Predict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = tf.lite.Interpreter(model_path="model/overwatch_img_model.tflite")
        self._input_details = self.model.get_input_details()
        self._output_details = self.model.get_output_details()
        self.img_height = 250
        self.img_width = 250
        with open("train.json", "r") as file:
            self.class_names = json.load(file)
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.get_channel(bot_chan).send("bot is ready, here is the graph for the current model being used")
        await self.bot.get_channel(bot_chan).send(file=discord.File(r"training_validation_loss.png"))

    @commands.command(pass_context=True)
    async def predict(self, ctx):
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if msg.attachments:
            image_url = msg.attachments[0].url
            if "jpg" in image_url:
                ext = ".jpg"
            elif "png" in image_url: #convert to jpg
                ext = ".png"
            else:
                raise Exception("That format does not work, please do PNG or JPG")
    
            file = requests.get(image_url, allow_redirects=True, stream=True)
            file_loc = f"temp{ext}"
            with open(file_loc, "wb") as out_file:
                shutil.copyfileobj(file.raw, out_file)
            img = Image.open(file_loc)
            file_loc = f"temp.jpg"
            img = img.convert("RGB")

            #must be jpg
            img = img.resize((self.img_height, self.img_width), Image.ANTIALIAS)
            img_array = np.array(img, dtype=np.float32)
            img_array = tf.expand_dims(img_array, 0)
            self.model.allocate_tensors()
            self.model.set_tensor(self._input_details[0]['index'], img_array)
            self.model.invoke()
            output_data = self.model.get_tensor(self._output_details[0]['index'])
            #predictions = self.model.predict(img_array)
            score = tf.nn.softmax(output_data)

            await ctx.send(self.class_names[np.argmax(score)])
            await self.bot.get_channel(bot_chan).send(f"{self.class_names[np.argmax(score)]} with {100 * np.max(score)} confidence")
            global predicted
            predicted = self.class_names[np.argmax(score)]

        else:
            raise Exception("No attachment found")

    @predict.error
    async def pred_error(self, ctx, error):
        await ctx.send(f"An error occured: {error}")
        await self.bot.get_channel(bot_chan).send(f"There was an error in {ctx.channel} with error of: {error} \n requested by {ctx.author}")

def setup(bot):
    bot.add_cog(Predict(bot))