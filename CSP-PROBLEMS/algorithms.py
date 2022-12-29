import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class BacktrackingAlgorithmFCAC(Algorithm):
    @staticmethod
    def read_number(var_str: str):
        number: str = var_str[0:-1:1]
        return int(number)

    @staticmethod
    def is_consistent_assignment(var_str, value, help_tiles):
        width = len(help_tiles[0])
        number = BacktrackingAlgorithmFCAC.read_number(var_str)
        i = int(number / width)
        j = int(number % width)
        k = 0
        if var_str[-1] == 'h':
            while j <= int(number % width) + len(value) - 1:
                if help_tiles[i][j] is not True and help_tiles[i][j] is not False:
                    if value[k] != help_tiles[i][j]:
                        return False
                k += 1
                j += 1
        else:
            while i <= int(number / width) + len(value) - 1:
                if help_tiles[i][j] is not True and help_tiles[i][j] is not False:
                    if value[k] != help_tiles[i][j]:
                        return False
                k += 1
                i += 1
        return True

    @staticmethod
    def put_the_word(var_str, word, new_help_tiles):
        number = BacktrackingAlgorithmFCAC.read_number(var_str)
        width = len(new_help_tiles[0])
        i = int(number / width)
        j = int(number % width)
        k = 0
        if var_str[-1] == 'h':
            while j <= int(number % width) + len(word) - 1:
                new_help_tiles[i][j] = word[k]
                k += 1
                j += 1
        else:
            while i <= int(number / width) + len(word) - 1:
                new_help_tiles[i][j] = word[k]
                k += 1
                i += 1

    @staticmethod
    def get_arcs_dict_xy(variables: dict, width):
        arcs_dict = dict()
        for var in list(variables.keys()):
            y_list = []
            for var1 in list(variables.keys()):
                if var1 != var and BacktrackingAlgorithmFCAC.are_constrained(arcs_dict, var, var1, variables, width):
                    y_list.append(var1)
            arcs_dict[var] = y_list
        return arcs_dict

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        # moves_list = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}
        help_tiles = copy.deepcopy(tiles)
        solved_set = set()
        # make arcs dict
        arcs_dict = BacktrackingAlgorithmFCAC.get_arcs_dict_xy(variables, len(help_tiles[0]))
        # SAD IZMENITI KAD SE U BACKTRAC-u POZIVA ZA PRESEK,moze efikasnijenjer imam ovaj dict
        # calling backtrack
        self.backtrack_search_fcac(0, variables, domains, solution, help_tiles, solved_set, arcs_dict)
        # for move in moves_list:
        #   solution.append([move[0], move[1], domains])
        return solution

    @staticmethod
    def get_cells(var, variables: dict, width):
        cells = []
        number = BacktrackingAlgorithmFCAC.read_number(var)
        i = int(number / width)
        j = int(number % width)
        if var[-1] == 'h':
            for j in range(int(number % width), int(number % width) + variables[var]):
                cells.append([i, j])
        else:
            for i in range(int(number / width), int(number / width) + variables[var]):
                cells.append([i, j])
        return cells

    @staticmethod
    def get_index(var, width, i1, j1):
        number = BacktrackingAlgorithmFCAC.read_number(var)
        i = int(number / width)
        j = int(number % width)
        if var[-1] == 'h':
            return j1 - j
        else:
            return i1 - i

    @staticmethod
    def are_constrained(arcs_dict: dict, var_str, var, variables, width, help_tiles=None):
        var_str_set: list = BacktrackingAlgorithmFCAC.get_cells(var_str, variables, width)
        var_set: list = BacktrackingAlgorithmFCAC.get_cells(var, variables, width)
        cell = []
        intersection = []
        for k in range(len(var_set)):
            if var_set[k] in var_str_set:
                intersection.append(var_set[k])
        if len(intersection) == 1:
            i = intersection[0][0]
            j = intersection[0][1]
            if help_tiles is not None:
                cell = [BacktrackingAlgorithmFCAC.get_index(var, len(help_tiles[0]), i, j), help_tiles[i][j]]
                return cell
            else:
                return True

    @staticmethod
    def get_constraints(variables: dict, help_tiles):
        pass

    @staticmethod
    def update_domain(var, domains, cell):
        domains[var] = [word for word in domains[var] if len(word) > cell[0] and word[cell[0]] == cell[1]]

    @staticmethod
    def satisfies_constraints(x, val_x, y, val_y, help_tiles, variables, arcs_dict: dict):
        BacktrackingAlgorithmFCAC.put_the_word(x, val_x, help_tiles)
        cell = BacktrackingAlgorithmFCAC.are_constrained(arcs_dict, x, y, variables, len(help_tiles[0]), help_tiles)
        if val_y[cell[0]] == cell[1]:
            return True
        else:
            return False

    @staticmethod
    def arc_consistency(var_str, arcs_dict: dict, domain: dict, help_tiles, solved_set: set, variables):
        neighbours = [neighbour for neighbour in arcs_dict[var_str] if neighbour not in solved_set]
        all_arcs = []
        for var in neighbours:
            for var1 in arcs_dict[var]:
                if var1 not in solved_set:
                    all_arcs.append([var, var1])
        while all_arcs:
            x, y = all_arcs.pop(0)
            x_vals_to_delete = []
            for val_x in domain[x]:
                y_no_val = True
                for val_y in domain[y]:
                    if BacktrackingAlgorithmFCAC.satisfies_constraints(x, val_x, y, val_y, copy.deepcopy(help_tiles),
                                                                       variables, arcs_dict):
                        y_no_val = False
                        break
                if y_no_val:
                    x_vals_to_delete.append(val_x)
            if x_vals_to_delete:
                domain[x] = [v for v in domain[x] if v not in x_vals_to_delete]
                if not domain[x]:
                    return False
                for v in list(arcs_dict.keys()):
                    if v != x and BacktrackingAlgorithmFCAC.are_constrained(arcs_dict, v, x, variables,
                                                                            len(help_tiles[0])):
                        all_arcs.append([v, x])
        return True

    def backtrack_search_fcac(self, level, variables: dict, domains: dict, moves_list: list, help_tiles,
                              solved_set: set, arcs_dict: dict):
        if level == len(variables):
            return True
        # at this moment we can optimize how to choose next variable
        # at this moment we can optimize how to choose next value of the variable
        var_str = list(variables.keys())[level]
        for word in domains[var_str]:
            if BacktrackingAlgorithmFCAC.is_consistent_assignment(var_str, word, help_tiles):
                moves_list.append([var_str, domains[var_str].index(word), domains])
                solved_set.add(var_str)
                new_domain = copy.deepcopy(domains)
                new_help_tiles = copy.deepcopy(help_tiles)
                BacktrackingAlgorithmFCAC.put_the_word(var_str, word, new_help_tiles)
                flag = True
                for var in list(variables.keys()):
                    if var != var_str and var not in solved_set and flag:
                        width = len(help_tiles[0])
                        cell = BacktrackingAlgorithmFCAC.are_constrained(arcs_dict, var_str, var, variables, width,
                                                                         new_help_tiles)
                        if cell is not None and len(cell) == 2:
                            BacktrackingAlgorithmFCAC.update_domain(var, new_domain, cell)
                            if len(new_domain[var]) == 0:
                                flag = False
                if flag:
                    if not BacktrackingAlgorithmFCAC.arc_consistency(var_str, arcs_dict, new_domain,
                                                                     new_help_tiles, solved_set, variables):
                        flag = False
                if flag and self.backtrack_search_fcac(level + 1, variables, new_domain, moves_list, new_help_tiles,
                                                       solved_set, arcs_dict):
                    return True
            solved_set.remove(var_str)
        moves_list.append([var_str, None, domains])
        return False


