# Overwatch-Bot
This is a machine learning bot that will identify the different characters within Overwatch and play voice lines from each one of them

Process:
The model must be pretrained from the training_pc.py file, this was done since newer versions of tensorflow is not available with ARM based devices like a Raspberry pi then converted to a tflite 16f file for speed within discord so the bot is cappable of responding quickly. 

.env file structure: 

Discord_token = TOKEN
owner_id = YOUR_ID
aaron_id = ANOTHER_OWNERS_ID
error_chan = CHANNEL_FOR_ERRORS


Currently working on:
- Play music from spotify and youtube with allowing the voice lines
- Improve current CNN model for better training in fewer images with more character options
- LSTM RNN for TTS options (2 models needed) for each character's phasing and wording choice
- Make the bot support guilds on discord