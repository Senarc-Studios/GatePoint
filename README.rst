discord.py
==========

.. image:: https://discord.com/api/guilds/886543799843688498/embed.png
    :target: https://discord.gg/5YY3W83YWg
    :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/api-gateway.svg
    :target: https://pypi.python.org/pypi/api-gateway
    :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/api-gateway.svg
    :target: https://pypi.python.org/pypi/api-gateway
    :alt: PyPI supported Python versions

An API Client for Discord Interactions written in Python.

Key Features
-------------

- Modern Python API using ``FastAPI`` for Discord.
- Optimised to work in serverless environments.
- API Client over Real-time connection.

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U api-gateway

    # Windows
    py -3 -m pip install -U api-gateway

To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/Senarc-Studios/api-gateway
    $ cd api-gateway
    $ python3 -m pip install -U .

Quick Example
--------------

.. code:: py

    import api_gateway
    from api_gateway import CommandInteraction

    Client = api_gateway.GatewayClient(
        api_version = 11,
        secret_key = "SECRET",
        public_key = "PUBLIC",
        token =  "TOKEN"
    )

    @Client.register(
        CommandInteraction(
            name = "ping",
            description = "Pong!"
        )
    )
    async def ping(interaction):
        await interaction.reply('pong!')

    Client.run()

You can find more examples in the examples directory.

Links
------

- `Documentation <https://api-gateway.readthedocs.io/en/latest/index.html>`_
- `Official Discord Server <https://discord.gg/5YY3W83YWg>`_
- `Discord API <https://discord.gg/discord-api>`_