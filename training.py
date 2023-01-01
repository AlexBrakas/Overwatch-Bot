import os
import numpy as np
import matplotlib.pyplot as plt
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from main import bot_chan


class Training(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @cog_ext.cog_slash(name="train", description="Trains the machine model", options=[
        create_option(
            name="epochs",
            description="Cycles of training to do",
            required=False,
            option_type=4), #int type
        create_option(
            name="batch_size",
            description="Number of images before updating model",
            required=False,
            option_type=4
        )])
  async def train(self, ctx:SlashContext, epochs:int=10, batch_size:int=2):
    #remove log info
    tf.get_logger().setLevel('ERROR') #current keras bug that makes resizing slow, TF v2.8.3 does not have it

    cur_dir = os.getcwd()
    dataset_path = f"{cur_dir}/characters_img"
    data_dir = pathlib.Path(dataset_path)

    image_count = len(list(data_dir.glob('*/*.*')))
    await ctx.reply(f"Processing {image_count} images")

    #number of images before updated
    batch_size = 1

    #resizing amounts
    img_height = 250
    img_width = 250

    #Supported image formats: jpeg, png, bmp, gif. Animated gifs are truncated to the first frame. 
    #80% for training
    train_ds = tf.keras.utils.image_dataset_from_directory(
      data_dir,
      validation_split=0.2,
      subset="training",
      seed=420,
      image_size=(img_height, img_width),
      batch_size=batch_size)

    #20% for validation
    val_ds = tf.keras.utils.image_dataset_from_directory(
      data_dir,
      validation_split=0.2,
      subset="validation",
      seed=420,
      image_size=(img_height, img_width),
      batch_size=batch_size)

    class_names = train_ds.class_names
    await ctx.send(f"found {len(class_names)}: {class_names}")

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    normalization_layer = layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

    num_classes = len(class_names)

    #Data augmentation
    data_augmentation = keras.Sequential(
      [
        layers.RandomFlip("horizontal", input_shape=(img_height, img_width, 3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
      ]
    )

    #dropout
    model = Sequential([
      data_augmentation,
      layers.Rescaling(1./255),
      layers.Conv2D(16, (3,3), padding='same', activation='relu'),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(32, (3,3), padding='same', activation='relu'),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
      layers.MaxPooling2D(2,2),
      layers.Dropout(0.2),
      layers.Flatten(),
      layers.Dense(128, activation='relu'),
      layers.Dense(num_classes, name="outputs")
    ])

    #compile and train model 
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    epochs = 5
    history = model.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs
    )

    #visualize results
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')

    filename = "temp.png"
    plt.savefig(filename)
    await ctx.send(file=filename)
    #self.bot.get_channel(bot_chan).send(file = discord.file(filename=filename))
    os.remove(filename)

    model.save('model/overwatch_img_model')
    await ctx.send(f"Model has been processed and save {model.summary()}")

def setup(bot: commands.bot):
    bot.add_cog(Training(bot))