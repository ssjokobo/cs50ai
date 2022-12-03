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
        for var in self.domains:
            to_be_removed = set()
            for word in self.domains[var]:
                if var.length != len(word):
                    to_be_removed.add(word)
            self.domains[var] -= to_be_removed

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        to_be_removed = set()

        i, j = self.crossword.overlaps[(x, y)]
        for x_word in self.domains[x]:
            possible_letters = {y_word[j] for y_word in self.domains[y]}
            if x_word[i] not in possible_letters:
                to_be_removed.add(x_word)

        if to_be_removed != set():
            self.domains[x] -= to_be_removed
            revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))

        while len(arcs) > 0:
            x, y = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
            for z in self.crossword.neighbors(x) - {y}:
                arcs.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # check if all vars are there
        if {var for var in self.domains} - {var for var in assignment} != set():
            return False

        # check if all vars have value as str
        for var in assignment:
            if not isinstance(assignment[var], str):
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check for value duplications
        if len(list(assignment.values())) != len(set(assignment.values())):
            return False

        for var in assignment:
            # check value and variable lengths
            if var.length != len(assignment[var]):
                return False

            # no conflict between neighbors
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    x, y = self.crossword.overlaps[(var, neighbor)]
                    if assignment[var][x] != assignment[neighbor][y]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domains = []
        for word in self.domains[var]:
            n = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    x, y = self.crossword.overlaps[(var, neighbor)]
                    for neighbor_word in self.domains[neighbor]:
                        if word[x] != neighbor_word[y]:
                            n += 1
            domains.append((word, n))

        return [word[0] for word in sorted(domains, key=lambda word: word[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get unassigned varibales
        unassigned_vars = {var for var in self.domains} - {var for var in assignment}

        # sort for lowest-remaining-value variables
        unassigned_vars = [var for var in sorted(unassigned_vars, key=lambda var: len(self.domains[var]))]

        # if tie
        if len(unassigned_vars) > 1 and len(self.domains[unassigned_vars[0]]) == len(self.domains[unassigned_vars[1]]):

            # sort the first two tied items for the higher degree variable
            return sorted(unassigned_vars[:2], key=lambda var: len(self.crossword.neighbors(var)), reverse=True)[0]

        else:
            return unassigned_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        # remember the original domain
        domains_history = self.domains

        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val

            if self.consistent(assignment):

                # update domains of var to selected val
                self.domains[var] = {val}

                # preparing new arcs for ac3
                arcs = []
                for neighbor in self.crossword.neighbors(var):
                    arcs.append((neighbor, var))

                # extra ac3 for inferencing
                self.ac3(arcs)

                assignment = self.backtrack(assignment)
                if assignment:
                    return assignment

            assignment.pop(var)

            # remove inferences by reverting back to domains_history
            self.domains = domains_history

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
