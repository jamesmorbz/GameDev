class GridChecker:
    def __init__(self, final_board, variant="classic"):
        self.final_board = final_board
        self.variant = variant # Later Allow different Versions??

    def row_checker(self):
        errors = []
        dupes = []
        valid_row = [1,2,3,4,5,6,7,8,9]
        for index, row in enumerate(self.final_board):
            if valid_row != sorted(row):
                errors.append(index+1)
        if len(errors) == 0:
            print("The Grid is Valid!")
        else:
            print(f"Row(s) {errors} are not valid as they contain duplicates!")
            for index in errors:
                row = self.final_board[index-1]
                for val in row:
                    if row.count(val) > 1:
                        findings = (index,val)
                        if findings not in dupes:
                            dupes.append((index,val))
                    else:
                        pass
            for tuple in dupes:
                print(f"Row {tuple[0]} had duplicate {tuple[1]}s!")
    
    def column_checker():
        pass

    def box_checker():
        pass