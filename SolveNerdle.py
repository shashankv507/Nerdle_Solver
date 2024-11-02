# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import re

debug = False
# debug = True
class Universe():
    def __init__(self):
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.operators = ['+', '-', '*', '/']
        self.operator_regex = r'\+|\-|\*|\/'
        self.equals = '='

class Feedback():
    def __init__(self):
        self.found = {}
        self.barred = []
        self.shuffle = {}
        self.submissions = []
        self.invalid_config = []
        self.found_valid_config = None
    
class Field(Universe):
    def __init__(self, position):
        super().__init__()
        self.value = None
        self.is_fixed = False
        self.input_set = self.numbers + self.operators
        self.is_equalsto = False
        self.index = position

class Equation(Universe, Feedback):
    def __init__(self, total_length):
        super().__init__()
        super(Universe, self).__init__()
        self.length = total_length
        self.equation_set = []
        self.equation_fields = [] # List of field objects
        self.equation = ''
        self.found = {}
        self.barred = []
        self.shuffle = {}
        self.submissions = []
        self.invalid_config = []
        self.found_valid_config = None
        
    def execute(self):
        configs = self.gen_equation_configs()
        eqn_set = []
        input_collection = []
        
        if len(self.equation_fields)==0:
            self.initialize_fields(self.length)
        self.equation_fields = self.process_feedback()
        for f in self.equation_fields:
            f.input_set = f.numbers + f.operators
            if debug is True:print('--',f.input_set)
            input_collection.append(f.input_set)
            
        if self.found_valid_config is not None:
            configs = [(self.found_valid_config , self.length-self.found_valid_config)]
        for c in configs:
            eq_len = c[0]
            if eq_len in self.invalid_config:
                continue
            temp = self.generate_equation_set(eq_len, input_collection)
            eqn_set = eqn_set + temp
            if debug is True:print('Running for config:',c, 'Found', len(temp), 'Entries')
        self.equation_set = eqn_set   
        # print(len(self.equation_set))
        self.filterout_invalid()
        # print(len(self.equation_set))
        self.complete_equation_set()
        # print(len(self.equation_set))
        # self.print_input_set()
        self.filterout_invalid2()
        # print(len(self.equation_set))
        
        
        # Generate score for each entry
        if debug is True:print('Valid Equations: ', self.equation_set)
        # if debug is True:print('Get Equation with max score')
        return self.selector()
    
    def print_input_set(self):
        for f in self.equation_fields:
            print(f.input_set)
    
    def gen_equation_configs(self):
        x = self.length - 2
        y = 1
        config = []
        while x >= y:
            config.append((x, y))
            x = x-1
            y = y+1
        return config
        
    def update_feedback(self, feedback_obj):
        self.found = feedback_obj.found
        self.barred = feedback_obj.barred
        self.shuffle = feedback_obj.shuffle
        self.submissions = feedback_obj.submissions
        self.invalid_config = feedback_obj.invalid_config
        self.found_valid_config = feedback_obj.found_valid_config
        if debug is True:print('found', self.found)
        if debug is True:print('barred', self.barred)
        if debug is True:print('shuffle', self.shuffle)
        if debug is True:print('submissions', self.submissions)
        if debug is True:print('invalid_config', self.invalid_config)
        if debug is True:print('found_valid_config', self.found_valid_config)
        return

    def equation_preset(self):
        """
        Equation preset to start off providing head start
        """
        # x = '1+3*8=25'
        x = '102-94=8'
        return x
      
    def initialize_fields(self, num_eq_fields):
        for pos in range(num_eq_fields):
            field_obj = Field(pos)
            self.equation_fields.append(field_obj)
        # self.process_feedback()
        return
                
    def combine_and_update(self, list1, list2):
        temp = []
        for item in list1:
            for element in list2:
                temp.append(item+element)
        return temp
    
    def generate_equation_set(self, num_eq_fields, input_collection):
        """
        Genereate equation based on available entries in input set - which is - combining 
        numbers and operators for a field.
        
        initialize_fields() should be called before calling this function
        """ 
        temp1 = []
        temp2 = []
        temp1 = input_collection[0]
        for i in range(1, num_eq_fields):
            temp2 = input_collection[i]
            temp1 = self.combine_and_update(temp1, temp2)
        return temp1
        
    def validate_equation(self, equation):
        """
        Check if an equation is valid
            1. Equation should not start with Operator or '0' and should not end with Operator
            2. Equation should contain operator (Cannot be just a number)
            3. No Consecutive operators
            4. Evaluate equation and remove not int or invalid equations (division by 0)
        """
        flag = False
        # 1. Equation should not start with Operator or '0' and should not end with Operator
        if equation[0] in self.operators or equation[-1] in self.operators:
            return flag
        
        # 2. Equation should contain operator (Cannot be just a number)
        opr_flag = False
        for i in equation: 
            if i in self.operators:
                opr_flag = True
                break
        if opr_flag is False:
            return flag
        
        
        # 3. No Consecutive operators
        opr_position = []
        k = 0
        for i in equation: 
            if i in self.operators:
                opr_position.append(k)
            k = k + 1
                
        if len(opr_position)>0:
            for entry in opr_position:
                if entry+1 in opr_position:
                    return flag
        
        nums_in_eq = re.split(self.operator_regex, str(equation))
        for num in nums_in_eq:
            if num[0]=='0':
                return flag
        
        
        # 4. Evaluate equation and remove not int or invalid equations (division by 0)
        ans = None
        try :
            ans = eval(equation)
        except:
            return flag
        if type(ans) is not int:
            return flag
        if ans<0:
            return flag
        
        return True
                
    def filterout_invalid(self):
        # if debug is True:print('Filtering out invalid entries')
        res = list(map(self.validate_equation, self.equation_set))
        false_index = [i for i, x in enumerate(res) if not x]
        self.equation_set = np.delete(self.equation_set, false_index).tolist()
        return
    
    def filterout_invalid2(self):
        # res = list(map(self.validate_equation, self.equation_set))
        # false_index = [i for i, x in enumerate(res) if not x]
        # self.equation_set = np.delete(self.equation_set, false_index).tolist()
        size = self.length
        self.equation_set = [x for x in self.equation_set if len(x)==size]
        
        false_index = []
        for eq_index in range(len(self.equation_set)):
            for field_index in range(self.length):
                element = self.equation_set[eq_index][field_index]
                # num = self.equation_fields[field_index].numbers
                # opr = self.equation_fields[field_index].operators
                input_set = self.equation_fields[field_index].input_set
                # if element not in num or element not in opr:
                # print(element, input_set)
                if element!=self.equals and element not in input_set:
                    false_index.append(eq_index)
                    break
        self.equation_set = np.delete(self.equation_set, false_index).tolist()
        return

    def process_feedback(self):
        """
        1. Remove barred entries from input set of all fields
        2. Handle fixed entries by removing everything else from the input set
        3. For entries in shuffle, Remove these from the input set of respective fields, \
            Scoring should take care of including these in subsequent submission
        """
        if len(self.barred)>0:
            for item in self.barred:
                for field in self.equation_fields:
                    if item in field.numbers:
                        field.numbers.remove(item)
                    elif item in field.operators:
                        field.operators.remove(item)
                    else:
                        pass
                        # if debug is True:print("!!!!!!!! Something went wrong1 !!!!!!!!")
                        # if debug is True:print("The identified value is not in the input set of the field. \
                        #       Please debug")
                        # if debug is True:print(field.operators)
                        # if debug is True:print(field.numbers)
                        # if debug is True:print(item)
                        # sys.exit()

        if len(self.found)>0:
            for k, v in self.found.items():
                if v in self.equation_fields[k].numbers:
                    self.equation_fields[k].numbers = [v]
                    self.equation_fields[k].operators = []
                    self.equation_fields[k].is_fixed = True
                elif v in self.equation_fields[k].operators:
                    self.equation_fields[k].numbers = []
                    self.equation_fields[k].operators = [v]
                    self.equation_fields[k].is_fixed = True
                    
                else:
                    pass

                if v==self.equals:
                    #  Everything else should be an invalid config.. /
                    #  k --> is the only valid config
                    self.found_valid_config = k
                    self.equation_fields[k].numbers = []
                    self.equation_fields[k].operators = [self.equals]
                    self.equation_fields[k].is_fixed = True
                    for i in range(k+1, self.length):
                        self.equation_fields[i].operators = []
                          
        if len(self.shuffle)>0:
            for k, v in self.shuffle.items():
                if v in self.equation_fields[k].numbers:
                    self.equation_fields[k].numbers.remove(v)
                    # if debug is True:print('removing')
                elif v in self.equation_fields[k].operators:
                    self.equation_fields[k].operators.remove(v)
                    # if debug is True:print('removing1')
                else:
                    pass

        # for f in self.equation_fields:
        #     f.input_set = f.numbers+f.operators
        #     if debug is True:print(f.input_set)
        return self.equation_fields

    def generate_score(self, equation):
        """
        Generates a score favouring below criterias
        1. Equation must include entries which are in the suffle set
        2. Novelty score - For entries/positions which are not fixed, entries \
            must be include Newer Elements to gain more knowledge of the answer and reduce
            available options in less iterations.
        """
        copy_eq = equation
        if len(self.submissions)>0:
            prev_submission = self.submissions[-1]
        else:
            prev_submission = []
        must_include = list(self.shuffle.values()) # Need to take care of the matching count
        fixed_indexes = list(self.found.keys()) # Ignore these positions when scoring/any comparison 
        copy_eq = np.delete(list(copy_eq), fixed_indexes).tolist()

        already_fixed = [x.index for x in self.equation_fields if x.is_fixed is True]
                
        score = {}
        itr = 0

        for i in equation:
            if i in already_fixed:
                score[i] = 10000
                continue
            else:
                subject = i
                if subject in must_include:
                    score[i] = 1000  
                    must_include.remove(subject)
                elif subject in prev_submission:
                    score[i] = 0
                elif copy_eq.count(subject)>1:
                    score[i] = 10 
                else:
                    score[i] = 100
        final_score = sum(list(score.values()))
        return final_score
    
    def selector(self):
        scores = list(map(self.generate_score, self.equation_set))
        max_score = max(scores)
        max_index = scores.index(max_score)
        selection = self.equation_set[max_index]
        if debug is True:print("Total Valid Equation:", len(self.equation_set),\
                               "Score Max = ", max_score,"Index: ", max_index,\
                               "Equation : ", selection)
        return selection
    
    def complete_equation(self, equation):
        updated_eq = equation
        try:
            output = eval(equation)
            updated_eq = equation+'='+str(output)
        except:
            if debug is True:print('Invalide equation, eval() failing. Please check: ', equation)
        return updated_eq

    def complete_equation_set(self):
        # if debug is True:print('Completing equation')
        self.equation_set = list(map(self.complete_equation, self.equation_set))
    
