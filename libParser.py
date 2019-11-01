from liberty.parser import parse_liberty
library = parse_liberty(open("test.lib").read())

print(str(library))