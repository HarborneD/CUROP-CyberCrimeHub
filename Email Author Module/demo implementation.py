import os

from email_author_module import EmailAuthorMatcher


#Custom email string pre-processing function
def ExtractEnronMessage(email_file):
	
	file_text = ""

	with open(email_file) as mail_file:
		for line in mail_file:
			if len(line) == 1:                
				for line in mail_file:
					file_text+=line
	return file_text

matcher = EmailAuthorMatcher( os.path.join("emails_temp","suspect_users"),os.path.join("emails_temp","target_users"),process_function=ExtractEnronMessage,verbose=True  )


for result in matcher.comparison_results:
	print("")
	print(result)

sectioned_results = matcher.ReturnSectionedResulted() 

for user_result_index in range(0,len(sectioned_results)):
	print("")
	print("Suspect: " +str(matcher.suspects_notation_list[user_result_index][0]))
	for section in sectioned_results[user_result_index]:
		print(section)