class BacktrackingAlgorithmFC(Algorithm):

    @staticmethod
    def read_number(var_str: str):
        number: str = var_str[0:-1:1]
        return int(number)

    @staticmethod
    def is_consistent_assignment(var_str, value, help_tiles):
        width = len(help_tiles[0])
        number = BacktrackingAlgorithmFC.read_number(var_str)
        i = int(number / width)
        j = int(number % width)
        k = 0
        if var_str[-1] == 'h':
            while j <= int(number % width) + len(value) - 1:
                if help_tiles[i][j] is not True and help_tiles[i][j] is not False:
                    if value[k] != help_tiles[i][j]:
                        return False
                k += 1
                j += 1
        else:
            while i <= int(number / width) + len(value) - 1:
                if help_tiles[i][j] is not True and help_tiles[i][j] is not False:
                    if value[k] != help_tiles[i][j]:
                        return False
                k += 1
                i += 1
        return True

    @staticmethod
    def put_the_word(var_str, word, new_help_tiles):
        number = BacktrackingAlgorithmFC.read_number(var_str)
        width = len(new_help_tiles[0])
        i = int(number / width)
        j = int(number % width)
        k = 0
        if var_str[-1] == 'h':
            while j <= int(number % width) + len(word) - 1:
                new_help_tiles[i][j] = word[k]
                k += 1
                j += 1
        else:
            while i <= int(number / width) + len(word) - 1:
                new_help_tiles[i][j] = word[k]
                k += 1
                i += 1

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        # moves_list = []
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}
        help_tiles = copy.deepcopy(tiles)
        solved_set = set()
        # calling backtrack
        self.backtrack_search_fc(0, variables, domains, solution, help_tiles, solved_set)
        # for move in moves_list:
        #   solution.append([move[0], move[1], domains])
        return solution

    @staticmethod
    def get_cells(var, variables: dict, width):
        cells = []
        number = BacktrackingAlgorithmFC.read_number(var)
        i = int(number / width)
        j = int(number % width)
        if var[-1] == 'h':
            for j in range(int(number % width), int(number % width) + variables[var]):
                cells.append([i, j])
        else:
            for i in range(int(number / width), int(number / width) + variables[var]):
                cells.append([i, j])
        return cells

    @staticmethod
    def get_index(var, width, i1, j1):
        number = BacktrackingAlgorithmFC.read_number(var)
        i = int(number / width)
        j = int(number % width)
        if var[-1] == 'h':
            return j1 - j
        else:
            return i1 - i

    @staticmethod
    def are_constrained(var_str, var, variables, width, help_tiles):
        var_str_set: list = BacktrackingAlgorithmFC.get_cells(var_str, variables, width)
        var_set: list = BacktrackingAlgorithmFC.get_cells(var, variables, width)
        cell = []
        intersection = []
        for k in range(len(var_set)):
            if var_set[k] in var_str_set:
                intersection.append(var_set[k])
        if len(intersection) == 1:
            i = intersection[0][0]
            j = intersection[0][1]
            cell = [BacktrackingAlgorithmFC.get_index(var, len(help_tiles[0]), i, j), help_tiles[i][j]]
            return cell
        return None

    @staticmethod
    def update_domain(var, domains, cell):
        domains[var] = [word for word in domains[var] if len(word) > cell[0] and word[cell[0]] == cell[1]]
        # tmp = []
        # for word in domains[var]:
        #     if len(word) - 1 >= cell[0]:
        #         if word[cell[0]] == cell[1]:
        #             tmp.append(word)
        # domains[var] = tmp
        # return domains

    def backtrack_search_fc(self, level, variables: dict, domains: dict, moves_list: list, help_tiles, solved_set: set):
        if level == len(variables):
            return True
        
        # at this moment we can optimize how to choose next variable
        # at this moment we can optimize how to choose next value of the variable
        var_str = list(variables.keys())[level]
        for word in domains[var_str]:
            if BacktrackingAlgorithmFC.is_consistent_assignment(var_str, word, help_tiles):
                moves_list.append([var_str, domains[var_str].index(word), domains])
                solved_set.add(var_str)
                new_domain = copy.deepcopy(domains)
                new_help_tiles = copy.deepcopy(help_tiles)
                BacktrackingAlgorithmFC.put_the_word(var_str, word, new_help_tiles)
                flag = True
                for var in list(variables.keys()):
                    if var != var_str and var not in solved_set and flag:
                        width = len(help_tiles[0])
                        cell = BacktrackingAlgorithmFC.are_constrained(var_str, var, variables, width, new_help_tiles)
                        if cell is not None and len(cell) == 2:
                            # new_domain = BacktrackingAlgorithmFC.update_domain(var, new_domain, cell)
                            BacktrackingAlgorithmFC.update_domain(var, new_domain, cell)
                            if len(new_domain[var]) == 0:
                                flag = False
                if flag and self.backtrack_search_fc(level + 1, variables, new_domain, moves_list, new_help_tiles,
                                                     solved_set):
                    return True
            solved_set.remove(var_str)
        moves_list.append([var_str, None, domains])
        return False


class BacktrackingAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        solution = []
        moves_list = []
        # domains = {var: [word for word in words] for var in variables}
        domains = {var: [word for word in words if len(word) == variables[var]] for var in variables}
        help_tiles = copy.deepcopy(tiles)
        # call backtrack search
        self.backtrack_search(0, variables, domains, moves_list, help_tiles)
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution

    @staticmethod
    def read_number(var_str: str):
        number: str = var_str[0:-1:1]
        return int(number)

    @staticmethod
    def is_consistent_assignment(var_str, value, help_tiles):
        width = len(help_tiles[0])
        number = BacktrackingAlgorithm.read_number(var_str)
        i = int(number / width)
        j = int(number % width)
        k = 0
        if var_str[-1] == 'h':
            while j <= int(number % width) + len(value) - 1:
                if help_tiles[i][j] is not True and help_tiles[i][j] is not False:
                    if value[k] != help_tiles[i][j]:
                        return False
                k += 1
                j += 1
        else:
            while i <= int(number / width) + len(value) - 1:
                if help_tiles[i][j] is not True and help_tiles[i][j] is not False:
                    if value[k] != help_tiles[i][j]:
                        return False
                k += 1
                i += 1
        return True

    @staticmethod
    def put_the_word(var_str, word, new_help_tiles):
        number = BacktrackingAlgorithm.read_number(var_str)
        width = len(new_help_tiles[0])
        i = int(number / width)
        j = int(number % width)
        k = 0
        if var_str[-1] == 'h':
            while j <= int(number % width) + len(word) - 1:
                new_help_tiles[i][j] = word[k]
                k += 1
                j += 1
        else:
            while i <= int(number / width) + len(word) - 1:
                new_help_tiles[i][j] = word[k]
                k += 1
                i += 1

    def backtrack_search(self, level, variables: dict, domains: dict, moves_list: list, help_tiles):
        if level == len(variables):
            return True
        
        # at this moment we can optimize how to choose next variable
        # at this moment we can optimize how to choose next value of the variable
        var_str = list(variables.keys())[level]
        for word in domains[var_str]:
            if BacktrackingAlgorithm.is_consistent_assignment(var_str, word, help_tiles):
                moves_list.append([var_str, domains[var_str].index(word)])
                # new_domain = copy.deepcopy(domains)
                # new_domain[var_str] = [word]
                new_help_tiles = copy.deepcopy(help_tiles)
                BacktrackingAlgorithm.put_the_word(var_str, word, new_help_tiles)
                if self.backtrack_search(level + 1, variables, domains, moves_list, new_help_tiles):
                    return True
        moves_list.append([var_str, None])
        return False
