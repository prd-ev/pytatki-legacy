from flask import render_template

with open('db/render.txt') as fp:
    files = fp.readlines()

for f in files:
    #x = render_template(f, dbname='pytatki2')
    with open(f, 'w') as fp:
        # fp.write(x)
