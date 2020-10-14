import json

class JsonParser:
    def __init__(self):
        self.json_file = "sample2.json"

    def read_json(self, json_file):
        """Reads .json file and returns json data"""
        with open(json_file, 'r') as myfile:
            data=myfile.read()
        obj = json.loads(data)
        return obj

    def get_words(self):
        """Gets all the words in the json file"""
        json_words = []
        obj = self.read_json(self.json_file)
        x = obj["AudioFileResults"][0]["SegmentResults"]
        for i in range(len(x)):
            json_words += x[i]["NBest"][0]["Words"]
        return json_words

    def find_word(self, word):
        """Returns the index of word in the json data if found"""
        json_words = self.get_words()
        for i in range(len(json_words)):
            if word == json_words[i]["Word"]:
                break
        #print("[find_word] ", i)
        return i

    def in_sequence(self, l):
        """Checks if words indicies are in sequence"""
        for i in range(len(l)-1):
            if l[i+1] != 1 + l[i]:
                return False
        #print("[in_sequence] True")
        return True

    def get_duration_offset(self, l1, l2):
        """Returns offsets difference between 2 lists of words"""
        l1_idx = []
        l2_idx = []
        l1_offset = 0
        l2_offset = 0
        json_words = self.get_words()
        for word in l1:
            i = self.find_word(word)
            l1_idx.append(i)
        if self.in_sequence(l1_idx):
            last_word, idx_json_words = l1[-1], l1_idx[-1]
            l1_offset = json_words[idx_json_words]["Offset"]/10000000
            #print(l1_offset)

        for word in l2:
            i = self.find_word(word)
            l2_idx.append(i)
        if self.in_sequence(l2_idx):
            last_word, idx_json_words = l2[-1], l2_idx[-1]
            l2_offset = json_words[idx_json_words]["Offset"]/10000000
            #print(l2_offset)

        return l2_offset - l1_offset, (l2_offset - l1_offset)/60

if __name__ == "__main__":
    l1 = ["provident", "god"]
    l2 = ["W", "jerome"]
    jp = JsonParser()
    print(l1)
    print(l2)
    print("Duration: {}".format(jp.get_duration_offset(l1, l2)))
