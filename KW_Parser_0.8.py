from flashtext import KeywordProcessor
from docx import Document
import re
import regex as reg
import os
from plyer import filechooser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
import kivymd.icon_definitions
from kivymd.uix.dialog import MDDialog
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem
from kivymd.uix.boxlayout import MDBoxLayout



"""
EXPORT WITH:
pyinstaller -F -w --hidden-import=plyer.platforms.win.filechooser --hidden-import=kivymd.uix.dropdownitem .\KW_Parser_0.8.py
"""

#TODO:
#program causes memory leak on resize and reset, because fuck you 
#make pretty - colors, element size, padding, etc.
#link parsing method, collect all <a> tags and the their contents
#paragraph length method, if paragraph > 70 raise issue
#tabs has worked out for this. Now it's only a matter of introducing the rest of the desired features - paragraph length, links list

class Bolding_Errors:

    all_bolding_errors = []
    def __init__(self, line_string, bolding_error):
        self.line_string = line_string
        self.bolding_error = bolding_error
        
    ...

class Keyword:
    final_table = ""
    complete_data = []
    def __init__(self, keyword, exact_match=0, partial_match=0) -> None:
        self.keyword = keyword
        self.exact_match = exact_match
        self.partial_match = partial_match
        
    def __str__(self):
        return str([self.keyword, self.exact_match, self.partial_match])

