
import sys
import argparse
import ASDecompiler

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Decompiles and recompiles ED6 AS script files."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0"
    )
    
    parser.add_argument('file')
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
  
    if not args.file:
        raise Exception("ASDecompiler needs a file to decompile!")
    else:
        decompiled = ASDecompiler.decompile(args.file)
        ASDecompiler.to_py(decompiled)
    
        


if __name__ == "__main__":
    main()
