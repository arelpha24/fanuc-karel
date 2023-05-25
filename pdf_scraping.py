import json
import pdfplumber
import re

# List to store lines
lines = []

# Open the PDF
with pdfplumber.open('book.pdf') as pdf:
    # Loop over the range of pages
    for i in range(299, 680):  # Python uses 0-indexing, so we start at 300 for page 301
        page = pdf.pages[i]

        # Extract the text and split it into lines
        text = page.extract_text()
        for line in text.split('\n'):
            lines.append(line)

functions = []  # A list to store unique function names
last_function_name = ""
parameter_pattern = r"\[([\w,]+)\]\s+(\w+)\s+:\s+(\w+)"
# Now 'lines' contains all the lines from pages 300 to 310 that start with your enumeration pattern
for line in lines:
    # Check if the line starts with enumeration pattern
    if re.match(r'^A\.\d+\.\d+', line):
        # Substring the enumeration tag and "Built-In Procedure"
        function_name = re.sub(r'^A\.\d+\.\d+ ', '', line)
        if "Built-In Procedure" in line:
            function_name = re.sub(r' Built-In Procedure$', '', function_name)
            functions.append({"name": function_name, "parameters": [], "syntax":""})
            last_function_name = function_name
        elif "Built-In Function" in line:
            function_name = re.sub(r' Built-In Function$', '', function_name)
            functions.append({"name": function_name, "parameters": [], "syntax":""})
            last_function_name = function_name
        else:
            last_function_name = ""
    else:
        if last_function_name:
            if "Syntax:" in line:
                syntax = line
                syntax = syntax.replace("Syntax : ", "")
                syntax = syntax.replace("Syntax: ", "")
                syntax = syntax.replace("Syntax:", "")
                for func in functions:
                    if func["name"] == last_function_name:
                        func["syntax"] = syntax
            if "[in]" in line or "[out]" in line or "[in,out]" in line:
                parameter = re.match(parameter_pattern, line)
                if parameter:
                    for func in functions:
                        if func["name"] == last_function_name:
                            func["parameters"].append(
                                {
                                    "name": parameter.group(2),
                                    "parameter_type": parameter.group(1),
                                    "data_type": parameter.group(3)
                                }
                            )
                            
                            
for function in functions:
    syntax_exported = function['name'] + '(' +','.join(parameter["name"] for parameter in function["parameters"]) + ')'
    syntax_from_manual = function['syntax'].replace(" ", "")
    syntax_from_manual = syntax_from_manual.replace(chr(32), "")
    syntax_from_manual = syntax_from_manual.replace("<,group_no>", ",group_no")
    if syntax_exported != syntax_from_manual:
        print("Syntax error detected, syntax from manual: " + syntax_from_manual + ", syntax exported: " + syntax_exported)
        
    
                            
# Write to JSON file
with open('karelFunctions.json', 'w') as json_file:
    json.dump(functions, json_file, indent=4)
