from gatepoint import GatewayClient, Interaction, Choice, AutoComplete
from typing import Optional

gateway = GatewayClient(
    api_version = 11,
    secret_key = "SECRET",
    public_key = "PUBLIC",
    token =  "TOKEN"
)

@gateway.register(
    CommandInteraction(
        name = "test",
        description = "Test command",
        options = [
            Option(
                type = OptionType.STRING,
                name = "name",
                description = "Name",
                required = True
            ),
            Option(
                type = OptionType.STRING,
                name = "name2",
                description = "Name2",
                required = False
            )
        ]
    )
)
async def test_command(
    interaction: Interaction,
    name: Optional[Choice],
    name2: AutoComplete("name")
):
    interaction.reply("Hello World!", ephemeral = True)

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