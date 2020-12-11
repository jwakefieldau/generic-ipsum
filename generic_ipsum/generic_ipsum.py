import random
import re

# generic template processing, separate this into another module
class GenericIpsum(object):

    def __init__(self):
        self.tag_re = re.compile(r'\[(.+?)\]')

        # change these - might not need to be res
        self.num_range_re = re.compile(r'([0-9]+)-([0-9]+)')
        self.literal_list_re = re.compile(r"('[^']+',\s*)+'[^']+'")
        self.literal_list_split_re = re.compile(r'\W+')

    def num_range(self, min_num, max_num):
        num_list = list(range(min_num, max_num + 1))
        return str(random.choice(num_list))

    def literal_list(self, list_str):
        split_elems = re.split(self.literal_list_split_re, list_str)
        literal_elem_list = [elem for elem in split_elems if elem != '']
        return random.choice(literal_elem_list)

    def term(self, term_str):
        term_choice_list = self.terms[term_str]

        return random.choice(term_choice_list)

    def process_tag(self, m):
        inner_str = m.group(1)
        
        inner_m = self.num_range_re.match(inner_str)
        if inner_m:
            return self.num_range(int(inner_m.group(1)), int(inner_m.group(2)))
 
        inner_m = self.literal_list_re.match(inner_str)
        if inner_m:
            return self.literal_list(inner_str)

        else:
            return self.term(inner_str)
        
    def process_fragment(self, frag_str):
        return self.tag_re.sub(self.process_tag, frag_str)

    def get(self):
        ret_str_list = []

        for cur_frag_list in self.fragments:
            cur_frag = random.choice(cur_frag_list)
            proc_frag = self.process_fragment(cur_frag)
            ret_str_list.append(proc_frag)

        return '. '.join(ret_str_list)
 
    def __iter__(self):
        return self

    def __next__(self):
        return self.get() 
