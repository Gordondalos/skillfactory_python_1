target_word = 'анна'
target_chapter = 4
import math


def read_data():
    handle = open('../war_peace_processed.txt', 'rt', encoding="utf-8")
    res = handle.read()
    handle.close()
    return res.split('\n')


class Filters:
    chapters = {}
    data = {}
    info = {}

    def __init__(self, data):
        self.data = data

    def draw_dict(self, data):
        words = {}
        for word in data:
            value = words.get(word, 0)
            words[word] = value + 1
        return words

    def get_chapter(self):
        return [chapter[0] for chapter in enumerate(self.data) if chapter[1] == '[new chapter]']

    def get_chapters(self):
        chapters = self.get_chapter()
        last_index = len(self.data)
        chapters.append(last_index)
        self.chapters = chapters

    def get_info(self, word):
        words = {}
        previous_index = 0
        count_chapter_with_word = 0
        for chapter in self.chapters:
            chapter_list = self.data[previous_index:chapter]
            previous_index = chapter
            words[chapter] = self.draw_dict(chapter_list)
            count_target = words[chapter].get(word, 0)
            if count_target > 0:
                count_chapter_with_word += 1

        return count_chapter_with_word

    def get_info_by_chapter(self, number_chapter):
        words = {}
        previous_index = 0
        index = 0
        for chapter in self.chapters:
            chapter_list = self.data[previous_index:chapter]
            previous_index = chapter
            words[chapter] = self.draw_dict(chapter_list)
            if index == number_chapter:
                self.info = words[chapter]
                return words[chapter]
            index += 1
        return False

    def get_number(self, word, df):
        count_target = self.info.get(word, 0)
        count_words = -1

        for item in self.info:
            count_words += self.info.get(item, 0)

        tf = count_target
        chapter_size = count_words
        return math.log(1 + tf / chapter_size) * math.log(1 / df)

    def get_result(self):
        arr = {}
        for word in self.info:
            count_chapter_with_word = self.get_info(word)
            df = count_chapter_with_word / len(self.chapters)

            arr[word] = self.get_number(word, df)
        return self.my_sort(arr)

    def my_sort(self, arr):
        return sorted(list(arr.items()), key=lambda i: i[1], reverse=True)


data = read_data()

my_filter = Filters(data)
my_filter.get_chapters()
my_filter.get_info_by_chapter(target_chapter)

s_arr = my_filter.get_result()

arres = s_arr[:3]
res = ''

index = 0
for item in arres:
    res += item[0]
    if index != 2:
        res += ' '

print(res)