class UVSetNamer():
	name_index = 0
	pass

def Name():
	UVSetNamer.name_index += 1
	return "TempNamed_" + str(UVSetNamer.name_index)