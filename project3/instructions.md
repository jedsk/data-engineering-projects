## Whisper API and NLP Analysis Project

### Prerequisites
- Python environment with necessary libraries installed.
- Audio file for transcription.

#### Setup Instructions:
1. **Install Whisper**:
   - Run `pip install openai-whisper` to install OpenAI's Whisper API.

2. **Install OpenAI's Python Client**:
   - Use `pip install openai` to install the OpenAI Python client for making API requests.

### Transcription and NLP Analysis

1. **Transcription with Whisper API**:
   - Load and use Whisper API to transcribe an audio file.
   - **Sample Code**:
     ```python
     import whisper

     model = whisper.load_model("tiny.en") # Choose from: base.en, small.en, medium.en
     result = model.transcribe("path_to_your_audio_file.mp3")
     print(result["text"])
     ```

2. **NLP Analysis using OpenAI**:
   - Send the transcript to OpenAI for analysis.
   - **Sample Code**:
     ```python
     import pandas as pd
     import logging
     from openai import OpenAI

     client = OpenAI()

     transcript = """[Your Transcribed Text Here]"""

     prompt = (
         "Analyze the following call transcript and extract key details. "
         "Provide concise responses suitable for each. [Details of the Prompt]"
             "Transcript: {}\n\n"
            "Details to extract:\n"
            "- Caller Name\n"
            "- Phone Number\n"
            "- Call Type\n"
            "- Service Type\n"
            "- Call Reason\n"
            "- Urgency Level\n"
            "- Tasks Extracted\n"
            "- Customer Sentiment\n"
            "- Agent Sentiment\n"
            "- Resolution Status\n"
            "- Follow up Required\n"
            "- Agent Name\n"
            "- Agent Efficiency\n"
            "- Response Time\n"
            "- Feedback Offered\n"
            "- Upselling Attempt\n"
            "- Repeat Call\n"
            "- Data Privacy Adherence\n"
     ).format(transcript)

     response = client.chat.completions.create(
         messages=[
             {
                 "role": "user",
                 "content": prompt
             }
         ],
         model="gpt-4-1106-preview"  # or any other appropriate model
     )

     response_content = response.choices[0].message.content

     print(response_content)
     ```

3. **Data Processing and Export to CSV**:
   - Process the response and export the details to a CSV file.
   - **Sample Code**:
     ```python
     details = [line.split(": ")[1] if ": " in line else None for line in response_content.split("\n") if "- " in line]

     expected_columns = [
         "Caller Name", "Phone Number", "Call Type", "Service Type", "Call Reason", 
         "Urgency Level", "Tasks Extracted", "Customer Sentiment", 
         "Agent Sentiment", "Resolution Status", "Follow up Required", "Agent Name", 
         "Agent Efficiency", "Response Time", "Feedback Offered", "Upselling Attempt", 
         "Repeat Call", "Data Privacy Adherence"
     ]

     if len(details) == len(expected_columns):
         df = pd.DataFrame([details], columns=expected_columns)
         csv_filename = "call_transcript_details.csv"
         df.to_csv(csv_filename, index=False)
         print(f"Saved data to {csv_filename}")
     else:
         logging.error("Mismatch between extracted details and expected columns.")
         df = pd.DataFrame()
     ```

### Usage

- Replace the audio file path and transcript in the code with your data.
- Run the script to perform transcription and analysis.
