# CUROP-CyberCrimeHub
Collaboration Between Cardiff University and Dyfed Powys Cyber Crime Unit to Analyse Writing Prints in Emails

# CUROP Demo
A very simple wireframe demonstration used to illurstrate a possible final result of the collaboration between the two parties.

A live version can be found here:
https://users.cs.cf.ac.uk/HarborneD/CUROP-wireframe/index.html

To explore the demo as intended follow these steps:

___
Part 1 (left hand side)
name: Joe Bloggs
email:

Click Add Account
Platform: Twitter
Account Id: TwitterNerd

Click 'Find Accounts'

This process shows that from a name and a twtter account the hub can search facebook accounts and rate the porbability that they are owned by the suspect.

It also shows that modules can be added for other platforms over time (such as instagram. Though in this demo it is shown that no instagram account could be found for the user)

___
Part 2 (Right hand side)

Click 'Add Account' 3 times

For each account that appears select an account type from the drop down and enter an Account Id (any dummy data will do)

Click 'Predict Ownership'

Probabilities that the suspect fromt he left is also the opperator of each of the 3 accounts is displayed

This shows that from a suspect profile on the left, we can check ownership of other accounts. Options exist to import and export the target accounts to deal with large volumes of accounts.

___



#Email Author Matching Module

This module was the focus of the first 8 weeks of the collaboration. It takes in clusters of emails and uses writing style identification techniques to check similarities between other clusters. It returns a list of the target cluster names sorted by similarity.

Instrcutions:

Place suspect email clusters in a folder per cluster within the appropriate location within email_temp (suspect clusters in suspect_users, target clusters in target_users)

Cluster folder names are used to identify the cluster in output results

You can pass a pre-processing functioning to the module that should accept the path of an email and output the email text after any desired pre-processing. 

Example email clusters are provided along with a demonstration.

Producing feature prints can take time, if you would like to monitor progress, pass "verbose=True" when creating the Matcher.
