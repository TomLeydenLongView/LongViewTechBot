import os
import openai
from microsoft.bot.builder import TeamsActivityHandler, TurnContext, BotFrameworkAdapter
from microsoft.bot.schema import Activity, ActivityTypes

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define a function to generate a response using ChatGPT
def generate_response(query):
    prompt = f"Query: {query}\nResponse:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Define a TeamsActivityHandler to handle incoming messages
class TeamsBot(TeamsActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            # Get the text of the incoming message
            message_text = turn_context.activity.text

            # Generate a response using ChatGPT
            response_text = generate_response(message_text)

            # Send the response back to the Teams channel
            reply_activity = Activity(
                type=ActivityTypes.message,
                text=response_text,
                conversation=turn_context.activity.conversation,
                recipient=turn_context.activity.from_property,
                from_property=turn_context.activity.recipient,
            )
            await turn_context.send_activity(reply_activity)

# Set up the Bot Framework Adapter
adapter = BotFrameworkAdapter(
    os.environ.get("MICROSOFT_APP_ID"),
    os.environ.get("MICROSOFT_APP_PASSWORD"),
)

# Create the TeamsBot instance and add it to the adapter
bot = TeamsBot()
adapter.on_turn_error = bot.on_error

# Define a function to start the bot
async def start_bot():
    await adapter.start_async()

# Define a function to stop the bot
async def stop_bot():
    await adapter.stop_async()

# Start the bot
asyncio.run(start_bot())
