from FRG import databaseFunctions as dbf
from GDR import basicFunctions as bscf

for i in range(1,148):
	bak = dbf.get_bakery_from_id(i)
	print bak.name
	newName = bak.name.replace('(Brood- & banketbakkerijen)','')
	bscf.update_bakery(bak.id,newName,bak.adress,bak.postcode,bak.city,bak.GPSLat,bak.GPSLon,bak.telephone,bak.email,bak.website,bak.foto_url,bak.openings,bak.description,bak.bestelLimitTime,bak.bankAccount,bak.member)
