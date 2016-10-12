# CUROP-CyberCrimeHub
Collaboration Between Cardiff University and Dyfed Powys Cyber Crime Unit to Analyse Writing Prints in Emails


#Email Author Matching Module

This module was the focus of the first 8 weeks of the collaboration. It takes in clusters of emails and uses writing style identification techniques to check similarities between other clusters. It returns a list of the target cluster names sorted by similarity.

Instrcutions:

Place suspect email clusters in a folder per cluster within the appropriate location within email_temp (suspect clusters in suspect_users, target clusters in target_users)

Cluster folder names are used to identify the cluster in output results

You can pass a pre-processing functioning to the module that should accept the path of an email and output the email text after any desired pre-processing. 

Example email clusters are provided along with a demonstration.

Producing feature prints can take time, if you would like to monitor progress, pass "verbose=True" when creating the Matcher.
