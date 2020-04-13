if __name__ == "__main__":
    import sys
    sys.exit()

def Ask(question):
	"""
	Creates a (Y/N) question with given question string.
	:param question: (str) question string
	:returns: bool
	"""
	q = ''
	while not any([q.upper() == 'Y', q.upper() == 'N']):
		try: q = raw_input(question + '(Y/N): ')
		except NameError: q = input(question + '(Y/N): ')
            
		if q.upper() == 'Y':
			return True
		elif q.upper() == 'N':
			return False