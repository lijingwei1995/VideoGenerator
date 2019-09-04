# ffmpeg -y -f concat -safe 0 -i video_config.txt -i bgm/bgm01.mp3 -shortest output.mp4
# ffmpeg -i input1.mp3 -i input2.mp3 -filter_complex amerge -ac 2 -c:a libmp3lame -q:a 4 output.mp3
# ffmpeg -y -i bgm/bgm01.mp3 -i bgm/bgm01.mp3 -filter_complex amerge output.mp3
# ffmpeg -y -stream_loop 2 -i bgm/bgm01.mp3 -i output.mp4 -shortest output2.mp4

# ffmpeg -y -stream_loop 1 -i bgm/global_visions.mp3 output3.mp3
ffmpeg -y -i output3.mp3 -i output.mp4 -shortest output2.mp4

# ffmpeg -f concat -i "audio_handler.txt" -c copy a.mp3

ffmpeg -y -i bgm/Psyche.mp3 -i output.mp4 -shortest output_final.mp4