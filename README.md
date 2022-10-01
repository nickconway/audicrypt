# Audicrypt
Audicrypt is a cross-platform application for encryption and steganography using audio files. Project was created as part of the HackUMBC hackathon 2022. 

<img src="src/assets/logo.png" height="100" />

## Introduction
Audio steganography is a technique of embedding messages into sound files. This hides the existence of the encrypted message, providing additional security to the users.

## Overview
The main technique used in this project is the LSB-steganography process, in which all of the least significant bits(LSB) in an audio file is replaced with a bit from the message. Adding the bits from the message into the audio file in the form of small, unnoticeable noises makes the detection of the existence of the message more difficult. However, once the noises are discoverd, it would be fairly easy to obtain all of the LSB to decode the message. This is where our second technique, message encryption, comes in. Therefore, even if the attacker obtains the least significant bits from the audio, it would either look like garbage values or at the very minimum provide great security to the message. Currently, the project supports wav, mp3, FLAC, and OGG audio file formats.

## Tools
Follow this [guide](https://tauri.app/v1/guides/getting-started/prerequisites) to set up the toolchain required for this project.

## Installation
```
$ git clone https://github.com/nickconway/audicrypt
$ cd audicrypt
$ pip install -r requirements.txt
```

## Run
```
$ cd audicrypt
$ cargo tauri dev
```

## Usage
When prompted, enter a message to be encrypted and choose an audio file to encrypt into. Once you have an encrypted audio file, you can choose that file to decrypt. 
* Note: the original audio file will be replaced by a wav file of the same name if encryption is successful.

## Errors
Sometimes, you might encounter an error where ffmpeg or ffprobe cannot be found. One way to resolve this is to place the bin folder of the missing package directly into your PATH environment variables. Similarily, if any of the installed packages are not working, try placing their bins in the PATH.

## Future plans
Currently, we plan on expanding the acceptable encryption file types to include all formats. Allowing the encryption of messages into pdf, text, image, and video files. We also plan on adding a send and receive feature to facilitate the sharing of the encrypted file. Our encryption method uses a fixed key, which is highly vulnerable and in the near future we plan on adding assymetric encryption to boost the security of the messages. 
