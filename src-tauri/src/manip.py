import os
import sys
import wave
from pydub import AudioSegment as AudiSeg
from cryptography.fernet import Fernet

class AudiCrypt:
    # python 0:filename.py 1:encrypt/decrypt 2:filepath 3:message
    def __init__(self) -> None:
        self.original_filepath = sys.argv[2] # calls to this py file will fail if not enough argvs are present
        self.original_filedir = os.path.dirname(self.original_filepath)
        self.original_filename = os.path.basename(self.original_filepath).split(".")[0] 
        self.original_wav_path = os.path.join(self.original_filedir, "original.wav")
        self.encrypted_wav_path = os.path.join(self.original_filedir, f"{self.original_filename}.wav") # output to where ever the original sound file came from
        self.output_format = "wav"
        self.encryption_key = b'YjwFBT6dQLGcGtq3yVEGkYUdRiJXjrxWaEHgR5tXX8o=' # a fixed encryption key
        self.encryption = Fernet(self.encryption_key)

        if sys.argv[1] == "encrypt":
            self.encrypt(filepath=sys.argv[2], message=str(sys.argv[3]))
        if sys.argv[1] == "decrypt":
            self.decrypt(filepath=sys.argv[2])

    # acceptable filename includes the path to it   
    def audicrypt_to_wav(self, filepath:str) -> bool:
        try:
            if os.path.exists(self.original_wav_path): # remove existing original file
                os.remove(self.original_wav_path)
            if os.path.exists(self.encrypted_wav_path): # remove existing encrypted file
                os.remove(self.encrypted_wav_path)

            original_audio = AudiSeg.from_file(filepath)
            original_audio.export(self.original_wav_path, format=self.output_format) # exports the new wav file to the current directory
            return True
        except:
            print("Failed to convert audio file to wav format.")
            return False

    def encrypt(self, filepath:str, message:str="HackUMBC22") -> bool:
        try:
            self.audicrypt_to_wav(filepath)
            audio = wave.open(self.original_wav_path, mode="rb")
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes()))) # turns every frame of the audio file into a byte array

            message = self.encryption.encrypt(message.encode()) # encrypts the message using a fixed key
            encrypted_message = message + (int((len(frame_bytes)-(len(message)*8*8))/8) *'*').encode() # extend the encrypted message with garbage values to match amount of frames

            ascii_chars = []
            for _ in encrypted_message:
                single_char = bin(_).lstrip('0b').rjust(8, '0') # casts chars into ints into binary, strips the leading 0b and fill the stripped space with 0s
                ascii_chars.append(single_char)
            ascii_chars = "".join(ascii_chars)

            binary_bits = map(int, ascii_chars) 
            list_of_binaries = []
            for _ in binary_bits:
                list_of_binaries.append(_) # maps ascii characters of the chars in the message to integers and append them to a list

            for i in range(len(list_of_binaries)): 
                frame_bytes[i] = (frame_bytes[i] & 254) | list_of_binaries[i] # the actual steganography, places the binaries of the message in the least significant bits

            frame_modified = bytes(frame_bytes)
            newAudio = wave.open(self.encrypted_wav_path, 'wb')
            newAudio.setparams(audio.getparams())
            newAudio.writeframes(frame_modified)

            newAudio.close()
            audio.close()

            if self.original_wav_path: # deletes the original wav file
                os.remove(self.original_wav_path)
            print(f"Successfully encoded: {self.encrypted_wav_path}")

            return True
        except:
            print("Failed to encrypt.")
            return False

    def decrypt(self, filepath:str) -> bool:
        try:
            audio = wave.open(filepath, mode='rb') # retrieves the encoded audio file
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes()))) # first step, divide the audio file into byte array
            extracted = []
            for i in range(len(frame_bytes)):
                extracted.append(frame_bytes[i] & 1) # gets the least significant bit from every frame

            to_binary_bits = []
            for i in range(0, len(extracted), 8): # have i increment by 8 bits per iteration to get all necessary bits for a byte
                to_binary_bits.append(map(str, extracted[i : i+8]))
            
            to_binary_chars = []
            for _ in to_binary_bits:
                to_binary_chars.append(chr(int("".join(_), 2))) # casting base 2 integers to chars
            
            encrypted_string = "".join(to_binary_chars) # joining the obtained chars from the audio file gives the encrypted string
            decoded = encrypted_string.split("***")[0] # last step, take out the garbage values

            decoded = self.encryption.decrypt(decoded.encode()).decode() # decrypt to get the hidden message
            print(f"Sucessfully decoded: {decoded}")
            audio.close()

            return True
        except:
            print("Failed to decrypt.")
            return False

if __name__ == "__main__":
    AC = AudiCrypt()


