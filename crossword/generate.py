import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for v in self.domains:
            inconsistent_values = []
            for w in self.domains[v]:
                if v.length != len(w):
                    inconsistent_values.append(w)
            for iv in inconsistent_values:        
                self.domains[v].remove(iv)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        indexes = self.crossword.overlaps[x,y]
        rev = False
        lremove = []
        for w1 in self.domains[x]:
            el = True
            for w2 in self.domains[y]:
                if w1[indexes[0]] == w2[indexes[1]]:
                    el = False
            if el:
                lremove.append(w1)
        for it in lremove:
            self.domains[x].remove(it)
            rev = True        
        return rev        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            for v in self.domains:
                for n in self.crossword.neighbors(v):
                    if arcs == None:
                        arcs = []
                        arcs.append((v, n))
                    else:
                        if not ((v, n) in arcs) and not ((n, v) in arcs):
                            arcs.append((v, n))

        while len(arcs) > 0:
            a = arcs.pop(0)
            if self.revise(a[0], a[1]):
                if len(self.domains[a[0]]) == 0:
                    return False
                #for n in (self.crossword.neighbors(a[0])-set(a[1])):
                for n in self.crossword.neighbors(a[0]):
                    if n != a[1]:
                        arcs.append((a[0], n))
        return True            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """  
        for v in self.crossword.variables:
            if not v in assignment:
                return False      
            if not (assignment[v] in self.crossword.words):
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        ws = list(assignment.values())
        if len(ws) != len(set(ws)):
            return False

        for v in assignment:
            if v.length != len(assignment[v]):
                return False     
            for n in self.crossword.neighbors(v):
                indexes = self.crossword.overlaps[v,n]
                if assignment[v][indexes[0]] != assignment[n][indexes[1]]:
                    return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        list_values = self.domains[var]
        dict_restrict = dict(list_values, [0]*len(list_values))
        
        for val in dict_restrict:
            for neighbor in self.crossword.neighbors(var):
                if not (neighbor in assignment) and val in self.domains[neighbor]:
                    dict_restrict[val] += 1
        tup = sorted(dict_restrict.items(), key=lambda x:x[1])       
        list_ordered_values = []
        for t in tup:
            list_ordered_values.append(t[0])
        return list_ordered_values    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        dictvar = dict()
        for var in self.crossword.variables:
            if not var in assignment:
                dictvar[var] = len(self.domains[var])
        print("dictvar", dictvar)        
        tup = sorted(dictvar.items(), key=lambda x:x[1])  
        print("tup", tup) 
        list_ordered_values = []
        list_ordered_values1 = []
        list_ordered_values2 = []
        for t in tup:
            # vars
            list_ordered_values.append(t[0])
            # minimum remaining value
            list_ordered_values1.append(t[1])
            # degree
            list_ordered_values2.append(len(self.crossword.neighbors(t[0])))
        if len(list_ordered_values1) > 1:
            if list_ordered_values1[0] == list_ordered_values1[1]:
                return list_ordered_values[0] if list_ordered_values2[0] >= list_ordered_values2[1] else list_ordered_values[1] 
            else:
                return list_ordered_values[0]
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print("assig", assignment)
        if self.assignment_complete(assignment):
            return assignment
        
        unvar = self.select_unassigned_variable(assignment)   
        print("unvar", unvar) 
        for val in self.domains[unvar]:
            new_assignment = assignment.copy()
            new_assignment[unvar] = val            
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result != None:
                    return result     
                                  
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
