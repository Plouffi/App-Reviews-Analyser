from typing import List, Tuple
import numpy as np
import Image.make_image as make_image
import re


class Cloud:
	"""
		Class to generate word clouds
		...
		Attributes
		----------
		counts : np.ndarray
			Store the occurrences for each word.
		alpha : float
			Smoothing parameter, usefull to remove noise from data. (remove very uncommon words)
		words : np.ndarray
			The number of words in the words cloud
		voc: Dict
			All words found in reviews. Key: the word, Value: an index (0, 1, 2, ...)
	"""
	counts: np.ndarray

	def __init__(self, alpha=1, words=50):
		self.voc = {}
		self.alpha = alpha
		self.words = words
		self.reg_token = re.compile(r"(?u)\b\w+\b")

	def tokenize(self, content: str) -> List[str]:
		"""
			Method to tokenize the review's content. Find all words and return them as a list of lowered string.
			Return
			----------
				List[str]
		"""
		return self.reg_token.findall(content.lower())

	def load_reviews(self, *data_reviews):
		"""
			Method to fill vocabulary and occurences and counts.
			Parameter
			----------
				*data_reviews
				2 set of data reviews (1 for reviews before FEH pass, 1 after)
		"""
		# Start by tokenized review's content and build vocabulary
		tk_data_reviews = []
		for reviews in data_reviews:
			tk_reviews = []
			for review in reviews:
				tokenized_review = self.tokenize(review["content"] if isinstance(review["content"], str) else '')
				for token in tokenized_review:
					if token not in self.voc:
						self.voc[token] = len(self.voc)
				tk_reviews.append(tokenized_review)
			tk_data_reviews.append(tk_reviews)

		# Initiliaze shape depending on vocabulary length, fill value alpha.
		self.counts = np.full(shape=(len(self.voc), len(data_reviews)), fill_value=self.alpha)

		# Counting occurrences
		for i, tk_reviews in enumerate(tk_data_reviews):
			for tk_review in tk_reviews:
				for token in tk_review:
					self.counts[self.voc[token], i] += 1.

		# Normalize counts matrix. It's very important to do this. It allows very commons words such as "you" to not be
		# classified as "a pertinent word" because such word are commom in reviews before and after FEH pass
		vector_words = np.sum(self.counts, 1)
		self.counts = self.counts/vector_words[:, None]

	def word_cloud(self, index: int) -> List[Tuple[str, float]]:
		"""
			Method to return the 50 words of each set of reviews.
			Parameter
			----------
			index : int
				the index of the set of review (0--> before, 1-->after)
		"""
		counts = self.counts[:, index]
		# it works, don't ask what kind of black magic is it
		return [
			(list(self.voc.keys())[i], counts[i])
			for i in np.argpartition(counts, -self.words)[-self.words:]
		]

	def cloud(self):
		image = make_image.simple_image(self.word_cloud(0))
		image.save(fp=f"./ressources/before_fehp_word_cloud.png", format="PNG")

		image = make_image.simple_image(self.word_cloud(1))
		image.save(fp=f"./ressources/after_fehp_word_cloud.png", format="PNG")
