import nltk
import itertools 
import enchant
import csv
import EFZP as zp


class FeatureAnalysis:
	#a class that contains the functions to create a feature vector from a message (which is done on instantiation)
	def __init__(self,message):
		self.writing_print = self.get_features(message)

	def yule(self,words):
		#from the blog post: http://swizec.com/blog/measuring-vocabulary-richness-with-python/swizec/2528
	    # yule's I measure (the inverse of yule's K measure)
	    # higher number is higher diversity - richer vocabulary
	    d = {}
	    stemmer = nltk.stem.porter.PorterStemmer()
	    for w in words:
	        w = stemmer.stem(w).lower()
	        try:
	            d[w] += 1
	        except KeyError:
	            d[w] = 1
	 
	    M1 = float(len(d))
	    M2 = sum([len(list(g))*(freq**2) for freq,g in itertools.groupby(sorted(d.values()))])
	 
	    try:
	        return (M1*M1)/(M2-M1)
	    except ZeroDivisionError:
	        return 0

	def analyse_email_zones(self,message):
		sig_opening_statements = [
	                          "warm regards",
	                          "kind regards",
	                          "regards",
	                          "cheers",
	                          "many thanks",
	                          "thanks",
	                          "sincerely",
	                          "ciao",
	                          "Best",
	                          "bGIF",
	                          "thank you",
	                          "thankyou",
	                          "talk soon",
	                          "cordially",
	                          "yours truly",
	                          "thanking You",
	                          "sent from my iphone"]

		salutation_opening_statements = ["hi","dear","to","hey","hello","thanks","good morning","good afternoon","good evening","thankyou","thank you"]

		zoned_message = zp.parse(message)

		analysis_result = []

		if(zoned_message["salutation"]):
			analysis_result.append(1)

			comma_newline_check = True

			for statement in salutation_opening_statements:
				if(statement in zoned_message["salutation"].lower()):
					analysis_result.append(1)
					comma_newline_check = False
				else:
					analysis_result.append(0)

			if comma_newline_check:
				analysis_result.append(1)
			else:
				analysis_result.append(0)
		else:
			analysis_result.append(0)

			analysis_result += [0] * len(salutation_opening_statements)

		if(zoned_message["signature"]):
			analysis_result.append(1)

			for statement in sig_opening_statements:
				if(statement in zoned_message["signature"].lower()):
					analysis_result.append(1)
				else:
					analysis_result.append(0)
		else:
			analysis_result.append(0)

			analysis_result += [0] * len(sig_opening_statements)
	    

		return analysis_result

	def get_features(self,message):
		#function to calculate the features outlined in our reference paper.
		#the features are assigned to properties of the class for indervidual reference but a function does exist to compile them to a vector. 
		#comments labels show which feature (as per the paper numbering) lines relate to

		self.char_count = len(message) #1

		num_digits = 0 #2
		num_letters = 0 #3
		num_upper = 0 #4
		num_spaces = 0 #5
		num_tabs = 0 #6
		self.occurence_list = [0] * 128 #7 & 8 & 19

		self.lines = 0 #21
	
		for character in message:
			if(character.isdigit()):
				num_digits +=1
			elif(character.isalpha()):
				num_letters +=1
				if(character.isupper()):
					num_upper +=1
			elif(character == '\n'):
				self.lines +=1
			elif(character.isspace()):
				num_spaces +=1
			elif(character == '\t'):
				num_tabs +=1
			

			self.occurence_list[ord(character.upper())] += 1


		self.ratio_digits = num_digits/self.char_count #2
		self.ratio_letters = num_letters/self.char_count #3
		self.ratio_upper = num_upper/self.char_count #4 
		self.ratio_spaces = num_spaces/self.char_count #5
		self.ratio_tab = num_tabs/self.char_count #6
		

		tokenised_sentences = nltk.sent_tokenize(message)
		self.sentence_count = len(tokenised_sentences) #22

		tokenised = nltk.word_tokenize(message) #9
		self.num_tokens = len(tokenised) #9

		sentence_lengths = [len(x) for x in tokenised_sentences] # 10
		self.average_sentance_length = sum(sentence_lengths)/len(sentence_lengths) #10
		
		token_lengths = [len(x) for x in tokenised] # 11
		self.average_token_length = sum(token_lengths)/len(token_lengths) #11
		
		self.chars_in_tokens_ratio = sum(token_lengths)/self.char_count #12

		short_words  = len([x for x in tokenised if len(x) <= 3])

		self.short_word_ratio = short_words/self.num_tokens #13

		#14
		self.word_length_ratios = []
		for word_length in range(1,21):
			self.word_length_ratios.append( len([x for x in tokenised if len(x) == word_length])/self.num_tokens )

		#15

		self.yule_k_measure = self.yule(tokenised) #16

		frequency_distribution = nltk.FreqDist(tokenised)
		self.hapax_legomena_count = len(frequency_distribution.hapaxes()) #17
		self.hapax_dislegomena_count =  len(self.calculate_hapax_dislegomena(frequency_distribution))#18

		self.function_word_occurences = list(self.get_function_word_occurences(frequency_distribution).values())#20


		#New Features (not in paper):

		self.incorrect_spellings_count = len(self.check_spelling(tokenised)) #NF1

		self.zone_analysis = self.analyse_email_zones(message) #NF2 - #NF30

	def calculate_hapax_dislegomena(self,distribution):
		
		return [word for word in distribution.keys() if distribution[word] == 2]

	def check_spelling(self,words):
		incorrect_spellings = []
		
		enchant_dict = enchant.Dict("en_UK")
		
		for word in words:
			if(not(enchant_dict.check(word))):
				incorrect_spellings.append(word)

		return incorrect_spellings

	def get_function_word_occurences(self,distribution):
		
		function_word_occurences = {}
		
		with open('function_words_1-0.csv') as csvfile:
		    csv_reader = csv.reader(csvfile, delimiter=',')     
		    
		    for row in csv_reader:
		    	function_word_occurences[row[0]] = distribution[row[0]]

		return function_word_occurences


	def as_list(self):
		#compiles features to vector
		return_list = []
		return_list.append(self.char_count) #1
		return_list.append(self.ratio_digits) #2
		return_list.append(self.ratio_letters) #3
		return_list.append(self.ratio_upper) #4
		return_list.append(self.ratio_spaces) #5
		return_list.append(self.ratio_tab) #6
		return_list = return_list + self.occurence_list # 7 & 8 & 19
		return_list.append(self.num_tokens) #9
		return_list.append(self.average_sentance_length) #10
		return_list.append(self.average_token_length) #11
		return_list.append(self.chars_in_tokens_ratio) #12
		return_list.append(self.short_word_ratio) #13
		return_list += self.word_length_ratios #14
		#15
		return_list.append(self.yule_k_measure) #16
		return_list.append(self.hapax_legomena_count) #17
		return_list.append(self.hapax_dislegomena_count) #18
		return_list = return_list + self.function_word_occurences #20
		return_list.append(self.lines) #21
		return_list.append(self.sentence_count) #22

		return_list.append(self.incorrect_spellings_count) #NF1
		
		return_list+= self.zone_analysis #NF2 - #NF30

		return return_list



