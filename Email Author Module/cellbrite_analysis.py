import os
import xlrd
import uuid

from email_author_module import EmailAuthorMatcher


def CheckIfSent(xls_row):
	return True


def GetSentMessages(email_sheet):

	emails_dict = {}

	if(email_sheet.nrows > 2):
		for row_index in range(2,email_sheet.nrows):
			if(CheckIfSent(email_sheet.row(row_index))):
				sender = email_sheet.cell(row_index,1).value
				if(sender in emails_dict):
					emails_dict[sender].append(email_sheet.cell(row_index,13).value)
				else:
					emails_dict[sender] = [email_sheet.cell(row_index,13).value]

	return emails_dict


def CreateMailUsersFromCellXLS(xls_path,user_label,output_path):
	cellebrite_output = xlrd.open_workbook(xls_path, on_demand=True)

	email_sheet = cellebrite_output.sheet_by_name('Emails')

	emails_dict = GetSentMessages(email_sheet)

	print("user: " + str(user_label))
	print("email accounts found:" +str(len(emails_dict.keys())))
	for key in emails_dict:
		unique_label = user_label + " - " + str(key.replace('.',""))
		email_output_path = os.path.join(output_path,unique_label)
		os.makedirs(email_output_path)

		message_count = 0
		for message in emails_dict[key]:
			with open(os.path.join(email_output_path,str(message_count)+".txt"),"w") as output_file:
				output_file.write(message)
			message_count += 1


def ConvertData(data_path,data_label):
	output_path = os.path.join("temp storage",data_label)

	if not os.path.exists(output_path):
		os.makedirs(output_path)

	suspects_dir = os.path.join(output_path,"suspect_users")
	os.makedirs(suspects_dir)
	
	targets_dir = os.path.join(output_path,"target_users")
	os.makedirs(targets_dir)
    
	input_suspects_dir = os.path.join(data_path,"suspects")
	input_targets_dir = os.path.join(data_path,"targets")

	input_suspects = os.listdir(input_suspects_dir)
	input_targets = os.listdir(input_targets_dir)

	print("suspects found: "+str(len(input_suspects)))
	print("")
	print("targets found: "+str(len(input_targets)))

	for suspect in input_suspects:
		suspect_path = os.path.join(input_suspects_dir,suspect)
		suspect_label = os.path.splitext(os.path.basename(suspect_path))[0]
		CreateMailUsersFromCellXLS(suspect_path,suspect_label,suspects_dir)    	

	for target in input_targets:
		target_path = os.path.join(input_targets_dir,target)
		target_label = os.path.splitext(os.path.basename(target_path))[0]
		CreateMailUsersFromCellXLS(target_path,target_label,targets_dir)    	




data_path = os.path.join("cellebrite","cellbrite test data")
session_uuid = str(uuid.uuid1())

ConvertData(data_path,session_uuid)

data_path = os.path.join("temp storage",session_uuid)

matcher = EmailAuthorMatcher( os.path.join(data_path,"suspect_users"),os.path.join(data_path,"target_users"),verbose=True  )


for result in matcher.comparison_results:
	print("")
	print(result)

sectioned_results = matcher.ReturnSectionedResulted() 
6
for user_result_index in range(0,len(sectioned_results)):
	print("")
	print("Suspect: " +str(matcher.suspects_notation_list[user_result_index][0]))
	for section in sectioned_results[user_result_index]:
		print(section)