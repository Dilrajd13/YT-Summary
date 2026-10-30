# YT-Summary
## Take a Youtube video and summarize it to check if it is worth watching or not.

<!-- Add a screenshot or GIF of the app here -->

Python- User input (youtube link) from the web page or console

yt-dlp- Find video -> download audio

YouTube captions- -> if the video has captions use those as the transcript (takes a few seconds)

OpenAI Whisper Audio Transcriber (faster-whisper)- -> if there are no captions, transcribe audio -> transcript

OpenAI GPT-5 mini API- -> Summarize transcript -> Summary + verdict (Worth watching / Maybe / Skip it)

Python- User output -> delete/cleanup files

HIGH LEVEL WORKFLOW/Architecture 
<img width="1851" height="596" alt="image" src="https://github.com/user-attachments/assets/a7d2f40c-9bfe-465c-b367-89a2fb92cd14" />

### UI

The app now has a local web page so you don't have to use the console. Paste a link and it shows the video, live progress for each step, and the summary. You can also copy the summary or view the full transcript.

### How to Run

This currently needs to be run locally and requires a OpenAI API key from user

*Performance currently is based entirely on system specs*. Most videos have captions so they're done in about 30 sec. If Whisper has to transcribe, it uses your NVIDIA GPU if you have one (a 6 min video took 15 sec on an RTX 2060), otherwise the CPU (about 80 sec)

Use the .env.example file as reference to create a .env file that includes your API key

<img width="286" height="35" alt="image" src="https://github.com/user-attachments/assets/06c08f15-0f9f-4c04-92bf-230509075e48" />

**Windows:** double-click `run.bat`. The first run installs everything (ffmpeg included), then the app opens in your browser.

**Mac/Linux:** `pip install -r requirements.txt` then `python src/app.py` and open http://127.0.0.1:5000

You can still run main.py and paste in youtube link and the summary will be outputted in console.

If downloads fail with `HTTP Error 403`, update yt-dlp: `pip install -U "yt-dlp[default]"` (run.bat does this for you)

## Sample Run with this [video](https://www.youtube.com/watch?v=orQKfIXMiA8) Title-"You Need to Be Bored. Here's Why."



Run main.py and Enter Youtube Link


<img width="484" height="20" alt="image" src="https://github.com/user-attachments/assets/0aea5add-56db-44d1-857e-91f1b413e5df" />


### Outputted Summary (console version) 

Main idea (one line)
- Boredom is valuable: deliberately allowing yourself to be bored (letting the brain’s “default mode network” run) helps you confront meaning, reduces dependence on phones, and can protect against anxiety, depression, and a hollow life.

All topics covered (bullet points)
- What boredom is: lack of cognitive occupation that activates the brain’s default mode network.
- Default mode network: when it turns on, your mind wanders to existential and self-reflective questions.
- Experimental evidence / anecdote: Dan Gilbert’s study where people preferred a painful shock over sitting and doing nothing.
- Why boredom is uncomfortable: it forces you to face big, sometimes unsettling questions about meaning and purpose.
- Societal problem: modern life has reduced opportunities for boredom, contributing to rising depression and anxiety.
- Role of smartphones: constant phone use prevents boredom and constantly distracts the default mode network.
- The “doom loop” of meaning: repeatedly avoiding boredom (via screens) makes it harder to find meaning over time.
- Practical prescriptions / habits:
  - Don’t bring your phone to the gym; allow device-free workouts.
  - Commute without audio or screens.
  - No devices during meals.
  - No phones in bed / don’t sleep with your phone.
  - Regular social-media and screen “cleanses.”
  - Limit notifications/emergency-only settings if needed.
- Personal accountability: the speaker follows these practices himself but admits occasional relapse; he emphasizes moderation and realistic implementation.
- Reassurance about missing out: most online/real-time updates are not emergencies and can wait.

Quick actionable takeaways
- Practice 15+ minute stretches of boredom daily (commute, workout, waiting).
- Implement phone curfews (e.g., no devices after 7 pm; no phones at dinner; sleep without phone).
- Do periodic social-media fasts and restrict nonessential notifications.

Reasons to help decide if it’s worth watching
- Good reasons to watch:
  - You want practical, easy-to-apply advice to reduce screen dependence.
  - You’re curious about why boredom matters psychologically and how it ties to meaning and mental health.
  - You like short, persuasive talks with memorable examples and behavioral tips.
  - You’re a parent, commuter, student, or knowledge worker seeking simple lifestyle changes.
- Reasons you might skip or deprioritize it:
  - You want a deep, technical neuroscientific or peer-reviewed review (the talk is high-level and anecdotal, not a detailed research lecture).
  - You already practice device-free habits and find the message repetitive.
  - You dislike prescriptive or slightly moralizing tones about technology use.

Recommendation
- Watch it if you’re looking for motivation and practical steps to cut back on screen time, reconnect with your thoughts, and explore meaning. Skip or supplement it with scientific literature if you need rigorous empirical detail or treatment-level advice for severe phone addiction or clinical depression.


