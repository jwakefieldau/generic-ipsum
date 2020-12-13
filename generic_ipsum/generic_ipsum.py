import random
import re

from collections import defaultdict

# generic template processing, separate this into another module
class GenericIpsum(object):

    def __init__(self):
        self.tag_re = re.compile(r'\[(.+?)\]')

        # change these - might not need to be res
        self.num_range_re = re.compile(r'([0-9]+)-([0-9]+)')
        self.kw_map = self.build_kw_map()
        self.tag_frag_map = self.build_tag_frag_map()

    def build_kw_map(self):
        kw_map = defaultdict(list)
        for (tag_name, tag_kw_list,) in self.terms.items():
            for tag_kw in tag_kw_list:
                kw_map[tag_kw].append(tag_name)
        return kw_map

    def build_tag_frag_map(self):
        tag_frag_map = defaultdict(list)
        for (i, frag_list,) in enumerate(self.fragments):
            for (j, frag,) in enumerate(frag_list):
                for tag in self.tag_re.findall(frag):
                    tag_frag_map[tag].append((i,j,))
        return tag_frag_map
                
    def num_range(self, min_num, max_num):
        num_list = list(range(min_num, max_num + 1))
        return str(random.choice(num_list))

    def literal_list(self, list_str):
        literal_elem_list = self.literal_list_re.findall(list_str)
        return random.choice(literal_elem_list)

    def term(self, term_str):
        term_choice_list = self.terms[term_str]
        return random.choice(term_choice_list)

    def process_tag(self, inner_str):
        inner_m = self.num_range_re.match(inner_str)
        if inner_m:
            return self.num_range(int(inner_m.group(1)), int(inner_m.group(2)))
        else:
            return self.term(inner_str)
        
    def process_fragment(self, frag_str, keyword=None, kw_tag=None):
        #return self.tag_re.sub(self.process_tag, frag_str)
        for inner_tag_str in self.tag_re.findall(frag_str):
            if keyword and kw_tag == inner_tag_str:
                frag_str = frag_str.replace(f"[{inner_tag_str}]", keyword, 1)
            else:
                frag_str = frag_str.replace(f"[{inner_tag_str}]", self.process_tag(inner_tag_str), 1)
        return frag_str

    def get(self, keyword=None):
        ret_str_list = []

        if keyword:
            kw_tag_list = self.kw_map.get(keyword)
            if not kw_tag_list:
                return None
            tag_choice = random.choice(kw_tag_list)
            tag_frag_list = self.tag_frag_map.get(tag_choice)
            (frag_choice_i, frag_choice_j,) = random.choice(tag_frag_list)

        for (i, cur_frag_list,) in enumerate(self.fragments):
            if keyword and i == frag_choice_i:
                cur_frag = cur_frag_list[frag_choice_j]
                proc_frag = self.process_fragment(cur_frag, keyword=keyword, kw_tag=tag_choice)
            else:     
                cur_frag = random.choice(cur_frag_list)
                proc_frag = self.process_fragment(cur_frag)
            ret_str_list.append(proc_frag)

        return '. '.join(ret_str_list)

    def __iter__(self):
        return self

    def __next__(self):
        return self.get() 
