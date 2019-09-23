################################################################################
#                                                                              #
#       OBFUSCATE.py - Cryptographically secure directory tree obfuscator      #
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
#    About: a script that will obfuscate the directory tree, intended for use  #
#        with compression/packaging softwares that store the directoy tree in  #
#        plaintext. The script accepts only 1 argument: the relative or        #
#        absolute path of the directory to be obfuscated. The script also      #
#        creates a file titled unobfuscate.csv which contains a dictionary     #
#        against which the original directory tree can be recovered.           # 
#                                                                              #
################################################################################
#                                                                              #
#    Minimum requirements:                                                     #
#        - Python 3.6                                                          #
#                                                                              #
################################################################################

from csv import DictWriter			# writing dicts to CSV files
from pathlib import Path			# path manipulation
from secrets import choice			# cryptographically secure random selector
from string import hexdigits		# string of hexadecimal characters
from sys import argv, exit			# handling arguments and safe exits

uuid_len = 32						# declare global length of UUID

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
			
		# safety check! make sure longest path will not exceed MAX_PATH
		base_length = len(str(path.resolve()))
		max_obfuscated = 0
		for p in path.glob('**/*'):
			depth = len(str(p.relative_to(path)).split('\\'))
			obfuscated = (uuid_len * depth) + depth
			if obfuscated > max_obfuscated:
				max_obfuscated = obfuscated
		if base_length + max_obfuscated + 1 > 260:
			raise RuntimeError("Obfuscated path(s) will exceed MAX_PATH!")
		
		# dict will store mapping from obfuscated to unobfuscated path
		unobfuscate = {}	# {obfuscated name: unobfuscated name}
		
		# recursively traverse directory tree, renaming all files and dirs
		for p in path.glob('**/*'):
			uuid = ''.join(choice(hexdigits) for _ in range(uuid_len)).lower()
			unobfuscate[uuid] = p.relative_to(path).name
			p.rename(p.with_name(uuid).with_suffix(''))
		
		# save dict to csv file for unobfuscation
		csv_file = path.joinpath("unobfuscate.csv")
		csv_file.touch()
		with csv_file.open('w') as f:
			writer = DictWriter(f, unobfuscate.keys())
			writer.writeheader()
			writer.writerow(unobfuscate)

	except (TypeError, FileNotFoundError) as e:
		print("[CRITICAL]: {}".format(e))
		exit(1)
	except KeyboardInterrupt as e:
		raise
	except Exception as e:
		print("[UNHANDLED]: {}".format(e))
		exit(2)
