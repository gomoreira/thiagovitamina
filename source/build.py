import os,shutil,sys
SRC=sys.argv[1]; OUT=sys.argv[2]
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(SRC,OUT)
for f in ['index.html','trade-in.html']:
    s=open(os.path.join(SRC,f)).read()
    k=s.index('<header')
    head,body=s[:k],s[k:]
    doc=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
         '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
         '<meta name="theme-color" content="#ffffff">\n'+head.strip()+'\n</head>\n<body>\n'+body.strip()+'\n</body>\n</html>\n')
    open(os.path.join(OUT,f),'w').write(doc)
open(os.path.join(OUT,'vercel.json'),'w').write('{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
print('built',OUT)
