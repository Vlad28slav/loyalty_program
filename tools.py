"functions for application"
def validation_program(program: str):
    all_programs= []
    prog_parsed = program.split(',')
    for two_vals in prog_parsed:
        temp = two_vals.split(' ')
        temp = [x for x in temp if x != '']
        if len(temp) != 2:
            return 0
        try:
            first = int(temp[0])
            second =int(temp[1])
            all_programs.append([str(first), str(second)])
        except ValueError:
            return 0

    res = list(map(','.join, all_programs))
    prog = "!".join(res)
    return prog
