from typing import List, Tuple
import numpy as np
import re
from re import Pattern


class CloudService:
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
	reg_token: Pattern

	def __init__(self):
		self.voc = {}
		self.reg_token = re.compile(r"(?u)\b\w+\b")

	def load_reviews(self, alpha: int = 1, n: int = 2, *data_reviews):
		"""
			Method to fill vocabulary and occurences and counts.
			Parameter
			----------
				alpha
				Noise reducer
				n
				Number of words per token vocabulary
				*data_reviews
				2 set of data reviews (1 for reviews before FEH pass, 1 after)
		"""
		# Start by tokenizing review's content and build vocabulary
		tk_data_reviews = []
		for reviews in data_reviews:
			tk_reviews = []
			for review in reviews:
				tokenized_review = self.n_grams(
					self.tokenize(review["content"] if isinstance(review["content"], str) else ''),
					n
				)
				for token in tokenized_review:
					if token not in self.voc:
						self.voc[token] = len(self.voc)
				tk_reviews.append(tokenized_review)
			tk_data_reviews.append(tk_reviews)

		# Initiliaze shape depending on vocabulary length, fill value alpha.
		self.counts = np.full(shape=(len(self.voc), len(data_reviews)), fill_value=alpha)

		# Counting occurrences
		for i, tk_reviews in enumerate(tk_data_reviews):
			for tk_review in tk_reviews:
				for token in tk_review:
					self.counts[self.voc[token], i] += 1.

		# Normalize counts matrix. It's very important to do this. It allows very commons words such as "you" to not be
		# classified as "a pertinent word" because such word are commom in reviews before and after FEH pass
		vector_words = np.sum(self.counts, 1)
		self.counts = self.counts/vector_words[:, None]

	def n_grams(self, tokens, n):
		if n == 1:
			return tokens
		if len(tokens) <= n:
			return [' '.join(tokens)]
		return [' '.join(tokens[i:i + n]) for i in range(len(tokens) - n)]

	def tokenize(self, content: str) -> List[str]:
		"""
			Method to tokenize the review's content. Find all words and return them as a list of lowered string.
			Return
			----------
				List[str]
		"""
		return self.reg_token.findall(content.lower())

	def word_cloud(self, index: int, words: int = 50) -> List[Tuple[str, float]]:
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
			for i in np.argpartition(counts, -words)[-words:]
		]
	
	def get_words(self) -> List[List[Tuple[str, float]]]:
		return [self.word_cloud(0), self.word_cloud(1)]