class Game():
    def __init__(self, answer_equation):
        # super().__init__()
        self.answer = answer_equation
        self.entries = []
        self.index = 0
    
    def submit(self, entry):
        self.entries.append(entry)
        feedback_obj = self.generate_feedback(entry)
        return feedback_obj
        
    def generate_feedback(self, submission):
        self.index = 0
        feedback_obj = Feedback()
        feedback_obj.submissions = self.entries
        for element in list(submission):
            if element==self.answer[self.index]:
                feedback_obj.found[self.index] = element
            elif element in self.answer:
                feedback_obj.shuffle[self.index] = element
            else:
                feedback_obj.barred.append(element)
            self.index = self.index + 1
        
        if len(feedback_obj.shuffle)>0:
            for k, v in feedback_obj.shuffle.items():
                if v == '=':
                    # k will be the index of = which is invalid
                    # k-1 will be the last field of eqn hence eqn length with be k
                    # invalid config --> (k,length-k-1)
                    feedback_obj.invalid_config.append(k)
        
        return feedback_obj
            
if __name__ == '__main__':
    # ANSWER = '12-7*1=5'
    # ANSWER = '12-1-9=2'
    # ANSWER = '1032*0=0'
    # ANSWER = '11-8-1=2'
    # ANSWER = '10+12=22'
    ANSWER = '10+23=33'
    length = len(ANSWER)
    
    if debug is True:print('!!!! Starting Game !!!!')
    
    game = Game(ANSWER)
    eq = Equation(length)
    
    headstart = 0
    
    # Uncomment if you want to start with Pre defined equation 
    sub0 = eq.equation_preset()
    feedback = game.submit(sub0)
    eq.update_feedback(feedback)
    headstart = 1
    
    for i in range(headstart, 50):
        sub = eq.execute()
        if debug is True:print('\nSubmission',i+1, sub)
        if sub==ANSWER:
            if debug is True:print('!!!!! Hurray Found answer in ',i+1,' iterations')
            break
        feedback = game.submit(sub)
        eq.update_feedback(feedback)

    
    
    