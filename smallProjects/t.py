
CHECK_LIST = ['united kingdom', 'visa', 'travel', 'passport', 'afghanistan']
responseHtml = 'visahanjgntravel vi sa passport'

if True in [text in responseHtml.lower() for text in CHECK_LIST]:
	print('YES')
else:
	print('NO')