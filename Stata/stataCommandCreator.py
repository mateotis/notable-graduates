countryNames = []

nameFile = open("countryList.txt","r")
lines = nameFile.read().splitlines()
for i in lines:
	countryNames.append(i)

commandFile = open("stataCommands.txt","w")
cnt = 1
for i in countryNames:
	if "political" in i:
		keepIf = 'keep if strpos(area1_of_ratt,"'+i+'")'
	else:
		keepIf = 'keep if area1_of_ratt=="'+i+'"'
	commandFile.write(keepIf)
	commandFile.write('\n')
	commandFile.write("keep if _n<100\n")
	commandFile.write('save "/Users/ew1555/Dropbox/CORE COURSE/2019/final essay data extraction/MAT_alma_mater' + str(cnt) + '.dta", replace\n')
	commandFile.write('restore\n')
	commandFile.write('preserve\n')
	cnt += 1;

commandFile.write('use "/Users/ew1555/Dropbox/CORE COURSE/2019/final essay data extraction/MAT_alma_mater1.dta", clear\n')
commandFile.write('forvalues k=2/'+str(cnt-1)+'{\n')
commandFile.write('append using "/Users/ew1555/Dropbox/CORE COURSE/2019/final essay data extraction/MAT_alma_mater' + "`k'.dta\n")
commandFile.write('}\n')
commandFile.write('save "/Users/ew1555/Dropbox/CORE COURSE/2019/final essay data extraction/MAT_alma_mater_top100_15countries.dta", replace\n')
commandFile.write('export delimited using "/Users/ew1555/Dropbox/CORE COURSE/2019/final essay data extraction/MAT_alma_mater_top100_15countries.csv", replace\n')