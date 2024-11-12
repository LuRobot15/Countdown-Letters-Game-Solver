from django.db import models

from collections import Counter
from datetime import date
import random

import LettersGame
import LettersGame.CountdownSolver
import LettersGame.CreateDict

# Create your models here.
class Letters(models.Model):
	"""
	A class for the letters for each game.
	There should be one object per day.

	Attributes:
		letters (models.CharField): The letters for the game as a string.
		date_used (models.DateField): The date this model was the letters.

	Methods:
		get_answers(): Returns a list of all the Answers objects related to this Letters object.
		get_answer_words(): Returns a list of all the words objects that are answers to this letters object.
		get_max_answer_length(): Returns the length of the longest word for this Letters object.
		get_most_guessed_answer(): Returns the answer with the most guesses for this Letters object.
		get_best_answer(): Returns the answer with the longest word for this Letters object.
	"""	
	letters = models.CharField(max_length=9)
	date_used = models.DateField(auto_now_add=True, unique=True)

	def __str__(self) -> str:
		"""
		Returns the string representation of the Letters object.

		Returns:
			str: The string representation of the Letters object showing the letters and the date this object was used.
		"""
		return self.letters  + " - " + str(self.date_used)

	def get_answers(self) -> list:
		"""
		gets all the answer objects related to this Letters object.

		Returns:
			list: A list of all the Answers objects related to this Letters object.
		"""
		return Answers.objects.filter(letters=self)

	def get_answer_words(self) -> list:
		"""
		gets all the words objects that are related to answers related to this Letters object.

		Returns:
			list: A list of all the words objects that are answers to this letters object.
		"""
		answers = Answers.objects.filter(letters=self)
		answer_words = [answer.word for answer in answers]
		return answer_words

	def get_max_answer_length(self) -> int:
		"""
		gets the length of the longest word that is an answer to this Letters object.

		Returns:
			int: _description_the length of the longest word that is an answer to this Letters object.
		"""
		return max([answer.answer.get_word_length() for answer in self.get_answers()])

	def get_most_guessed_answer(self):
		"""
		gets the answer object that has been guessed the most times for this Letters object.

		Returns:
			Answers: The object for the most guessed object for this Letters object.
		"""
		return max(self.get_answers(), key=lambda answer: answer.get_times_guessed())

	def get_best_answer(self):
		"""
		gets the answer object with the longest word for this Letters object.

		Returns:
			Answers: the answer object with the longest word for this Letters object.
		"""
		answers = self.get_answers()
		answers.sort(key=lambda answer: answer.get_word_length())
		return answers[-1]

	@staticmethod
	def create_random_letters():
		"""
		Creates a random set of letters for a game. Ensuring that there are betwen 1 and 4 vowls and the rest are consonants.

		Returns:
			Letters: A Letters object with a random set of letters.
		"""
		vowls = 'aeiou'
		consonants = 'bcdfghjklmnpqrstvwxyz'

		num_vowls_to_use = random.randint(1, 4)
		num_consonants_to_use = 9 - num_vowls_to_use
  
		vowls = ''.join(random.choices(vowls, k=num_vowls_to_use))
		consonants = ''.join(random.choices(consonants, k=num_consonants_to_use))
		letters = ''.join(random.sample(vowls + consonants, 9))

		l = Letters.objects.create(letters=letters, date_used=date.today())
		l.save()
		Answers.create_answers_for_letters(l)
		return l

    
	@staticmethod
	#Todo: handle the exception by creating a new Letters object
	def get_todays_letters():
		"""
		gets the Letters object for today's date.

		Returns:
			Letters: The Letters object for today's date.
		Throws:
			Letters.DoesNotExist: If there is no Letters object for today's date.
		"""
		try:
			l = Letters.objects.get(date_used=date.today())
		except Letters.DoesNotExist:
			return Letters.create_random_letters()


class Words(models.Model):
	"""
	A class for the words that are answers to the game.

	Attributes:
		word (models.CharField): The word that is an answer to at least one game.
		definition (models.CharField): The definition of the word.

	Methods:
		get_word_length(): Returns the length of the word.
		get_times_guessed(): Returns the total number of times this word has been guessed in all letters games.
		get_letter_counter(): Returns a Counter object of the letters in the word.
		get_questions(): Returns a list of all the questions related to this word.
	"""
	word = models.CharField(max_length=9)
	definition = models.CharField(max_length=100)

	def __str__(self) -> str:
		"""
		Returns the string representation of the Words object.

		Returns:
			str: The string representation of the Words object showing the word and the definition.
		"""
		return self.word + " - " + self.definition

	def get_word_length(self) -> int:
		"""
		gets the length of the word.

		Returns:
			int: the length of the word.
		"""
		return len(self.word)

	def get_times_guessed(self) -> int:
		"""
		gets the total number of times this word has been guessed in all games.

		Returns:
			int: the number of times this word has been guessed in all games.
		"""
		return Answers.objects.filter(answer=self).aggregate(models.Sum('times_guessed'))['times_guessed__sum']

	def get_letter_counter(self) -> Counter:
		"""
		gets a Counter object of the letters in the word.

		Returns:
			Counter: A Counter object of the letters in the word.
		"""
		return Counter(self.word)

	def get_questions(self) -> list:
		"""
		gets a list of all the questions this word is an answer for.

		Returns:
			list: a list of all the questions related to this word.
		"""
		questions = []
		for answer in self.answer_set.all():
			questions.append(answer.letters)
		return questions


class Answers(models.Model):
	"""
	A composite class for the many-to-many relationship between Letters and Words.
 
	Attributes:
		letters (models.ForeignKey): The Letters object this answer is related to.
		answer (models.ForeignKey): The Words object that is the answer.
		times_guessed (models.IntegerField): The number of times this answer has been guessed for this letters game.
  
	Methods:
		increment_times_guessed(): Increments the times_guessed attribute by 1.
	"""
	letters = models.ForeignKey(Letters, on_delete=models.CASCADE)
	answer = models.ForeignKey(Words, on_delete=models.CASCADE)
	times_guessed = models.IntegerField(default=0)
 
	def __str__(self) -> str:
		"""
		Returns the string representation of the Answers object.

		Returns:
			str: The string representation of the Answers object showing the letters, the answer, and the number of times guessed.
		"""
		return \
			self.letters.letters + " - " +  self.answer.word + \
      		"\tTimes guessed: " + str(self.times_guessed)
        
	def increment_times_guessed(self) -> None:
		"""
  		Increments the times_guessed attribute by 1.
		"""
		self.times_guessed += 1
		self.save()
  
	@staticmethod
	def create_answers_for_letters(letters: Letters) -> None:
		"""
		Creates the answer objects for the provided Letters object.

		Args:
			letters (Letters): The Letters object to create answers for.
		"""
		try:
			letters_dict = LettersGame.CreateDict.load_dict("dict.json")
		except FileNotFoundError:
			letters_dict = LettersGame.CreateDict.create_dict("OPTED-Dictionary.csv", "dict.json")
   
		answer_words = LettersGame.CountdownSolver.solve_countdown(letters.letters, letters_dict)
		for word in answer_words:
			w = Words.objects.get_or_create(word=word["word"], definition=word["definition"])[0]
			a = Answers.objects.get_or_create(letters=letters, answer=w)
			w.save()
			a.save()