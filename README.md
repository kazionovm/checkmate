# checkmate

checkmate is a neural-network chess engine written in Python.  
**Gameplay demonstration** - https://www.dailymotion.com/video/x7y1z8o

##  🛠 How it works?
* CNN as a value function to find step win probability.
* Minimax + Beam search to prune that value function.

## ♟ Training set
* We trained our nn using board data from [lichess elite database](https://database.nikonoel.fr/)
* `6.11.2020` - I had managed to serialize 305339 chess games and got 25 millions board positions

## 📎 Useful links
* [Sunfish chess engine](https://github.com/thomasahle/sunfish)
* [Deep pink chess engine](https://github.com/erikbern/deep-pink)
