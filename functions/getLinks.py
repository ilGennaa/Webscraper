def getLinks(linkFP):

	LINKS = []
	with open(linkFP ,'r') as f:
		for line in f.readlines():
				LINKS.append(line.split(' , '))
				for numline in range(len(LINKS[-1])):
						LINKS[-1][numline] = LINKS[-1][numline].rstrip()
	return LINKS