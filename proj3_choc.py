import sqlite3
import plotly.graph_objs as go


#################################
##### Name: Po-Tsun Kuo      ####
##### Uniqname: ptkuo        ####
#################################

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

DBNAME = 'choc.sqlite'

dictKV_list = {'bars':['country', 'region', 'sell', 'source', 'ratings', 'cocoa', 'bottom','top', 'barplot'],
                'companies':['country', 'region', 'ratings', 'cocoa', 'number_of_bars', 'bottom','top','barplot'],
                'countries':['region', 'sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'bottom','top','barplot'],
                'regions':['sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'bottom','top','barplot'],}


# Part 1: Implement logic to process user commands
def process_command(command):
    ''' search the result in the SQL database
    Parameters
    ----------
    string
            the string that use for search the wanted result
        
    Returns
    -------
    list
            the search result from the SQL database
    '''
    # step 1 parse the command input to generate desire list first
    parsed_list = find_parsed_string_list(command)
    #step 2 find the desire sql query_string
    sql_query_result = find_sql_string(parsed_list)
    #step 3 connect to sql and get the result 
    conn = sqlite3.connect('choc.sqlite')
    cur = conn.cursor()
    result = cur.execute(sql_query_result).fetchall()
    return result


def load_help_text():
    ''' read the help_text file
    Parameters
    ----------
    none
        
    Returns
    -------
    string
            all the content in the help.txt
    '''
    with open('Proj3Help.txt') as f:
        return f.read()


def find_parsed_string_list(input_string_from_user):
    ''' turn the user input into a list with specific format. 
        It will later be used to construct the SQL querty string
    Parameters
    ----------
    string
            string decidede by the user
    Returns
    -------
    list
            a list with specific format
    '''
    parsed_input_string_list = input_string_from_user.split(' ')
    # for bars
    if parsed_input_string_list[0] == "bars":
        default_bar_list = ['bars', 'none', 'sell', 'ratings', 'top', '10','none']
        for ele in parsed_input_string_list:
            if "=" in ele:
                default_bar_list[1] = ele
            elif "sell" in ele or "source" in ele:
                default_bar_list[2] = ele
            elif "ratings" in ele or "cocoa" in ele:
                default_bar_list[3] = ele
            elif "top" in ele or "bottom" in ele:
                default_bar_list[4] = ele
            elif "10" not in ele and  ele.isnumeric():
                default_bar_list[5] = ele
            elif "barplot" in ele:
                default_bar_list[6] = ele
        output_string_list = default_bar_list
        return output_string_list
    # for companies    
    elif parsed_input_string_list[0] == "companies":
        default_companies_list = ['companies', 'none', 'ratings', 'top', '10','none']
        for ele in parsed_input_string_list:
            if "=" in ele:
                default_companies_list[1] = ele
            elif "ratings" in ele or "cocoa" in ele or "number_of_bars" in ele:
                default_companies_list[2] = ele
            elif "top" in ele or "bottom" in ele:
                default_companies_list[3] = ele
            elif "10" not in ele and  ele.isnumeric():
                default_companies_list[4] = ele
            elif "barplot" in ele:
                default_companies_list[5] = ele    
        output_string_list = default_companies_list
        return output_string_list
    # for countries   
    elif parsed_input_string_list[0] == "countries":
        default_countries_list = ['countries', 'none','sell', 'ratings', 'top', '10','none']
        for ele in parsed_input_string_list:
            if "region=" in ele:
                default_countries_list[1] = ele
            if "sell" in ele or  "source" in ele:
                default_countries_list[2] = ele
            elif "ratings" in ele or "cocoa" in ele or "number_of_bars" in ele:
                default_countries_list[3] = ele
            elif "top" in ele or "bottom" in ele:
                default_countries_list[4] = ele
            elif "10" not in ele and  ele.isnumeric():
                default_countries_list[5] = ele
            elif "barplot" in ele:
                default_countries_list[6] = ele
        output_string_list = default_countries_list    
        return output_string_list
    # for regions   
    elif parsed_input_string_list[0] == "regions":
        default_regions_list = ['regions', 'sell', 'ratings', 'top', '10','none']
        for ele in parsed_input_string_list:
            if "sell" in ele or  "source" in ele:
                default_regions_list[1] = ele
            elif "ratings" in ele or "cocoa" in ele or "number_of_bars" in ele:
                default_regions_list[2] = ele
            elif "top" in ele or "bottom" in ele:
                default_regions_list[3] = ele
            elif "10" not in ele and  ele.isnumeric():
                default_regions_list[4] = ele
            elif "barplot" in ele:
                default_regions_list[5] = ele
        output_string_list = default_regions_list
        return output_string_list


def find_sql_string(desire_output_list):
    ''' constuct the query string for searching in the SQL database
    Parameters
    ----------
    list
            list with specific format
    Returns
    -------
    string
            a string with specific format
    '''
    # for bars
    if desire_output_list[0]== "bars":
        order_dict = {"ratings":"Rating ", "cocoa": "CocoaPercent", "top":"DESC", "bottom":"ASC"}
        query_string = '''SELECT B.SpecificBeanBarName, B.Company, cpy.EnglishName, B.Rating, B.CocoaPercent, bean.EnglishName
                        FROM Bars B JOIN Countries bean, Countries cpy 
                        ON B.BroadBeanOriginId=bean.Id AND B.CompanyLocationId = cpy.Id
                        '''
        if desire_output_list[1] == "none":
            key_word= f'ORDER BY B.{order_dict[desire_output_list[3]]} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
        elif desire_output_list[1].split("=")[0]== "country":
            if desire_output_list[2] == "sell":
                key_word = f'WHERE cpy.Alpha2="{desire_output_list[1].split("=")[1]}" ORDER BY B.{order_dict[desire_output_list[3]]} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
            elif desire_output_list[2] == "source":
                key_word = f'WHERE bean.Alpha2="{desire_output_list[1].split("=")[1]}" ORDER BY B.{order_dict[desire_output_list[3]]} {order_dict[desire_output_list[4]]}  LIMIT {desire_output_list[5]}'
        elif desire_output_list[1].split("=")[0]== "region":
            if desire_output_list[2] == "sell":
                key_word = f'WHERE cpy.Region="{desire_output_list[1].split("=")[1]}" ORDER BY B.{order_dict[desire_output_list[3]]} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
            elif desire_output_list[2] == "source":
                key_word = f'WHERE bean.Region="{desire_output_list[1].split("=")[1]}" ORDER BY B.{order_dict[desire_output_list[3]]} {order_dict[desire_output_list[4]]}  LIMIT {desire_output_list[5]}'
        query_words = query_string + key_word  


    # for comapnies
    order_dict = {"ratings":"Rating", "cocoa": "CocoaPercent", "number_of_bars": "SpecificBeanBarName", "top":"DESC", "bottom":"ASC"}
    if desire_output_list[0]== "companies":
        query_string_beginning = '''SELECT B.Company, cpy.EnglishName, '''
        query_string_midpoint2 = '''
                                FROM Bars B JOIN Countries cpy
                                ON B.CompanyLocationId = cpy.Id
                                '''
        if desire_output_list[2] == "ratings" or desire_output_list[2] == "cocoa":
            query_string_midpoint1 = f'AVG(B.{order_dict[desire_output_list[2]]})'
        elif desire_output_list[2] == "number_of_bars":
            query_string_midpoint1 = f'COUNT(B.{order_dict[desire_output_list[2]]})'
        if desire_output_list[1] == "none": 
            query_word = f'GROUP BY B.Company HAVING COUNT(B.Company) >4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[3]]} LIMIT {desire_output_list[4]}'
        elif desire_output_list[1].split("=")[0] == "country":
            query_word = f'WHERE cpy.Alpha2="{desire_output_list[1].split("=")[1]}" GROUP BY B.Company HAVING COUNT(B.Company) >4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[3]]} LIMIT {desire_output_list[4]}'
        elif desire_output_list[1].split("=")[0] == "region":
            query_word = f'WHERE cpy.Region="{desire_output_list[1].split("=")[1]}" GROUP BY B.Company HAVING COUNT(B.Company) >4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[3]]} LIMIT {desire_output_list[4]}'
        query_words = query_string_beginning + query_string_midpoint1+ query_string_midpoint2+ query_word 
    

    # for countries
    order_dict = {"ratings":"Rating", "cocoa": "CocoaPercent", "number_of_bars": "SpecificBeanBarName", "top":"DESC", "bottom":"ASC"}
    if desire_output_list[0]== "countries":
        query_string_midpoint2 = '''
                                FROM Bars B JOIN Countries bean, Countries cpy 
                                ON B.BroadBeanOriginId=bean.Id AND B.CompanyLocationId = cpy.Id
                                '''
        if desire_output_list[3] == "ratings" or desire_output_list[3] == "cocoa":
            query_string_midpoint1 = f'AVG(B.{order_dict[desire_output_list[3]]})'
        elif desire_output_list[3] == "number_of_bars":
            query_string_midpoint1 = f'COUNT(B.{order_dict[desire_output_list[3]]})'
        if desire_output_list[2] == "sell":
            query_string_beginning = '''SELECT cpy.EnglishName, cpy.Region,'''
            if desire_output_list[1] == "none":
                query_word = f'GROUP BY cpy.EnglishName HAVING COUNT(B.SpecificBeanBarName) >4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
            elif desire_output_list[1].split("=")[0] == "country":
                query_word = f'WHERE cpy.Alpha2="{desire_output_list[1].split("=")[1]}" GROUP BY cpy.EnglishName HAVING COUNT(B.SpecificBeanBarName)>4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
            elif desire_output_list[1].split("=")[0] == "region":
                query_word = f'WHERE cpy.Region="{desire_output_list[1].split("=")[1]}" GROUP BY cpy.EnglishName HAVING COUNT(B.SpecificBeanBarName)>4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
        elif desire_output_list[2] == "source":
            query_string_beginning = '''SELECT bean.EnglishName, bean.Region,'''
            if desire_output_list[1] == "none":
                query_word = f'GROUP BY B.BroadBeanOriginId HAVING COUNT(B.BroadBeanOriginId) >4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
            elif desire_output_list[1].split("=")[0] == "country":
                query_word = f'WHERE bean.Alpha2="{desire_output_list[1].split("=")[1]}" GROUP BY bean.Id HAVING COUNT(B.BroadBeanOriginId) >4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
            elif desire_output_list[1].split("=")[0] == "region":
                query_word = f'WHERE bean.Region="{desire_output_list[1].split("=")[1]}" GROUP BY bean.Id HAVING COUNT(B.BroadBeanOriginId)>4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[4]]} LIMIT {desire_output_list[5]}'
        query_words = query_string_beginning + query_string_midpoint1+ query_string_midpoint2+ query_word 
    # for regions
    order_dict = {"ratings":"Rating", "cocoa": "CocoaPercent", "number_of_bars": "SpecificBeanBarName", "top":"DESC", "bottom":"ASC"}
    if desire_output_list[0]== "regions":
        query_string_midpoint2 = '''
                                FROM Bars B JOIN Countries bean, Countries cpy 
                                ON B.BroadBeanOriginId=bean.Id AND B.CompanyLocationId = cpy.Id
                                '''
        if desire_output_list[2] == "ratings" or desire_output_list[2] == "cocoa":
            query_string_midpoint1 = f'AVG(B.{order_dict[desire_output_list[2]]})'
        elif desire_output_list[2] == "number_of_bars":
            query_string_midpoint1 = f'COUNT(B.{order_dict[desire_output_list[2]]})'
        
        if desire_output_list[1] == "sell":
            query_string_beginning = '''SELECT cpy.Region,'''
            query_word = f'GROUP BY cpy.Region HAVING COUNT(B.SpecificBeanBarName)>4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[3]]} LIMIT {desire_output_list[4]}'
        elif desire_output_list[1] == "source":
            query_string_beginning = '''SELECT bean.Region,'''
            query_word = f'GROUP BY bean.Region HAVING COUNT(B.BroadBeanOriginId)>4 ORDER BY {query_string_midpoint1} {order_dict[desire_output_list[3]]} LIMIT {desire_output_list[4]}'
        query_words = query_string_beginning + query_string_midpoint1+ query_string_midpoint2+ query_word 
    return query_words


def draw_barplot(query_result_list, cmd):
    ''' output the bar plot
    Parameters
    ----------
    list
            the SQL search result
    string
            the string that will be used to identify the cases
    Returns
    -------
    none

    '''
    xvals = []
    yvals = []
    cmd_type = find_parsed_string_list(cmd)
    if cmd_type[0] == "bars":
        for ele in query_result_list:
            xvals.append(ele[0])
            if cmd_type[3] == "cocoa":
                yvals.append(ele[4]) 
            elif cmd_type[3] == "ratings":
                yvals.append(ele[3])
        #basic_layout = go.Layout(title= "Result based on bars")
    elif cmd_type[0] == "companies":
        for ele in query_result_list:
            xvals.append(ele[0])
            yvals.append(ele[2])
        #basic_layout = go.Layout(title= "Result based on companies")
    elif cmd_type[0] == "countries":
        for ele in query_result_list:
            xvals.append(ele[0])
            yvals.append(ele[2])
        #basic_layout = go.Layout(title= "Result based on countries")
    elif cmd_type[0]== "regions":
        for ele in query_result_list:
            xvals.append(ele[0])
            yvals.append(ele[1])
        #basic_layout = go.Layout(title= "Result based on Regions")
    bar_data = go.Bar(x = xvals, y = yvals)
    if cmd_type[-3] == "top":
        basic_layout = go.Layout(title= f"Result based on {cmd_type[0]} descending order")
    elif cmd_type[-3] == "bottom":
        basic_layout = go.Layout(title= f"Result based on {cmd_type[0]} by ascending order")
    fig = go.Figure(data = bar_data, layout = basic_layout)
    fig.show()


def print_output(result_list, filter_string):
    ''' print the search result in specific format
    Parameters
    ----------
    list
            the SQL search result
    string
            the string that will be used to identify the case
    Returns
    -------
    none
    '''
    parsed_list = find_parsed_string_list(filter_string)
    outer_row = []
    for row in result_list:
        trimmed_row=[]
        for i in range(len(row)):
            if type(row[i]) == str and len(row[i]) > 13:
                trimmed_row.append('{:.<12}...'.format(row[i][0:12]))
            else:
                trimmed_row.append((row[i]))
        outer_row.append(trimmed_row)
    # for bars
    if parsed_list[0] == 'bars':
        for ele in outer_row:
            ele[4] = str('{:.0f}'.format((ele[4]*100)))+"%"
            print('{:<16}{:<16}{:<16}{:<5}{:<5}{:<5}'.format(ele[0],ele[1],ele[2],ele[3],ele[4],ele[5]))
    # for countries and companies
    if parsed_list[0] == 'countries':
        for ele in outer_row:
            if parsed_list[3] == "ratings" or parsed_list[3] == "cocoa":
                ele[2] = '{:.1f}'.format((ele[2]))
            elif parsed_list[3] == "number_of_bars":
                ele[2] = '{:.0f}'.format((ele[2]))
            print('{:<16}{:<16}{:<16}'.format(ele[0],ele[1],ele[2]))
    # for companies
    if parsed_list[0] == 'companies':
        for ele in outer_row:
            if parsed_list[2] == "ratings" or parsed_list[2] == "cocoa":
                ele[2] = '{:.1f}'.format((ele[2]))
            elif parsed_list[2] == "number_of_bars":
                ele[2] = '{:.0f}'.format((ele[2]))
            print('{:<16}{:<16}{:<16}'.format(ele[0],ele[1],ele[2]))
    # for regions
    if parsed_list[0] == 'regions':
        for ele in outer_row:
            if parsed_list[2] == "ratings" or parsed_list[2] == "cocoa":
                ele[1] = '{:.1f}'.format(ele[1])
            elif parsed_list[2] == "number_of_bars":
                ele[1] = '{:.0f}'.format(ele[1])
            print('{:<16}{:<16}'.format(ele[0],ele[1]))


def final_output(decide_string):
    ''' decide the output format and displace on screen
    Parameters
    ----------
    string 
            the input specify by user
    Returns
    -------
    none
    '''
    decide_element = find_parsed_string_list(decide_string)[-1]
    if decide_element == "none":
        result = process_command(decide_string)
        print_output(result, decide_string)
    elif decide_element == "barplot":
        result = process_command(decide_string)
        draw_barplot(result, decide_string)


# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    ''' the active interface between user and the program
    Parameters
    ----------
    none 
    Returns
    -------
    none
    '''
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')
        response1 = response.lower().strip(" ")
        if response1 == 'help':
            print(help_text)
            continue
        elif response1 == "exit":
            print("See you next time! Bye!")
            exit()
        elif len(response1) == 0:
            print(f"Command not recognized: {response}")
            continue
        elif response1.split(" ")[0] not in dictKV_list.keys():
            print(f"Command not recognized: {response}")
            continue
        elif len(response1.split(" ")) == 7 and response1.split(" ")[-2].isdigit() == False or len(response1.split(" ")) > 8:
            print(f"Command not recognized: {response}")
            continue
        elif 0 < len(response1.split(" ")) <= 7:
            if len(response1.split(" ")) == 1:
                result = process_command(response1.split(" ")[0])
            elif 1 < len(response1.split(" ")) < 8:
                count = 0
                condition = 0
                for ele in response1.split(" ")[1:]:
                    if ele.split('=')[0] in dictKV_list[response1.split(" ")[0]]:
                        count = count + 1
                if count == 0:
                    print(f"Command not recognized: {response}")
                for ele in response1.split(" ")[1:]:
                    if bool(ele.isnumeric()) == True:
                        condition = condition + 1
                if condition == 1:
                    if count == len(response1.split(" ")[1:])-1:
                        final_output(response)
                elif condition == 0:
                    if count == len(response1.split(" ")[1:]):
                        final_output(response)

# Make sure nothing runs or prints out when this file is run as a module/library

if __name__=="__main__":
    interactive_prompt()
