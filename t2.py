
import Algorithmia
from time import time
start = time()


###
### Twitter Sentiment Analytics
###



input = {
	"query": "ufc",
	"numTweets": "1000",
	"auth": {
		"app_key": "6o5lUQislg7NIUkN21WwmkhNh",
		"app_secret": "DDenY1SCqcdlwI9KmPyPHcdVG5ZO16x15G85ws2qeaj1JDYclK",
		"oauth_token": "1884018308-5BvH7yNH9zwSFyUWT9IjmRw6j8v3p4rYtJ1KZVs",
		"oauth_token_secret": "YUIwEalFD3ff6NDBqj12WZvBIzbB7SCrT2okR0k1xPvIh"
	}
}
client = Algorithmia.client('simVc04MrGvYvthdP7EphVjBPhx1')
algo = client.algo('nlp/AnalyzeTweets/0.1.10')
print(algo.pipe(input))



# https://scontent-syd2-1.cdninstagram.com/vp/60f7954cd07dc826efd9cc1f3884e14c/5AE55043/t51.2885-15/e35/26276616_174229330014038_3190693412781162496_n.jpg
# https://scontent-syd2-1.cdninstagram.com/vp/00d9a9d200439007c56b5be367c7e542/5AF308D0/t51.2885-15/e35/26153101_1664889826864811_5174472230515507200_n.jpg
# https://scontent-syd2-1.cdninstagram.com/vp/c350fe32b2dd720d1f192adca03b056c/5AF8E6D7/t51.2885-15/e35/26865061_322193374934262_8189734117793857536_n.jpg
# https://scontent-syd2-1.cdninstagram.com/vp/db0675112c072a8b915cc80a92069a28/5AE4747F/t51.2885-15/e35/26181309_1412332835544342_715126112211959808_n.jpg



print(time()-start)