def writeHistory(historyFP, prices):
	with open(historyFP, 'a') as f:
		for key, item in prices.items():
			for it in item:
				f.write(" ".join([key, it[0], it[1], it[2], "\n"]))
			f.write("\n")