import sys

def fix_line(path, line_num, new_content):
    with open(path, 'r') as f:
        lines = f.readlines()
    if 1 <= line_num <= len(lines):
        lines[line_num - 1] = new_content + ('\n' if not new_content.endswith('\n') else '')
        with open(path, 'w') as f:
            f.writelines(lines)
        print(f'SUCCESS: Fixed line {line_num} in {path}')
    else:
        print(f'ERROR: Line {line_num} out of range for {path}')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 fix_line.py <path> <line_num> <new_content>')
    else:
        fix_line(sys.argv[1], int(sys.argv[2]), sys.argv[3])
