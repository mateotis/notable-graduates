rankings = open("THE2020_v2.txt","r")
unis = open("unis.txt","w")
lines = rankings.read().splitlines()
for line in lines:
	line = line[line.find(',')+1:]
	if line.find('"') != -1:
		line = line[1:]
		line = line[0:line.find('"')]
	else:
		line = line[0:line.find(',')]
	print(line)
	unis.write(line + '\n')