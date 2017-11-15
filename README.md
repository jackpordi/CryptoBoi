# CryptoBoi Cryptocurrency exchange monitering and trading bot

We currently have:
  - A very simple wrapper that can make public-api calls to Bittrex. Hopefully I'll have time to add more exchanged in the future.
  - Very basic data type of trading pairs groups (e.g. to BTC, ETH, and USDT currently)

What I want to implement:
  - Object representing an asset
  - Object representing a market trading (as opposed to keeping it in JSON, as this will allow us to modify fields easily if we want, and storing historical data)
  - Object that encapsulates both of the above, or perhaps a combination of the two.
  - Asset objects will intelligently add the relevent trading pairs to themselves
  - Object that represents "Our Assets" i.e. currencies that we actually have, probably just going to be a basic set or list implementation.
  - An actual algorithmic design for the bot
