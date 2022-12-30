GatePoint
==========

.. image:: https://discord.com/api/guilds/886543799843688498/embed.png
    :target: https://discord.gg/5YY3W83YWg
    :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/gatepoint.svg
    :target: https://pypi.python.org/pypi/gatepoint
    :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/gatepoint.svg
    :target: https://pypi.python.org/pypi/gatepoint
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
    python3 -m pip install -U gatepoint

    # Windows
    py -3 -m pip install -U gatepoint

To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/Senarc-Studios/gatepoint
    $ cd gatepoint
    $ python3 -m pip install -U .

Quick Example
--------------

.. code:: py

    import gatepoint

    InteractionAPI = gatepoint.GatewayClient(
        api_version = 11,
        secret_key = "SECRET",
        public_key = "PUBLIC",
        token =  "TOKEN"
    )

    @InteractionAPI.command(name = "ping", description = "Pong!")
    async def ping(interaction):
        await interaction.reply('pong!')

    InteractionAPI.run()

You can find more examples in the examples directory.

Links
------

- `Documentation <https://gatepoint.readthedocs.io/en/latest/index.html>`_
- `Official Discord Server <https://discord.gg/5YY3W83YWg>`_
- `Discord API <https://discord.gg/discord-api>`_
