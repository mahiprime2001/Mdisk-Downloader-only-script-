try:

	import requests
	import os 
	import subprocess
except:
    print("some modules are not available so trying to install...")
    iswin = os.environ.get("WIN", "0")
    if iswin == 0:
        os.system("pip3 install requests")
    else:
    	os.system("pip install requests")

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
ytdlp = dirPath + "/binaries/yt-dlp.exe"
aria2c = dirPath + "/binaries/aria2c.exe"
mkvmerge = dirPath + "/binaries/mkvmerge.exe"



while True:

	browser_url = input("enter the url: ")
	


	fxl = browser_url.split("/")
	cid = fxl[-1]

	URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'

	header = {
					'Accept': '*/*',
					'Accept-Language': 'en-US,en;q=0.5',
					'Accept-Encoding': 'gzip, deflate, br',
					'Referer': 'https://mdisk.me/',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
			}

	resp = requests.get(url=URL, headers=header).json()['source']
	print(resp)
	output = requests.get(url=URL, headers=header).json()['filename']
	bad_chars = [';', ':', '!', "*", "?", "|", "@"] 
	for i in bad_chars:
			output = output.replace(i, '')
	input_video = dirPath + output+'_vid.mp4'
	input_audio = dirPath + output+'_aud.m4a'


	subprocess.run([ytdlp, '--no-warning', '-k', '--user-agent',
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', '--allow-unplayable-formats', '-F', resp])

	vid_format = input('\nEnter Video Format ID: ')
	aud_format = input('\nEnter Audio Format ID: ')

	if not os.path.exists(input_video):
		subprocess.run([ytdlp, '--no-warning', '-k', '-f', vid_format, resp, '-o', output+'_vid.mp4', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
					'--allow-unplayable-formats', '--external-downloader', aria2c, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
	else:
				pass

	if not os.path.exists(input_audio):
				subprocess.run([ytdlp, '--no-warning', '-k', '-f', aud_format, resp, '-o', output+aud_format+'_aud.m4a', '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
					'--allow-unplayable-formats', '--external-downloader', aria2c, '--external-downloader-args', '-x 16 -s 16 -k 1M'])
	else:
				pass
	for f in os.listdir():
		if f.endswith("vid.mp4"):
			video_file = f
		elif f.endswith("aud.m4a"):
			audio_file = f

	os.system("mkvmerge -o \""+output+".mp4\" -A \""+video_file+"\" \""+audio_file+"\"")
	print("Cleaning the process .....")
	for f in os.listdir():
		if f.startswith(output+".mp4"):
			os.remove(video_file)
			os.remove(audio_file)
		else:
			print("unable to complete the cleaning process....")
