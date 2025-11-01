# Line editor initally crafted by minimax AI to resemble DOS edlin
import os
import sys
try:
    from pydos_ui import input
except:
    pass

class EdlinEditor:
    def __init__(self):
        self.lines = []
        self.filename = ""
        self.current_line = 1
        self.modified = False
        
    def run(self, filename=""):
        print("Type ? for help")
        
        self.filename = self._open_text(filename)
        
        while True:
            try:
                cmd = input(": ").strip()
                if not cmd:
                    self.display_and_edit([self.current_line])
                    self.current_line = min(self.current_line + 1, len(self.lines))
                    continue
                    
                # Parse command - check for line numbers and line ranges at the beginning
                parsed_cmd = self.parse_command(cmd)
                if not parsed_cmd:
                    continue
                    
                cmd_type = parsed_cmd[0]
                lrange = parsed_cmd[1]
                
                if cmd_type == '?':
                    self.show_help()
                elif cmd_type == 'q':
                    if self.check_save():
                        break
                elif cmd_type == 'w':
                    if lrange:  # w [filename]
                        self.filename = lrange
                    if not self.filename:
                        self.filename = input("Enter filename: ").strip()
                    if self.filename:
                        self.write_file(self.filename)
                elif cmd_type == 'e':
                    filename = lrange if lrange else self.filename
                    if filename:
                        self.filename = filename
                        self.write_file(self.filename)
                        print("Exiting...")
                        break
                    else:
                        print("No filename specified")
                elif cmd_type in ['l','r','s']:
                    self.process_range(parsed_cmd)
                elif cmd_type == 'a':
                    count = lrange if lrange else None
                    self.append_lines(count)
                elif cmd_type == 'i':
                    insert_line = lrange if lrange else self.current_line
                    self.insert_line(insert_line)
                elif cmd_type == 'd':
                    self.delete_lines(lrange)
                elif cmd_type == 'o':
                    filename = lrange if lrange else None
                    self.open_file(filename)
                elif cmd_type == '.':
                    self.display_and_edit(lrange)
                    
            except KeyboardInterrupt:
                print("\n")
                if self.check_save():
                    break
            except EOFError:
                if self.check_save():
                    break
                
        print("Goodbye!")
    
    def parse_command(self, cmd):
        """Parse command to extract line ranges and command type"""
        cmd = cmd.strip()
        
        # Special case: just a number (display and edit)
        if cmd.isdigit():
            line_num = int(cmd)
            if 1 <= line_num <= len(self.lines) or line_num == len(self.lines) + 1:
                return ('.',(line_num, line_num), None)
            else:
                print(f"Line {line_num} does not exist. Total lines: {len(self.lines)}")
                return None
        
        # Check for line range at the beginning
        if self.extract_range(cmd):
            cmd_without_range = cmd[self.extract_range(cmd)[1]:].strip()
            
            # Enter without command
            if not cmd_without_range:
                return ('.',self.extract_range(cmd)[0], None)
            
            first_char = cmd_without_range[0] if cmd_without_range else None
            
            if first_char in ['l','d']:
                return (first_char, self.extract_range(cmd)[0], None)
            elif first_char in ['a','i']:
                return (first_char, self.extract_range(cmd)[0][0], None)
            elif first_char in ['r','s']:
                rest = cmd_without_range[1:]
                return (first_char, self.extract_range(cmd)[0], rest)
            elif cmd_without_range.startswith('?r') or cmd_without_range.startswith('?s'):
                rest = cmd_without_range[2:]
                return (cmd_without_range[1],self.extract_range(cmd)[0], '?' + rest)
            else:
                print(f"Unknown command: {first_char}")
                return None
        
        # No line range - check for commands
        # Handle confirmation prefix for replace and search
        if cmd.startswith('?r') or cmd.startswith('?s'):
            rest = cmd[2:]
            return (cmd[1], None, '?' + rest)
        
        first_char = cmd[0]
        
        if first_char in ['l','a','i','q','?']:
            return (first_char, None, None)
        elif first_char == 'd':
            print("Usage: [start],[end] d")
            return None
        elif first_char in ['r','s']:
            rest = cmd[1:].strip()
            return (first_char, None, rest)
        elif first_char in ['w','e','o']:
            rest = cmd[1:].strip()
            return (first_char, rest, None)
        else:
            print(f"Unknown command: {first_char}")
            return None
    
    def _manual_match(self, end_part):
        i = 0
        n = len(end_part)

        # 1. Capture leading digits
        while i < n and end_part[i].isdigit():
            i += 1

        # Only counts as a match if digits exist (like \d+)
        if i == 0:
            return None

        digits = end_part[:i]
        
        # 2. Capture following whitespace
        spaces = ''
        while i < n and end_part[i].isspace():
            spaces += end_part[i]
            i += 1

        # 3. Capture the remainder
        remainder = end_part[i:]

        return digits, spaces, remainder

    def extract_range(self, cmd):
        """Extract line range from beginning of command"""
        cmd = cmd.strip()
        
        # Check for range [start],[end] followed by command (with or without space)
        if ',' in cmd:
            parts = cmd.split(',', 1)
            try:
                start = int(parts[0].strip())
                end_part = parts[1].strip()
                
                # Find where the range ends and command begins
                # Look for first non-digit character
                match = self._manual_match(end_part)
                if match:
                    end_line = int(match[0])
                    space_part = match[1]
                    remaining = match[2]
                    
                    range_str = f"{start},{end_line}"
                    
                    return ((start, end_line),len(range_str) + len(space_part))
            except (ValueError, IndexError):
                pass
        
        # Check for single line number followed by command (with or without space)
        match = self._manual_match(cmd)
        if match:
            line_num = int(match[0])
            space_part = match[1]
            remaining = match[2]
            
            return ((line_num, line_num),len(match[0]) + len(space_part))
        
        return None

    def check_save(self):
        if self.modified:
            save = ''
            while save not in ['y','yes','n','no']:
                save = input("Text modified. Save before quitting? (y/n): ").lower().strip()
            if save[0] == 'y':
                if not self.filename:
                    filename = input("Enter filename: ").strip()
                    if filename:
                        self.filename = filename
                if self.filename:
                    self.write_file(self.filename)
                else:
                    print("Cannot save: no filename specified")
                    return False
        return True
    
    def show_help(self):
        print("\nEDLIN Commands:")
        print("  [#]                   - Display and edit line")
        print("  [#][,#]l              - List lines")
        print("  a                     - Append lines (type 'END' to finish)")
        print("  [#]a                  - Append specified number of lines")
        print("  [#]i                  - Insert before line number")
        print("  [#][,#]d              - Delete line range")
        print("  [#][,#][?]r/old/new/  - Replace string [?] for confirmation")
        print("  [#][,#][?]s<text>     - Search for <text> [?] for confirmation")
        print("  w [filename]          - Write to file")
        print("  o / o [filename]      - Open file")
        print("  e [filename]          - Exit and write to file")
        print("  q                     - Quit")
        print("  ?                     - Show this help")
        print("\n[#][,#] specifies either single line # or start,end range")
        print("If a line number or range is not specified, the current line will be used")
        print("Note: * indicates current line pointer")
    
    def display_and_edit(self, lrange):
        """Display a line and allow editing"""
        line_num = lrange[0]
        
        if 1 <= line_num <= len(self.lines):
            self.current_line = line_num
            print(f"{line_num}: {self.lines[line_num-1]}")
            
            new_text = input(f"{line_num}: ").strip()
            
            # If user just pressed enter, keep existing line
            if new_text:
                self.lines[line_num-1] = new_text
                self.modified = True
                print(f"Line {line_num} updated")
        elif line_num == len(self.lines) + 1:
            # Adding a new line at the end
            self.current_line = line_num
            new_text = input(f"{line_num}: ").strip()
            if new_text:
                self.lines.append(new_text)
                self.modified = True
                print(f"Line {line_num} added")
        else:
            print(f"Line {line_num} does not exist. Total lines: {len(self.lines)}")
    
    def append_lines(self, count=None):
        """Append lines to the file"""
        if count:
            line_num = len(self.lines) + 1
            print(f"Appending {count} lines:")
            
            for i in range(count):
                text = input(f"{line_num + i}: ")
                self.lines.append(text)
            
            self.modified = True
            self.current_line = len(self.lines)
            print(f"Appended {count} lines")
        else:
            print("Entering append mode. Type 'END' on a line by itself to finish:")
            line_num = len(self.lines) + 1
            
            appended = 0
            while True:
                text = input(f"{line_num}: ").strip()
                if text.upper() == "END":
                    break
                self.lines.append(text)
                line_num += 1
                appended += 1
                self.modified = True
                
            self.current_line = len(self.lines)
            print(f"Appended {appended} lines")
    
    def insert_line(self, insert_line):
        """Insert lines before the specified line"""
        print(f"Inserting at line {insert_line}. Type 'END' to finish:")
        new_lines = []
        line_num = insert_line
        self.current_line = insert_line
        
        while True:
            text = input(f"{line_num}: ").strip()
            if text.upper() == "END":
                break
            new_lines.append(text)
            line_num += 1
        
        if new_lines:
            # Insert at the specified position (before the line)
            insert_pos = max(0, min(insert_line - 1, len(self.lines)))
            for i, line in enumerate(new_lines):
                self.lines.insert(insert_pos + i, line)
            
            self.modified = True
            print(f"Inserted {len(new_lines)} lines")
    
    def delete_lines(self, line_range):
        """Delete lines in range"""
        start, end = line_range
        
        if 1 <= start <= end <= len(self.lines):
            deleted_count = end - start + 1
            del self.lines[start-1:end]
            self.modified = True
            print(f"Deleted {deleted_count} lines")
            
            if self.current_line > end:
                self.current_line -= deleted_count
            elif start <= self.current_line <= end:
                self.current_line = max(1, start)
            elif self.current_line > start:
                self.current_line = start
        else:
            print("Invalid line range")
    
    def process_range(self, parsed_cmd):
        """Perform Replace, Search or List functions"""

        if not self.lines:
            print("File is empty")
            return

        cmd = parsed_cmd[0]
        lrange = parsed_cmd[1]
        args = parsed_cmd[2]
        if args is None:
            args = ''
        
        # Determine range
        if lrange:
            start, end = lrange
        else:
            if cmd == 'l':
                start = 1
                end = len(self.lines)
            else:
                start = end = self.current_line
        
        start = max(1, min(start, len(self.lines)))
        end = max(start, min(end, len(self.lines)))

        # Check for confirmation prompt
        confirm = False
        if args.startswith('?'):
            confirm = True
            args = args[1:]

        if cmd in ['s','r']:
            if not args:
                print(f"Usage: [range] {'s<text>' if cmd == 's' else 'r/old/new/'}")
                return

        if cmd == 's':        
            # Search text is everything after 's' (no delimiters needed)
            search_text = args.rstrip()
            new_text = None
            
            if not search_text:
                print("No search text specified")
                return
        elif cmd == 'r':
            # First character is separator
            separator = args[0]
            rest = args[1:]
            
            parts = rest.split(separator)
            if len(parts) < 3:
                print("Error: Need exactly 3 separators for replace command - Usage: [range] r/old/new/")
                return
            
            # Check if there are extra characters after the third separator
            third_sep_pos = len(parts[0]) + 1 + len(parts[1]) + 1
            remaining = args[third_sep_pos + 1:]
            if remaining.strip():
                print("Error: Extra characters after third separator - Usage: [range] r/old/new/")
                return

            search_text = parts[0]
            new_text = parts[1]

        _count = 0
        for i in range(start, end+1):
            if cmd == 'l':
                _count += 1
                if i == self.current_line:
                    print(f"{i}*: {self.lines[i-1]}")
                else:
                    print(f"{i} : {self.lines[i-1]}")
            elif cmd in ['s','r']:
                if search_text in self.lines[i-1]:
                    if confirm:
                        print(f"{i}: {self.lines[i-1]}")
                        response = ''
                        while response not in ['y','yes','n','no','e','end']:
                            if cmd == 's':
                                response = input(f"Continue search? (Yes/No): ").lower().strip()
                            else:
                                response = input(f"Replace '{search_text}' with '{new_text}'? (Yes/No/End): ").lower().strip()
                        
                        if response[0] == 'n':
                            if cmd == 's':
                                self.current_line = i
                                _count += 1
                                break
                        elif response[0] == 'y':
                            if cmd == 'r':
                                self.lines[i-1] = self.lines[i-1].replace(search_text, new_text)
                                self.modified = True
                            _count += 1
                            self.current_line = i
                        elif response[0] =='e':
                            if cmd == 's':
                                self.current_line = i
                                _count += 1
                            break
                    else:
                        _count += 1
                        self.current_line = i
                        if cmd == 's':
                            print(f"{i}: {self.lines[i-1]}")
                            break  # Only show first match in non-confirmation mode
                        else:
                            self.lines[i-1] = self.lines[i-1].replace(search_text, new_text)
                            self.modified = True

        if cmd in ['s','r']:
            if _count > 0:
                print(f"{'Found' if cmd == 's' else 'Replaced'} '{search_text}' {\
                    "with '" if cmd == 'r' else ""}{new_text if cmd == 'r' else ""}{\
                    "'" if cmd == 'r' else ""}in {_count} line(s)")
            else:
                print(f"'{search_text}' not found in specified range")

    def write_file(self, filename):
        """Write file to disk"""
        try:
            with open(filename, 'w') as f:
                for line in self.lines:
                    f.write(line + '\n')
            self.modified = False
            print(f"Written {len(self.lines)} lines to {filename}")
        except Exception as e:
            print(f"Error writing file: {e}")

    def _chkPath(self, tstPath):
        validPath = True

        if tstPath == []:
            validPath = True
        else:

            savDir = os.getcwd()

            for path in tstPath:
                if path == "":
                    os.chdir("/")

                elif os.getcwd() == "/" and path == "..":
                    validPath = False
                    break

                elif path == "." or path == "..":
                    os.chdir(path)

                elif path in os.listdir() and (os.stat(path)[0] & (2**15) == 0):
                    os.chdir(path)

                else:
                    validPath = False
                    break

            os.chdir(savDir)

        return(validPath)
    
    def _open_text(self, name):

        if name == "":
            name = input("Enter file name: ")

        aPath = name.split("/")
        newdir = aPath.pop(-1)

        self.lines = []
        if self._chkPath(aPath) and \
            newdir in os.listdir(name[0:len(name)-len(newdir)]) and \
            os.stat(name)[0] & (2**15) != 0:

            with open(name,"r") as f:
                for line in f:
                    self.lines.append(line.rstrip("\n\r"))
        else:
            print("Unable to open: "+name+". File not found.")
            name = ""

        return name

    def open_file(self, filename=None):
        """Open a file for editing"""
        if self.modified:
            save = ''
            while save not in ["y","yes","n","no"]:
                save = input("Current file is modified. Save before opening new file? (y/n): ").lower().strip()
            if save[0] =='y':
                if self.filename:
                    self.write_file(self.filename)
                else:
                    temp_filename = input("Enter filename to save current file: ").strip()
                    if temp_filename:
                        self.write_file(temp_filename)
                    else:
                        sure = ''
                        while sure not in ["y","yes","n","no"]:
                            sure = input("Current changes will be lost! Are you Sure? (y/n): ")
                        if sure[0] =="n":
                            print("Open file aborted")
                            return
        
        self.filename = self._open_text(filename)
    
def edlin(passedIn=""):
    editor = EdlinEditor()
    editor.run(passedIn)

if __name__ != "PyDOS":
    passedIn = ""

edlin(passedIn)