class KeywordParser(MDApp): 
    def build(self):
        """
        A little explanation:
        the app has a main window (window0), within it are located the different sections
        left_side is the left half of the scren, where you enter files for parsing
        the right half (true_right_side) houses two additional sections, 
        one for the table visualisation (keyword_table) and for the buttons below it(right_side_buttons)
        """
        Window.size = (1300,1100)
        self.window0 = BoxLayout()
        self.left_side = BoxLayout(orientation='vertical',size_hint=(.3,1), spacing=10, padding = 10)
        #entire left half is coded below
        self.window0.add_widget(self.left_side) #this is the entire left section
        
        self.text_field = MDLabel(text="[color=000000]Parse keywords with my blessing", 
                                font_size=24, markup=True,pos_hint={'center_x':0.5,'center_y':0.2}, 
                                size_hint=(1,0.2), font_style='H3')
        self.left_side.add_widget(self.text_field) #title label

        self.left_side_input = BoxLayout(orientation='vertical', size_hint=(1, 0.7))
        self.left_side.add_widget(self.left_side_input) #element that houses all of the input elements, text fields and their buttons

        #self.kw_label = MDLabel(text="[color=000000]Enter file with keywords list:", size_hint=(1,.2), pos_hint={'center_x':0.5,'center_y':1}, markup=True)
        #self.left_side_input.add_widget(self.kw_label) #label for kw input

        
        self.kw_list = MDTextField(hint_text="Enter file with keywords list", readonly=True)
        self.left_side_input.add_widget(self.kw_list) #text input for kw list file

        self.kw_selection_button = MDRaisedButton(text="Select KW file", md_bg_color='red',
                                                  pos_hint={'center_x':0.8,'center_y':0.8})
        self.kw_selection_button.bind(on_release=self.select_kw_list_file)
        self.left_side_input.add_widget(self.kw_selection_button) #button for selecting a kw list file
        
        #self.docx_label = MDLabel(text="[color=000000]Enter docx file to parse",size_hint=(1,.2), pos_hint={'center_x':0.5,'center_y':0.5}, markup=True)
        #self.left_side_input.add_widget(self.docx_label) #label for docx input
        
        self.docx = MDTextField(hint_text = "Enter .docx file to parse", readonly=True, size_hint=(1,.2))
        self.left_side_input.add_widget(self.docx) #text input for docx file

        self.docx_selection_button = MDRaisedButton(text="Select docx file",md_bg_color='red',
                                                    pos_hint={'center_x':0.8,'center_y':0.8})
        self.docx_selection_button.bind(on_release=self.select_docx_file)
        self.left_side_input.add_widget(self.docx_selection_button) #button for selecting docx file  

        self.parse_button = MDRaisedButton(text="Start KW parse", size_hint=(0.8,0.1), 
                                           md_bg_color='red',pos_hint={'center_x':0.5,'center_y':0.5})
        self.parse_button.bind(on_release=self.main_parse)
        self.left_side.add_widget(self.parse_button) #parse button

        
        #entire right half is coded below
        self.true_right_side = BoxLayout(size_hint=(.7,1))
        self.window0.add_widget(self.true_right_side) #this is the entire right section
        
        self.right_side = MDNavigationRail(MDNavigationRailItem
                                           (text="Home",
                                            icon="language-python",                                            
                                            on_press=self.home_button
                                            ),
                                            MDNavigationRailItem
                                           (text="Show table",
                                            icon="language-python",                                            
                                            on_press=self.show_table
                                            ),

                                            MDNavigationRailItem
                                           (text="Show boldings",
                                            icon="language-python",                                            
                                            on_press=self.show_bolding
                                            ),

                                            MDNavigationRailItem
                                           (text="Show table",
                                            icon="language-python",
                                            #on_press=self.show_table
                                            ),

                                            )
        self.true_right_side.add_widget(self.right_side) #not entirely sure what this is, houses the keyword_table section
        
        self.display_section = MDBoxLayout()
        self.true_right_side.add_widget(self.display_section)


        self.keyword_table = MDDataTable(
            #use_pagination=True,
            rows_num=150,
            column_data = [
            ("Keyword", dp(80)),
            ("Exact Matches", dp(30)),
            ("Partial Matches", dp(30)),
            ("Total Matches", dp(30))
        ]
        ) 
        
        self.bolding_view = MDLabel(markup=True,padding = 30)
        
        
        """        
        #below are right-side buttons 
        self.right_side_buttons = BoxLayout(orientation='horizontal', size_hint=(1,.1), spacing=20)
        self.true_right_side.add_widget(self.right_side_buttons) #section for the buttons on the right side

        self.table_button = MDRaisedButton(text="Post final table", md_bg_color='black', size_hint=(0.3,1),
                                           pos_hint={'center_x':0.5,'center_y':0.5})
        self.table_button.bind(on_release=self.get_final_table)
        self.right_side_buttons.add_widget(self.table_button)

        self.bolding_error_button = MDRaisedButton(text="Show bolding errors", size_hint=(0.3,1),
                                                   pos_hint={'center_x':0.5,'center_y':0.5})
        self.bolding_error_button.bind(on_release=self.show_bolding_errors)
        self.right_side_buttons.add_widget(self.bolding_error_button)

        self.reset_button = MDRaisedButton(text="Reset",size_hint=(0.3,1),pos_hint={'center_x':0.5,'center_y':0.5})
        self.reset_button.bind(on_release=self.program_reset)
        self.right_side_buttons.add_widget(self.reset_button) #button that reset the program's state, currently eats RAM like a motherfucker

        """     
        return self.window0
    
    def show_bolding(self, *args):

        self.display_section.clear_widgets()
        self.display_section.add_widget(self.bolding_view)
    def show_table(self, *args):

        self.display_section.clear_widgets()
        self.display_section.add_widget(self.keyword_table)
        
    def home_button(self, *args):
        self.display_section.clear_widgets()
    def get_bolding(self, *args):
        if Bolding_Errors.all_bolding_errors:
            
            error_messages = ''
            for i in Bolding_Errors.all_bolding_errors:
                
                error = f'[b]{i.bolding_error}[/b]: {i.line_string}\n'
                error_messages+=error
            self.bolding_view.text = error_messages
            
        else:
            self.bolding_view.text = "No bolding errors found"            
            

        

    def program_reset(self, *args):
        self.root.clear_widgets()
        self.stop()
        self.__init__()
        return self.run()
        
    #below is file selection fuction
    def select_kw_list_file(self, *args):
        from plyer import filechooser
        file = filechooser.open_file(on_selection=self.selected_kw_list, filters=['*.txt'])
        if file == []:
            pass
        else:
            self.kw_list.text = file[0]
    
    #below is file selection fuction
    def selected_kw_list(self, selection):
        return selection
    
    #below is file selection fuction
    def select_docx_file(self, *args):
        from plyer import filechooser
        file = filechooser.open_file(on_selection=self.selected_docx_file, filters=['*.docx'])
        if file == []:
            pass
        else:
            self.docx.text=file[0]

    #below is file selection fuction
    def selected_docx_file(self, selection):
        return selection

    def get_final_table(self, *args): #this function adds the parsed data to the KW table
        
        for i in Keyword.complete_data:
            self.keyword_table.add_row(
                (i.keyword, i.exact_match, i.partial_match, i.exact_match + i.partial_match)
            )
        
        #self.table_button.md_bg_color='black'
        self.parse_button.md_bg_color='red'
    
    def main_parse(self, *args): #main function, runs required functions in order
        try:
            keyword_list = self.get_keywords_from_list()
            KW = self.pass_keywords_to_class(keyword_list)
            new_doc = self.word_document()
            formatted_doc = self.format(new_doc)
            self.exact_match_parse(formatted_doc, KW)
            self.partial_match_parse(formatted_doc, keyword_list, KW)
            Keyword.complete_data = KW
            del KW
            #self.table_button.md_bg_color='red'
            self.parse_button.md_bg_color='black'
            os.remove('formatted_temp.txt')
            os.remove('temp.txt')
            self.get_final_table()
            self.get_bolding()
        except FileNotFoundError:
            self.file_not_found_error = MDDialog(text="File not found")
            self.file_not_found_error.open()
        
    def get_keywords_from_list(self): #txt file which passed and every line is extracted as a keyword
        list_file = self.kw_list.text
        keyword_list = []
        with open(list_file) as file:
            file = file.readlines()
            for line in file:
                keyword_list.append(line.strip())
        return keyword_list


    def pass_keywords_to_class(self, keyword_list): #creates Keyword class instances and the variable that houses them
        KW = []
        for keyword in keyword_list:
            KW.append(Keyword(keyword))
        return KW

    def word_document(self):
        new_doc = open('temp.txt', 'w', errors='ignore')
        document = Document(self.docx.text)
        for i in document.paragraphs:
            new_doc.write(i.text + '\n')
        return 'temp.txt'
    
    def format(self, new_doc): #checks for bolding errors, then 
        with open(new_doc, 'r') as original_file, open('formatted_temp.txt', 'w') as formatted_file:
            bolding_errors=[]
            for line in original_file.readlines():
                if line == "\n" or line.startswith("<h") or line.startswith("<li"):
                    continue
                elif len(line.split(" "))<25:
                    continue
                elif line.count("<strong>") != line.count("</strong>"):
                    bolding_errors.append(Bolding_Errors(line, "Unmatched <strong> tags"))
                else:
                    pattern = r'<strong>.*?</strong>'
                    found_patterns = reg.findall(pattern, line, overlapped=True)
                    if len(found_patterns)<1:
                        bolding_errors.append(Bolding_Errors(line, "No boldings"))
                    elif len(found_patterns)>1:
                        bolding_errors.append(Bolding_Errors(line, "Too many boldings"))
                    else:
                        pass
                clean = re.compile('<.*?>')
                line = re.sub(clean,'', line)
                line = re.sub("[,.?:']",'', line)
                line = re.sub("\[[0-9]\]", '', line)
                formatted_file.write(line)
            Bolding_Errors.all_bolding_errors = bolding_errors
            del bolding_errors

        return 'formatted_temp.txt'    

    def exact_match_parse(self, formatted_file, KW): #
        
        formatted_document = open(formatted_file).read()
        keyword_processor = KeywordProcessor()
        for i in KW:
            keyword_processor.add_keyword(i.keyword)
        kw_found = keyword_processor.extract_keywords(formatted_document)
        for i in KW:
            i.exact_match += kw_found.count(i.keyword)

    def partial_match_parse(self, formatted_file, keyword_list, KW):
        kw_patterns = []
        for keyword in keyword_list:
            separated_kw = keyword.split(" ")
            kw_patterns.append('(?: |(?:(?: \w* )(?:\w* )?))'.join(separated_kw))
        with open(formatted_file, 'r') as file:
            file = file.read()
            for number, pattern in enumerate(kw_patterns):
                matches = re.findall(pattern, file, re.IGNORECASE)
                matches = [x.lower() for x in matches]                
                for match in matches:
                    if match in keyword_list:
                        continue
                    else:
                        KW[number].partial_match +=1

if __name__ == "__main__":
    KeywordParser().run()
