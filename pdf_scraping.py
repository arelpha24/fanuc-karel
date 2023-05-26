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
            function_name = re.sub(r' Built-In Procedure$', '', function_name).replace(' iRVision', '')
            functions.append({"name": function_name, "parameters": [], "syntax":""})
            last_function_name = function_name
        elif "Built-In Function" in line:
            function_name = re.sub(r' Built-In Function$', '', function_name).replace(' iRVision', '')
            functions.append({"name": function_name, "parameters": [], "syntax":""})
            last_function_name = function_name
        elif "Built-In Routine" in line:
            function_name = re.sub(r' Built-In Routine$', '', function_name).replace(' iRVision', '')
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

            if re.match(r'^\[(in|out|in,out)\]\s*\w+\s*:\s*.+$', line):
                parameter_parts = re.split(r'\s*:\s*', line, maxsplit=1)
                parameter = parameter_parts[0].strip()
                parameter_type = re.findall(r'\[(.*?)\]', parameter)[0]
                parameter_name = re.findall(r'\]\s*(\w+)', parameter)[0]
                data_type = parameter_parts[1].strip()

                func["parameters"].append({
                    "name": parameter_name,
                    "parameter_type": parameter_type,
                    "data_type": data_type
                })
                            
                           
for function in functions:
    syntax_exported = function['name'] + '(' +','.join(parameter["name"] for parameter in function["parameters"]) + ')'
    syntax_from_manual = function['syntax'].replace(" ", "")
    syntax_from_manual = syntax_from_manual.replace(chr(32), "").replace("<", "").replace(">", "")
    if syntax_exported != syntax_from_manual:
        print("Syntax error detected, syntax from manual:" )
        print(syntax_from_manual, 'syntax_from_manual')
        print(syntax_exported, 'syntax_exported')
        print()

    
                            
# Write to JSON file
with open('karelFunctions.json', 'w') as json_file:
    json.dump(functions, json_file, indent=4)
