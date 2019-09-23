################################################################################
#                                                                              #
#         UNOBFUSCATE.py - Recovers files obfuscated using OBFUSCATE.py        #
#                                                                              #
################################################################################
#                                                                              #
#    Author:  Alexander Liptak                                                 #
#    Email:   Alexander.Liptak@live.rhul.ac.uk                                 #
#    Tel:     +44 7901 595107                                                  #
#    Date:    23/09/2019                                                       #
#                                                                              #
################################################################################
#                                                                              #
#    Minimum requirements:                                                     #
#        - Python 3.6                                                          #
#                                                                              #
################################################################################

from csv import DictReader			# reading dicts from CSV files
from pathlib import Path			# path manipulation
from sys import argv, exit			# handling arguments and safe exits

################################################################################

if __name__ == "__main__":
	try:	
		# initial check to see if 1 argument has been passed to the script
		if len(argv) != 2:
			raise TypeError("Expected 1 argument!")

		# instantiate a path object and test whether it is an existing path
		path = Path(argv[1])
		if not path.is_dir():
			raise FileNotFoundError("Path \"{}\" does not exist!".format(path))
		
		# check whether unobfuscate.csv exists
		unobfuscate_file = path.joinpath("unobfuscate.csv")
		if not unobfuscate_file.is_file():
			raise FileNotFoundError("Cannot find unobfuscate.csv file!")
		
		# read csv file into dict against which filenames will be unobfuscated
		with unobfuscate_file.open('r') as f:
			csv_reader = DictReader(f)
			unobfuscate_dict = dict(*csv_reader)
			
			# iterate over all files and dirs and rename against loaded dict
			for p in path.glob('**/*'):
				if p.name == "unobfuscate.csv": continue
				p.rename(p.with_name(unobfuscate_dict[p.name]))
		
	except (TypeError, FileNotFoundError) as e:
		print("[CRITICAL]: {}".format(e))
		exit(1)
	except KeyboardInterrupt as e:
		raise
	except Exception as e:
		print("[UNHANDLED]: {}".format(e))
		exit(2)