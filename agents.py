from autogen import AssistantAgent, Agent, UserProxyAgent, AutoGenGroupChat
from image_generators import generate_image_stable_diffusion, generate_image_dalle

class StableDiffusionAgent(Agent):
    def __init__(self, name, api_key, **kwargs):
        super().__init__(name, **kwargs)
        self.api_key = api_key

    async def generate_image(self, text_prompt):
        image = generate_image_stable_diffusion(text_prompt)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str 

class DalleAgent(Agent):
    def __init__(self, name, api_key, **kwargs):
        super().__init__(name, **kwargs)
        self.api_key = api_key

    async def generate_image(self, text_prompt):
        image = generate_image_dalle(text_prompt) 
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

class ImageGeneratorManager(AssistantAgent):
    def __init__(self, name, stable_diffusion_agent, dalle_agent, **kwargs):
        super().__init__(name, **kwargs)
        self.stable_diffusion_agent = stable_diffusion_agent
        self.dalle_agent = dalle_agent

    async def handle_message(self, message):
        if message.get("role") == "user":
            text_prompt = message.get("content")
        
        if "photorealistic" in text_prompt.lower():
                image = await self.dalle_agent.generate_image(text_prompt)
        else:
                image = await self.stable_diffusion_agent.generate_image(text_prompt)

        await message.send(content=image)
