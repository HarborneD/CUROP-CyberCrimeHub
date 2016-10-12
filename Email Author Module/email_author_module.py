import os

from feature_analysis import FeatureAnalysis
from feature_analysis import FeatureIntervals



class EmailAuthorMatcher:

	def __init__(self,suspects_dir,targets_dir,notable_interval_ratio=0.3,max_interval_size_ratio=0.5,ignore_features=None,ignore_feature_aspects=None,process_function=None,verbose=False):
		
		if(ignore_features == None):
			self.ignore_features = []
		else:
			self.ignore_features = ignore_features

		if(ignore_feature_aspects == None):
			self.ignore_feature_aspects=["138_2","5_1","146_0","139_1","137_1","457_0","146_1","138_1","143_0","161_0","141_1","150_0","149_0","147_1","144_1","145_1","3_2","136_1","86_0","142_2","76_0","85_0","151_0","89_0","4_1","140_1","147_0","149_1"]
		else:
			self.ignore_feature_aspects = ignore_feature_aspects
		self.notable_interval_ratio = notable_interval_ratio

		self.max_interval_size_ratio = max_interval_size_ratio

		#get the messages for all users
		if(verbose):
			print("Analysing Suspect Messages")
		self.suspects_notation_list = self.GetUserNotationList(suspects_dir,process_function=process_function,verbose=verbose)

		if(verbose):
			print("")
			print("Analysing Target Messages")
		self.targets_notation_list = self.GetUserNotationList(targets_dir,process_function=process_function,verbose=verbose)

		self.comparison_results = self.PerformPrintComparisons(self.targets_notation_list,self.suspects_notation_list)

	def SetIgnoreFeatures(self,ignore_feature_list):
		self.ignore_features=ignore_feature_list

	def SetIgnoreFeatureAspects(self,ignore_feature_aspects_list):
		self.ignore_feature_aspects=ignore_feature_aspects_list

	

	def GetMessageStringsFromDir(self,message_dir,extract_limit=0,process_function=None):
		messages = []

		message_list = os.listdir(message_dir)

		message_count = 0
		for message in message_list:
			message_count+=1

			
			if process_function != None:
				message_string = process_function(os.path.join(message_dir,message))
			else:
				message_string = open(os.path.join(message_dir,message),"r").read()
			
			messages.append(message_string)
			if((extract_limit > 0) and (message_count >= extract_limit)):
				break

		return messages

	def ProduceFeatureVectors(self,messages):
		#function that takes a list of messages(as strings) and creates an instance of the feature_analysis for each
		#returns a list of these instances
		vectors = []

		for message in messages:
			vectors.append(FeatureAnalysis(message).as_list())
		
		
		return vectors

	def GetFeaturePrint(self,vectors,feature_intervals_list,notable_interval_ratio = 0.3,ignore_features=[],ignore_feature_aspects=[]):
		notation_feature_print = []

		#for each feature in an email feature vector
		for feature_index in range(len(feature_intervals_list)):
			feature_set = [vector[feature_index] for vector in vectors] #get the value from all vectors for the current feature

			feature_intervals_list[feature_index].sort_data_by_intervals(feature_set)
			
			notable_result = feature_intervals_list[feature_index].check_for_notable_interval(notable_interval_ratio)
			
			if(notable_result != -1):
				if not( (feature_index+1) in ignore_features):
					if not( (str(feature_index+1)+"_"+str(notable_result)) in ignore_feature_aspects):
						notation_feature_print.append( ("F"+str(feature_index+1),notable_result) )
			
		return notation_feature_print

	def CreateFeatureIntervals(self,feature_vectors,interval_max_size_ratio=0.5):
		feature_intervals_list=[]

		for feature_index in range(len(feature_vectors[0])): # for each feature of an email feature vector
			feature_set = [vector[feature_index] for vector in feature_vectors] # get the value from vectors for the current feature
			
			feature_intervals_list.append(FeatureIntervals(feature_index,feature_set,round(len(feature_set)*interval_max_size_ratio)))

		return feature_intervals_list

	def GetUserNotationList(self,user_dir,process_function=None,verbose=False):
		users_notation_list = []

		user_list = os.listdir(user_dir)

		
		for user in user_list:

			if(verbose):
				print("")
				print("Current User: "+str(user))
				
			user_message_list = self.GetMessageStringsFromDir(os.path.join(user_dir,user),process_function=process_function)

			feature_vectors = self.ProduceFeatureVectors(user_message_list) 

			feature_intervals_list = self.CreateFeatureIntervals(feature_vectors,self.max_interval_size_ratio)
			
			notation_feat_print = self.GetFeaturePrint(feature_vectors,feature_intervals_list,self.notable_interval_ratio,self.ignore_features,self.ignore_feature_aspects)
			

			users_notation_list.append( (user,notation_feat_print ) )
		return users_notation_list

	def PerformPrintComparisons(self,corpus_notations,suspect_notations):
		comparison_summaries = []

		feature_print_aspect_list = []

		for suspect_index in range(len(suspect_notations)):
		
			comp_summary = self.CompareSuspectToCorpus(suspect_notations[suspect_index],corpus_notations)

			comparison_summaries.append(sorted(comp_summary,key=lambda x: x[1],reverse=True))

		return comparison_summaries


	def CompareSuspectToCorpus(self,suspect_notation_print,corpus_notation_prints,show_full_prints=False,verbose=False):
		match_list = []
	
		suspect_set = set(suspect_notation_print[1])

		intersection_count_list =[]
		biggest_intersection_print = []
		biggest_intersection_count = 0



		for user in range(len(corpus_notation_prints)):
			
			user_set = set(corpus_notation_prints[user][1])
			
			intersection = suspect_set.intersection(user_set)
			

			intersection_count_list.append( (str(corpus_notation_prints[user][0]),len(intersection)) )

		return intersection_count_list

	def ReturnSectionedResulted(self):
		user_results = []

		for user_result in self.comparison_results:
			sectioned_results = []

			current_section = []
			current_section_count = -1

			for result in user_result:
				if(result[1] < current_section_count):
					sectioned_results.append(current_section[:])
					current_section = [result]
					current_section_count = result[1]
				elif(current_section_count == -1):
					current_section = [result]
					current_section_count = result[1]
				else:
					current_section.append(result)
			
			if(len(current_section)>0):
				sectioned_results.append(current_section[:])
			
			user_results.append(sectioned_results[:])

		return user_results

