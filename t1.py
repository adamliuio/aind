
import Algorithmia
from time import time
start = time()


###
### Twitter Sentiment Analytics
###



# input = {
# 	"query": "melbourne",
# 	"numTweets": "1000",
# 	"auth": {
# 		"app_key": "6o5lUQislg7NIUkN21WwmkhNh",
# 		"app_secret": "DDenY1SCqcdlwI9KmPyPHcdVG5ZO16x15G85ws2qeaj1JDYclK",
# 		"oauth_token": "1884018308-5BvH7yNH9zwSFyUWT9IjmRw6j8v3p4rYtJ1KZVs",
# 		"oauth_token_secret": "YUIwEalFD3ff6NDBqj12WZvBIzbB7SCrT2okR0k1xPvIh"
# 	}
# }
# client = Algorithmia.client('simVc04MrGvYvthdP7EphVjBPhx1')
# algo = client.algo('nlp/AnalyzeTweets/0.1.10')
# print(algo.pipe(input))



# https://scontent-syd2-1.cdninstagram.com/vp/60f7954cd07dc826efd9cc1f3884e14c/5AE55043/t51.2885-15/e35/26276616_174229330014038_3190693412781162496_n.jpg
# https://scontent-syd2-1.cdninstagram.com/vp/00d9a9d200439007c56b5be367c7e542/5AF308D0/t51.2885-15/e35/26153101_1664889826864811_5174472230515507200_n.jpg
# https://scontent-syd2-1.cdninstagram.com/vp/c350fe32b2dd720d1f192adca03b056c/5AF8E6D7/t51.2885-15/e35/26865061_322193374934262_8189734117793857536_n.jpg
# https://scontent-syd2-1.cdninstagram.com/vp/db0675112c072a8b915cc80a92069a28/5AE4747F/t51.2885-15/e35/26181309_1412332835544342_715126112211959808_n.jpg








###
### Image black-white to colorful
###

# local_file_loc = "/Users/hongru.liu/Downloads/tmp/dog_r.png"

# # client = Algorithmia.client('simVc04MrGvYvthdP7EphVjBPhx1')
# # if client.file(local_file_loc).exists() is False:
# # 	client.file(local_file_loc).putFile("data://adamleo/test/dog_r.png")
# # else:
# # 	print("file exists.")

# input = {
#   "image": ["https://scontent-syd2-1.cdninstagram.com/vp/60f7954cd07dc826efd9cc1f3884e14c/5AE55043/t51.2885-15/e35/26276616_174229330014038_3190693412781162496_n.jpg",
#   			"https://scontent-syd2-1.cdninstagram.com/vp/00d9a9d200439007c56b5be367c7e542/5AF308D0/t51.2885-15/e35/26153101_1664889826864811_5174472230515507200_n.jpg",
#   			"https://scontent-syd2-1.cdninstagram.com/vp/c350fe32b2dd720d1f192adca03b056c/5AF8E6D7/t51.2885-15/e35/26865061_322193374934262_8189734117793857536_n.jpg",
#   			"https://scontent-syd2-1.cdninstagram.com/vp/db0675112c072a8b915cc80a92069a28/5AE4747F/t51.2885-15/e35/26181309_1412332835544342_715126112211959808_n.jpg"
#   		]
# }


# # "data://adamleo/test/26073231_1789591588001704_3864305543636058112_n.jpg"
# # https://scontent-syd2-1.cdninstagram.com/vp/5f0eb6889a1d535684307e7bd6dbaa1f/5AFF94CB/t51.2885-15/e35/26863436_2071972822817304_45481530411188224_n.jpg

# client = Algorithmia.client('simVc04MrGvYvthdP7EphVjBPhx1')
# algo = client.algo('deeplearning/ColorfulImageColorization/1.1.7')
# print(algo.pipe(input))








###
### Summarizer
###

# # input = "A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another without going through a financial institution. Digital signatures provide part of the solution, but the main benefits are lost if a trusted third party is still required to prevent double-spending. We propose a solution to the double-spending problem using a peer-to-peer network. The network timestamps transactions by hashing them into an ongoing chain of hash-based proof-of-work, forming a record that cannot be changed without redoing the proof-of-work. The longest chain not only serves as proof of the sequence of events witnessed, but proof that it came from the largest pool of CPU power. As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the longest chain and outpace attackers. The network itself requires minimal structure. Messages are broadcast on a best effort basis, and nodes can leave and rejoin the network at will, accepting the longest proof-of-work chain as proof of what happened while they were gone."
# client = Algorithmia.client('simVc04MrGvYvthdP7EphVjBPhx1')
# algo = client.algo('nlp/Summarizer/0.1.6')
# print(algo.pipe(input))







###
### DeepFilter: Apply artistic and stylish filters to your images
###



input = {
  "images": [
  		"https://scontent-syd2-1.cdninstagram.com/vp/60f7954cd07dc826efd9cc1f3884e14c/5AE55043/t51.2885-15/e35/26276616_174229330014038_3190693412781162496_n.jpg",
		"https://scontent-syd2-1.cdninstagram.com/vp/00d9a9d200439007c56b5be367c7e542/5AF308D0/t51.2885-15/e35/26153101_1664889826864811_5174472230515507200_n.jpg",
		"https://scontent-syd2-1.cdninstagram.com/vp/c350fe32b2dd720d1f192adca03b056c/5AF8E6D7/t51.2885-15/e35/26865061_322193374934262_8189734117793857536_n.jpg",
		"https://scontent-syd2-1.cdninstagram.com/vp/db0675112c072a8b915cc80a92069a28/5AE4747F/t51.2885-15/e35/26181309_1412332835544342_715126112211959808_n.jpg"
	],
  "savePaths": [
    "data://adamleo/test/1.jpg"
    "data://adamleo/test/2.jpg"
    "data://adamleo/test/3.jpg"
    "data://adamleo/test/4.jpg"
  ],
  "filterName": "hot_spicy"
}
client = Algorithmia.client('simVc04MrGvYvthdP7EphVjBPhx1')
algo = client.algo('deeplearning/DeepFilter/0.6.0')
print(algo.pipe(input))














print("time spent:", time()-start)

