import streamlit as st
import asyncio
from agents import ImageGeneratorManager, StableDiffusionAgent, DalleAgent
from image_generators import generate_image_stable_diffusion, generate_image_dalle
from autogen import AssistantAgent, Agent, UserProxyAgent, AutoGenGroupChat
import base64
from PIL import Image
#api keys
STABILITY_API_KEY = st.secret["sk-proj-NYqQDPeNbR2xNdTfffPIT3BlbkFJrXWGXIGfGKDyVgit9mO"]
OPENAI_API_KEY = st.secret["sk-1A0hNsB9lKDLdGL4l22ZIAiVwt5PCaD6doXkTvidceudrI"]

async def run_image_generation(prompt: str):
    stable_diffusion_agent = StableDiffusionAgent(name="sd_agent",
        api_key=STABILITY_API_KEY)
    dalle_agent = DalleAgent(name="dalle_agent",
        api_key=OPENAI_API_KEY)
    manager_agent = ImageGeneratorManager(name="manager",
        stable_diffusion_agent=stable_diffusion_agent,
        dalle_agent=dalle_agent)
    
    chat = AutoGenGroupChat(agents=[manager_agent,stable_diffusion_agent,
                dalle_agent],messages=[],temperature=0.5)
    chat.register_agent(UserProxyAgent("user"))

    response = await chat.initiate_chat(prompt,agent_name="user")
    return response

st.title("Autogen Image generator")

prompt = st.text_input("Describe the image:")

if st.button("generate"):
    with st.spinner("creating image ..."):
        response = asyncio.run(run_image_generation(prompt))

        if response:
            image_data = response['content']
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            st.image(image)
        else:
            st.error("Image generation failed")
