from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from testclass import Keyword
from flashtext import KeywordProcessor
from docx import Document
import re
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from plyer import filechooser
import kivymd.icon_definitions





#CRUCIAL: plyer does not import with pyinstaller, used
#pyinstaller -F -w --hidden-import=plyer.platforms.plyer.FileChooser .\inter_kivy_mddatatable.py - this works, guess alternatives for other OS will also work
#program works as intended, barebones right now
#TODO:
#make pretty - colors, element size, padding, etc.
#export function - CSV

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
        one for the table visualisation (terminal_output) and for the buttons below it(right_side_buttons)
        """
        Window.size = (1280,800)
        self.window0 = BoxLayout()
        self.left_side = BoxLayout(orientation='vertical',size_hint=(.3,1))
        #entire left half is coded below
        self.window0.add_widget(self.left_side) #this is the entire left section
        
        self.text_field = Label(valign = 'top', text="[color=000000][b]the Keywords to your mother's cunt[/b]", 
                                font_size=24, markup=True)
        self.left_side.add_widget(self.text_field) #title label
        
        self.kw_label = Label(valign='bottom', text="[color=000000]Enter file with keywords list:", markup=True)
        self.left_side.add_widget(self.kw_label) #label for kw input

        
        self.kw_list = TextInput(text="kw_list_maybe.txt", multiline=False)
        self.left_side.add_widget(self.kw_list) #text input for kw list file

        self.kw_selection_button = Button(text="Select KW file")
        self.kw_selection_button.bind(on_release=self.select_kw_list_file)
        self.left_side.add_widget(self.kw_selection_button) #button for selecting a kw list file
        
        self.docx_label = Label(valign='bottom', text="[color=000000]Enter docx file to parse", markup=True)
        self.left_side.add_widget(self.docx_label) #label for docx input
        
        self.docx = TextInput(text = "new_doc.docx", multiline=False)
        self.left_side.add_widget(self.docx) #text input for docx file

        self.docx_selection_button = Button(text="Select docx file")
        self.docx_selection_button.bind(on_release=self.select_docx_file)
        self.left_side.add_widget(self.docx_selection_button) #button for selecting docx file

        self.parse_button = Button(valign = 'middle', text="Start KW parse", size_hint=(1,0.55), background_color=[255,0,255])
        self.parse_button.bind(on_release=self.main_parse)
        self.left_side.add_widget(self.parse_button) #parse button

        

        

        #entire right half is coded below
        self.true_right_side = BoxLayout(orientation='vertical', size_hint=(.7,1))
        self.window0.add_widget(self.true_right_side) #this is the entire right section
        self.right_side = ScrollView(size_hint=(1,.9), scroll_wheel_distance = 25)
        self.true_right_side.add_widget(self.right_side) #not entirely sure what this is, houses the terminal_output section
        
        self.terminal_output = MDDataTable(
            use_pagination=True,
            rows_num=50,
            column_data = [
            ("Keyword", dp(80)),
            ("Exact Matches", dp(30)),
            ("Partial Matches", dp(30)),
            ("Total Matches", dp(30))
        ]
        ) 
        self.right_side.add_widget(self.terminal_output) #this displays the final parsed data as a table
        
        self.right_side_buttons = BoxLayout(orientation='vertical', size_hint=(1,.1))
        self.true_right_side.add_widget(self.right_side_buttons) #section for the buttons on the right side

        self.table_button = Button(text="Post final table", size_hint=(1,0.2))
        self.table_button.bind(on_release=self.get_final_table)
        self.right_side_buttons.add_widget(self.table_button) #button that prints the table withe parsed data

     
        return self.window0

    def select_kw_list_file(self, *args):
        from plyer import filechooser
        file = filechooser.open_file(on_selection=self.selected_kw_list)
        if file == []:
            pass
        else:
            self.kw_list.text = file[0]
    
    def selected_kw_list(self, selection):
        return selection
    
    def select_docx_file(self, *args):
        from plyer import filechooser
        file = filechooser.open_file(on_selection=self.selected_docx_file)
        if file == []:
            pass
        else:
            self.docx.text=file[0]

    def selected_docx_file(self, selection):
        return selection

    def get_final_table(self, *args):
        self.terminal_output.row_data = []
        for i in Keyword.complete_data:
            self.terminal_output.add_row(
                (i.keyword, i.exact_match, i.partial_match, i.exact_match + i.partial_match)
            )

    def main_parse(self, *args):
        keyword_list = self.get_keywords_from_list()
        KW = self.pass_keywords_to_class(keyword_list)
        new_doc = self.word_document()
        formatted_doc = self.format(new_doc)
        self.exact_match_parse(formatted_doc, KW)
        self.partial_match_parse(formatted_doc, keyword_list, KW)
        Keyword.complete_data = KW
        
    def get_keywords_from_list(self): #txt file which passed and every line is extracted as a keyword
        list_file = self.kw_list.text
        keyword_list = []
        with open(list_file) as file:
            file = file.readlines()
            for line in file:
                keyword_list.append(line.strip())
        return keyword_list


    def pass_keywords_to_class(self, keyword_list):
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
    
    def format(self, new_doc):
        with open(new_doc, 'r') as original_file, open('formatted_temp.txt', 'w') as formatted_file:
            for line in original_file.readlines():
                clean = re.compile('<.*?>')
                line = re.sub(clean,'', line)
                line = re.sub("[,.?:']",'', line)
                line = re.sub("\[[0-9]\]", '', line)
                formatted_file.write(line)
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