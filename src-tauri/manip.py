import os 
import sys
import wave
from pydub import AudioSegment as AudiSeg

class AudiCrypt:
    # python 0:filename.py 1:encrypt/decrypt 2:filepath 3:message
    def __init__(self) -> None:
        self.original_filepath = sys.argv[2]
        self.cwd = os.getcwd()
        self.audios_directory = self.cwd+"\\audios"
        self.original_wav_path = self.audios_directory+"\\original.wav"
        self.encrypted_wav_path = self.audios_directory+"\\encrypted.wav"
        self.output_format = "wav"

        if sys.argv[1] == "encrypt":
            self.encode(filepath=sys.argv[2], message=str(sys.argv[3]))
        if sys.argv[1] == "decrypt":
            self.decode(filepath=sys.argv[2])

    # acceptable filename includes the path to it   
    def audicrypt_to_wav(self, filepath:str) -> bool:
        try:
            if not os.path.isdir(self.audios_directory):
                os.makedirs(self.audios_directory)
            if os.path.isfile(self.original_wav_path): # remove existing original file
                os.remove(self.original_wav_path)
            if os.path.isfile(self.encrypted_wav_path): # remove existing encrypted file
                os.remove(self.original_wav_path)
        
            original_audio = AudiSeg.from_file(filepath)
            original_audio.export(self.original_wav_path, format=self.output_format) # exports the new wav file to the current directory
            return True
        except:
            return False

    def encode(self, filepath:str, message:str="HackUMBC22") -> None:
        try:
            audio = wave.open(filepath, mode="rb")
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
            message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
            bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
            for i, bit in enumerate(bits):
                frame_bytes[i] = (frame_bytes[i] & 254) | bit
            frame_modified = bytes(frame_bytes)
            newAudio = wave.open(self.encrypted_wav_path, 'wb')
            newAudio.setparams(audio.getparams())
            newAudio.writeframes(frame_modified)

            newAudio.close()
            audio.close()
            print(f"Successfully encoded: {self.encrypted_wav_path}")
            return True
        except:
            return False

    def decode(self, filepath:str=None):
        try:
            audio = wave.open(filepath, mode='rb')
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
            extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
            string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
            decoded = string.split("###")[0]
            print("Sucessfully decoded: " + decoded)
            audio.close()
            return True
        except:
            return False	

if __name__ == "__main__":
    AC = AudiCrypt()


