from lxml import objectify

class PWObjectifyOutputParser:
    def parse(self, file_path):
        with open(file_path, encoding='utf8') as f:
            root = objectify.parse(f).getroot()
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
        objectify.deannotate(root, cleanup_namespaces=True)
        return root

if __name__ == '__main__':
    parser = PWObjectifyOutputParser()
    output = parser.parse('./pwscf.xml')
    print(output.output.total_energy.etot)
    