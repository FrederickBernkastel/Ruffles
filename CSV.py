import csv

class CSV:
    def __init__(self, link, fieldnames):
        self.link = link
        self.content = []
        self.fieldnames = fieldnames

    #list of key value pairs
    def push(self, dict):
        self.content.append(dict)
        return None

    def displayValues(self):
        if self.content is not None:
            print "These are the field names:"
            print self.fieldnames

            print "These are the data inside the csv file"
            for item in self.content:
                print item
        else:
            print "Nothing in the list right now."

    def save(self):
        file = open(self.link, 'w')
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        for item in self.content:
            writer.writerow(item)

        file.close()

    def read(self):
        file = open(self.link)
        reader = csv.DictReader(file)
        self.content = []

        for item in reader:
            self.content.append(item)

        file.close()


if __name__ == '__main__':
    newCsv = CSV("names.csv", ["first_name", "last_name"])
    newCsv.read()

    newCsv.displayValues()
