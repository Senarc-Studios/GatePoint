from api_gateway import Discord, Interaction, Choice, AutoComplete
from typing import Optional

gateway = Discord.GatewayClient(
    api_version = 11,
    secret_key = "SECRET",
    public_key = "PUBLIC",
    token =  "TOKEN"
)

@
async def test_command(
    interaction: Interaction,
    choice: Optional[Choice],
    autocomplete: AutoComplete("name")
):
    await interaction.reply("Hello World!", ephemeral = True)

@gateway.autocomplete("name")
async def test_autocomplete(interaction: Interaction):
    return [
        Choice("Name", "value"),
        Choice("Name2", "value2")
    ]

@gateway.button("custom_id")
async def test_button(interaction: Interaction):
    await interaction.respond(
        {
            "type": 4,
            "data": {
                "content": "Hello World!",
                "flags": 64
            }
        }
    )

@gateway.event("interaction_receive")
async def interaction_receive(interaction: Interaction):
    print(interaction)

gateway.run()