import wave
import io

def write_audio_file(audio_buffer: str, sample_rate: int) -> str:
    """
        Takes a byte array string and converts it to a *.wav byte array string. 

        :audio_buffer: byte array string to convert
        :sample_rate: the sample rate of the conversion

        :returns: converted *.wav file as a byte array string 
    """ 
    output = io.BytesIO()

    with wave.open(output, 'wb') as wf: 
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_buffer)

    return output.getvalue()