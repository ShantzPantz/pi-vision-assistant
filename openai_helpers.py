import base64
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

from openai import OpenAI

client = OpenAI()


personalities = {
    "dougie": """
        You're a chatbot named Douglas Adams, the narrator and creator of HHGTTG.
        Humorous: The narrator frequently employs humor, often in the form of dry wit and absurdity, to comment on the events unfolding in the story.
        Sardonic: There's a sense of cynicism and irony in the narrator's tone, especially when depicting the absurdities of the universe and human behavior.
        Observant: The narrator demonstrates keen observation skills, providing insightful commentary on various aspects of the universe, technology, and society.
        Detached: Despite being present throughout the story, the narrator maintains a certain level of detachment from the characters and events, often adopting a perspective of amused detachment.
        Informative: Alongside its humor, the narrator serves as a source of information about the universe, offering explanations of various phenomena and technologies encountered by the characters.
        Eccentric: The narrator's voice can be quirky and eccentric, mirroring the offbeat and unconventional nature of the story itself.
    """,
    "snoop": """
        Imagine you're embodying the essence of Snoop Dogg, the iconic rapper and cultural icon. 
        Your character exudes a laid-back and charismatic vibe, with a playful sense of humor. 
        You're known for your distinctive voice and love for cannabis culture. 
        Your responses should reflect a cool and relaxed demeanor, while still maintaining authenticity and charm. 
        Feel free to sprinkle in some references to music, pop culture, or anything else that captures the essence of Snoop Dogg's personality.
    """,
    "marshall": """
        You are a chatbot who always responds with a rap verse in the form of Rapper Eminem. You use clever wordplay and rhymes in your conversation.
    """
}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def text_from_audio(file_path): 
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    print("Audio Transcript:")
    print(transcription.text)

    return transcription.text


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image. Pay special attention to the people in the photo."},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


# Based on the command, determine if an image description would help with the response.
def does_command_require_camera(text):
    system_prompt = """
        Your goal is to determine if a users request sounds like they are asking you information about something visual. 

        If the user mentions how something looks, or asks about how something looks, you will respond "YES". 
        If they ask about their environment, or something that is related to their looks, you should respond "YES". 
        If the user asks for advice on what they are wearing, or their surroundings. You should reply "YES". 
        In any scenario where visual context would help with the response, or if something is asked about what something looks like, respond "YES".

        If the question does not relate to things that are visual, or likely in the users surroundings, you will respond "NO". 
        You will not respond with anything other than "YES" or "NO. 
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
        max_tokens=10
    )
    response_text = response.choices[0].message.content
    if response_text == "YES":
        return True
    else: 
        return False


def analyze_image(user, base64_image, command):
    system_prompt = personalities.get(user)
    system_prompt += "\n Pay extra attention to the details of the people in the photo and their surroundings when responding."
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
            "role": "user",
            "content": [
                {"type": "text", "text": command},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
        ],
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    return response_text


def generate_response(user, script):
    system_prompt = personalities.get(user)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
        ]
        + script,        
        max_tokens=500
    )
    response_text = response.choices[0].message.content
    return response_text


def main():   
    # Getting the base64 encoding
    base64_image = encode_image("test.png")

    output = analyze_image(base64_image, [])
    print(output)

if __name__ == "__main__":    
    main()
