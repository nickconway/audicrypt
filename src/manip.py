from ftplib import all_errors
import os 
import wave
from pydub import AudioSegment as AudiSeg

class AudiCrypt:
    def __init__(self) -> None:
        self.original_filename = ""
        self.cwd = os.getcwd()
        self.audio_directory = self.cwd+"\\src\\audios"
        self.sample_path = self.audio_directory+"\\sample.mp3" # sample from https://file-examples.com/index.php/sample-audio-files/sample-mp3-download/
        self.original_output_path = self.audio_directory+"\\original.wav"
        self.encrypted_output_path = self.audio_directory+"\\encrypted.wav"
        self.output_format = "wav"

    # acceptable filename includes the path to it   
    def audicrypt_to_wav(self, filepath:str=None) -> bool:
        try:
            filepath = filepath if filepath else self.sample_path
            if os.path.isfile(self.original_output_path): # remove existing original file
                os.remove(self.original_output_path)
            if os.path.isfile(self.encrypted_output_path): # remove existing encrypted file
                os.remove(self.original_output_path)
        
            original_audio = AudiSeg.from_file(filepath)
            original_audio.export(self.original_output_path, format=self.output_format) # exports the new wav file to the current directory
            return True
        except:
            return False

    def encode(self, message:str) -> None:
        print("\nEncoding Starts..")
        audio = wave.open(self.original_output_path, mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)
        newAudio = wave.open(self.original_output_path, 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        print(f" |---->succesfully encoded inside {self.encrypted_output_path}")

    def decode(self):
        print("\nDecoding Starts..")
        audio = wave.open("output.wav", mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        decoded = string.split("###")[0]
        print("Sucessfully decoded: "+decoded)
        audio.close()	

if __name__ == "__main__":
    AC = AudiCrypt()
    AC.audicrypt_to_wav(os.getcwd()+"\\src\\audios\\sample.mp3")
    while True:
        print("\nSelect an option: \n1)Encode\n2)Decode\n3)exit")
        val = int(input("\nChoice:"))
        
        if val == 1:
            AC.encode("Something something Nick's gay")
        if val == 2:
            AC.decode()
        if val not in [1,2]:
            break


