from pydub import AudioSegment
from pydub.silence import split_on_silence


def split(filepath, save_path, time_length):
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound,
                              min_silence_len=500,
                              silence_thresh=dBFS-16,
                              keep_silence=250   # optional
                              )
    # setting minimum length of each chunk to x seconds
    target_length = time_length * 1000
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            # if the last output chunk is longer than the target length,
            # we can start a new one
            output_chunks.append(chunk)
    
    # Attention!
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.mkdir(save_path)
    
    for i, chunk in enumerate(output_chunks):
        chunk.export(os.path.join(
            save_path, "{0}.wav".format(i)), format="wav")
    return len(output_chunks)
