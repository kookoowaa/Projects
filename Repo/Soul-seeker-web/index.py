print("content-type: text/html; charset=utf-8")
print()
import cgi, os, module

cgi_data = module.classification()
box ='''
<select class="form-control" id="jsonstandard" name="jsonstandard">
            <option value="1" selected="">성질</option>
            <option value="2">직업</option>
            <option value="3">등급</option>
'''

print('''
<!doctype html>
<html>
<head>
  <title>Soul Seeker - 6th Knight Hero List</title>
  <meta charset="utf-8">
</head>

<body>
    <h1>Hero List</h1>
    <strong>Filter by...</strong>
    <br>
    {box}
    </select>
</body>
'''.format(box=box)




  <h1><a href="index.py">WEB</a></h1>
  <ol>{list}</ol>
  {create}
  {update}
  {delete}
  <h2>{title}</h2>
  <p>{desc}</p>

</body>
'''.format(title = cgi_data['pageId'], desc = cgi_data['desc'], 
           list = module.getList(), create = cgi_data['create'],
           update = cgi_data['update'], delete = cgi_data['delete']))
