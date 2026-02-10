class FunctionInputHandler:
    """
    Handles inputs connected to specified functions and calls chosen function.
    """
    def __init__(self, title:str, choices=None, secure=False):
        self.secure = secure
        self.title = title
        self.choices = choices if choices is not None else {}
    
    def UpdateTitle(self,title:str):
        """
        Sets the title of the input prompt.
        """
        self.title = title
        
    def AddChoice(self,choiceName:str,callbackFunction:callable):
        """
        Add a choice with a callback function
        """
        self.choices[choiceName] = callbackFunction
        
    def RemoveChoice(self,choiceName:str):
        """
        Remove a choice by the name.
        """
        del self.choices[choiceName]
    def GetInput(self):
        """
        Prompt input from user.
        """
        choice = ""
        choices = []
        
        madeChoice = False
        while not madeChoice:
            while not type(choice) is int:
                print("\n\n"+self.title+"\n")
                choices = []
                for number in self.choices:
                    choices.append(self.choices[number])
                    print(" "+str(len(choices))+". "+number)
                choice = input("    ")
                try:
                    choice = int(choice)
                except:
                    pass
                
            if 1 <= choice <= len(choices):
                if self.secure:
                    prompt = input("Are you sure? (y/n)\n    ")
                    if prompt == "y":
                        madeChoice = True
                        choices[choice-1]()
                else:
                    madeChoice = True
                    choices[choice-1]()
            else:
                print("    Invalid choice!")
            
class StringInputHandler:
    """
    Handles inputs and returns chosen input.
    """
    def __init__(self, title:str, choices=None, secure=False):
        self.secure = secure
        self.title = title
        self.choices = choices if choices is not None else []
    
    def UpdateTitle(self,title:str):
        """
        Sets the title of the input prompt.
        """
        self.title = title
        
    def AddChoice(self,choiceName:str):
        """
        Add a choice.
        """
        self.choices.append(choiceName)
        
    def RemoveChoice(self,choiceName:str):
        """
        Remove a choice by the name.
        """
        self.choices.remove(choiceName)
    def GetInput(self):
        """
        Prompt input from user.
        """
        
        madeChoice = False
        while not madeChoice:
            choice = ""
            while not type(choice) is int:
                print("\n\n"+self.title+"\n")
                idx = 0
                for number in self.choices:
                    idx += 1
                    print(" "+str(idx)+". "+number)
                choice = input("    ")
                try:
                    choice = int(choice)
                except:
                    pass
                
            if 1 <= choice <= len(self.choices):
                if self.secure:
                    prompt = input("Are you sure? (y/n)\n    ")
                    if prompt == "y":
                        madeChoice = True
                        return self.choices[choice-1]
                else:
                    madeChoice = True
                    return self.choices[choice-1]
            else:
                print("    Invalid choice!")