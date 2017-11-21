# CryptoBoi Cryptocurrency exchange monitering and trading bot

We currently have:
  - A very simple wrapper that can make public-api calls to Bittrex. Hopefully I'll have time to add more exchanged in the future.
  - Very basic data type of trading pairs groups (e.g. to BTC, ETH, and USDT currently)
  - Object representing an asset
- Object representing a market trading (as opposed to keeping it in JSON, as this will allow us to modify fields easily if we want, and storing historical data). Currently the only use for this object is merely to log data to a log file.

What I want to implement:
  - Object that represents "Our Assets" i.e. currencies that we actually have, probably just going to be a basic set or list implementation. Need to figure out how to securely use private API keys first.
  - Being able to put the data into a SQL format.
  - An actual algorithmic design for the bot