### freature pattern code #####

class FeatureIntervals:

	def __init__(self,feature_index_in_vector,data_from_all_vectors,max_interval_size):
		
		self.from_index = feature_index_in_vector #index of feature from a full message feature vector
		self.data_list = data_from_all_vectors	#data all belonging to this feature
		self.working_data = [self.data_list[:]]	#list to be split during interval calculation
		self.intervals = [max(self.data_list)]	#list to store the interval thresholds (number stored in maximum for it's respective interval)
		
		self.intervaled_data = []	

		self.build_intervals(max_interval_size) #build the intervals for this feature

					#used to store the intervaled data for this feature

	def build_intervals(self,max_count_in_interval):

		all_intervals_below_max = False

		start_from_index = 0
		while(not all_intervals_below_max):

			all_intervals_below_max= True

			for interval_list_index in range(start_from_index,len(self.working_data)):
				if(len(set(self.working_data[interval_list_index]))>max_count_in_interval):
					all_intervals_below_max = False
					
					current_interval_min = min(self.working_data[interval_list_index])
					new_interval = current_interval_min+((max(self.working_data[interval_list_index]) - current_interval_min)/2)
					self.intervals.append(new_interval)
					
					new_lower_interval_data = [value for value in self.working_data[interval_list_index] if(value <= new_interval)]
					new_upper_interval_data = [value for value in self.working_data[interval_list_index] if(value > new_interval)]

					self.working_data[interval_list_index] = new_upper_interval_data
					self.working_data.insert(interval_list_index,new_lower_interval_data)

					start_from_index = interval_list_index
					break
		self.intervals.sort()
		self.intervaled_data = self.working_data
		

	def sort_data_by_intervals(self,input_data):
		self.intervaled_data = [[] for interval_list in range(len(self.intervals))]
		
		input_data.sort()
		final_interval_threshold = self.intervals[-1]
		
		interval_index = 0
		current_threshold = self.intervals[interval_index]

		for value_index in range(len(input_data)):
			
			value = input_data[value_index]

			if value > current_threshold and (interval_index != (len(self.intervals)-1)):
				interval_index +=1
				current_threshold = self.intervals[interval_index]

				if current_threshold == final_interval_threshold:
					self.intervaled_data[interval_index] += input_data[value_index:]
					break
				else:
					self.intervaled_data[interval_index].append(value)
			else:
				self.intervaled_data[interval_index].append(value)


		return self.intervaled_data



	def check_for_notable_interval(self,notable_interval_proportion_of_space = 0.3):		
		self.interval_sizes = [len(interval) for interval in self.intervaled_data]

		biggest_interval_max = max(self.interval_sizes)

		if (len(self.intervals) > 1) and (biggest_interval_max >= notable_interval_proportion_of_space * len(self.data_list)):
			return(self.interval_sizes.index(biggest_interval_max))
		else:
			return -1