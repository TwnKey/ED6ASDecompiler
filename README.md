# ED6ASDecompiler
 Tool used to decompile the ASXXXXXX._DT files from The Legend of Heroes: Trails in the Sky FC.
 
 The decompilation is not perfect (some operands might not be sized properly), maybe a few instructions could not be delimited properly too, 
 but the tool has been tested on all files and gives the identical binary content than the input.
 
 It's very ROUGH, something made to translate a few lines (The lines in battle typically at the beginning of the crafts, lines that no one is willing to make a whole decompiler for!)
 ![test](https://user-images.githubusercontent.com/69110695/171930208-c8ff18df-94cd-4f2e-ba28-f2764f574e2b.PNG)
 
 Some pointers might still be missing here and there, if you get a crash, please submit an issue and I will fix it. Adding one pointer is a matter of seconds once you find them.
 
 # How to use
 
 With Python installed (I have 3.9, no idea if it works for lower versions), just use the script like this:
 
 (PythonExePath) ASDT2py.py "AS00100 ._DT"
 
 It will generate a "AS00100 .py" file containing the decompiled script. Make your edits then recompile like this:
 
  (PythonExePath) "AS00100 ._py"
 
 # Custom encodings
   
 Typically fan translations are using the range 0xA1->0xCF to add new characters (since the game has variable spacing only for the 0x20->0x7F characters), and they have at least the full space/2. If you want to use those characters you can modify the map contained in "CustomEncoding.py" (something I made quickly, there is not even a decoding function right now)
   
 
 
