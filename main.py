#importing necessary modules
from tkinter import *
from tkinter import ttk
from login import Login
from tools.calculator import Calculator
from tools.notepad import Notepad
from tools.statusBar import StatusBar
from tabs.addCustomer import AddCustomer
from tabs.addFile import AddFile
from tabs.dashboard import Dashboard
from tabs.about import About
from tabs.customers import Customers
from tabs.helpMenu import HelpMenu
from tabs.profile import Profile
from tabs.files import Files
from tabs.ledger import Ledgers
from tabs.addLoanRequest import AddLoanRequest

from config.colorConfig import MAINFRAMECOLOR, TOOLFRAMECOLOR, TABCOLOR, TOOLFRAMECOLOR, STATUSBARCOLOR

class Finoshok:
    def __init__(self, root):
        #making a menubar
        mainMenubar = Menu(root)
        
        #making submenubarss
        submenu = Menu(mainMenubar, tearoff=0)
        submenu.add_command(label="Customers", command=self.customer)
        submenu.add_command(label="Add Customer", command=self.addCustomer)
        
        submenu.add_command(label="Add new file", command=self.addFile)
        submenu.add_command(label="Add Credit Request", command=self.addLoanRequest)
        submenu.add_command(label="Files", command=self.files)

        #adding submenu in mainmenybar
        mainMenubar.add_cascade(menu=submenu, label="File")
        
        #adding personal finance option in menu
        # mainMenubar.add_command(label="Personal Finance", command=self.personalFinance)

        #adding settings menu option
        # mainMenubar.add_command(label="Settings", command=lambda:self.addTab("Settings"))

        #about object made out from About class to show information related the software
        About(mainMenubar)

        #creating a help menu item in Mainmenubar

        HelpMenu(mainMenubar)

        #configuring the menu in root as mainmenubar
        root.config(menu=mainMenubar)

        
        #creating a status bar
        statusBar = StatusBar(root)

        #creating toolFrame in root

        toolFrame = Frame(root, bg=TOOLFRAMECOLOR)
        toolFrame.pack(side="left", fill="y")

        noteFrame = Frame(toolFrame, bg=TOOLFRAMECOLOR, borderwidth=2, relief="groove")
        noteFrame.pack(side="top", fill="both", expand=True)

        calculatorFrame = Frame(toolFrame, bg=TOOLFRAMECOLOR, borderwidth=2, relief="groove")
        calculatorFrame.pack(side="bottom")
        

        #binding widgets to keyBoardHandler for key event anc creating a calculator
        calc = Calculator(calculatorFrame)
        
        #create mini notepad
        notepad = Notepad(noteFrame, 200, 200)

        #CREATING main frame in root

        mainFrame = Frame(root, bg=MAINFRAMECOLOR)
        mainFrame.pack(fill="both", expand=True)

        #creating a notebook of tabs in mainframe

        self.myNotebook = ttk.Notebook(mainFrame)
        self.myNotebook.pack(fill="both", expand=True)

        #making a dictionary to hold tabs by their names so that we can manipulate and navigate to tabs without any confustion later
        self.tabsDictionary = {}

        #creating a addFileObjects variable because to hold addFile class objects
        self.addFileObjects = []

        #creating a customerObjects variable because to hold Customer class objects
        self.customerObjects = []

        #creating a filesObject variable because to hold Files class objects
        self.filesObjects = []
        self.viewLedgerObjects = []

        #creating a viewCustomerObjects variable because to hold Customers class objects
        self.viewCustomerObjects = []

        #creating uncloasable dashboard
        # self.addTab("Dashboard", closeBtn=False)
        # Dashboard(self.tabsDictionary["Dashboard"])
        self.customer()
        self.addCustomer()

    #method or function to add tabs in myNotebook, it takes one parameter tabName which has store tab's name
    def addTab(self, tabName, multiple=False, closeBtn=True):
        #check if the tab is already present in tabsDictionary so that we do not create the same tab again
        if(tabName not in self.tabsDictionary.keys()):
            #tabframe to hold contents of the tab
            tabFrame = Frame(self.myNotebook, bg=TABCOLOR)
            tabFrame.pack(fill="both", expand=True)

            #creating close button to close tabs. if it is not false only then
            if(closeBtn):
                closeButton = Button(tabFrame, text="X", bg="red", fg="white", command=lambda:self.closeTab(tabName))
                closeButton.pack(anchor=NE, ipadx=15)

            #appending tab in the dictionary with their tab names
            self.tabsDictionary[tabName]=tabFrame

            #now adding the frame as a tab in myNotebook
            self.myNotebook.add(tabFrame, text=tabName)
            
            #selecting the tab after creating it
            tabIndex = list(self.tabsDictionary.keys()).index(tabName)
            self.myNotebook.select(tabIndex)
            
            #return true if tab created successfully.
            return tabName
        
        #if the caller has stated multiple = True then new tab with former name with an increment will be created
        elif(multiple):
            count=1 # base count
            baseTabName = tabName #base tabname set to the tabname

            #continously try to add tab until its created . after createing return tabName
            while(True):
                #dynamictab name changes with time
                dynamicTabName = baseTabName+f" {count}" 

                #it contains the return value of function 
                returnValue = (self.addTab(dynamicTabName, multiple=False)) 

                 #if returnvalue is tabname then return it to the caller
                if(returnValue):
                    return returnValue
                else:
                    #else continue the loop until the creation of tab

                    #incrementing the count
                    count+=1
                    continue

        else:
            #return false if tab already exists and selecting the preexisting tab
            tabIndex = list(self.tabsDictionary.keys()).index(tabName)
            self.myNotebook.select(tabIndex)
            return False
    
    
    #this function close the tab with associated with tabName and updates the dictionary by deleting the corresoponding key -velue pair
    def closeTab(self, tabName):
        tabIndex = list(self.tabsDictionary.keys()).index(tabName)
        self.myNotebook.forget(tabIndex)
        self.tabsDictionary.pop(tabName)
     
    #this adds a customer tab in the notebook
    def addCustomer(self):
        #it calls addtab function to add tab named Add Customer + count
        tabName = self.addTab("Add Customer", multiple=True)

        # adding contents of AddCustomer class to the add customer tab
        AddCustomer(self.tabsDictionary[tabName], parentUpdateStatus=self.updateStatus)

    #this adds a new file tab in notebook
    def addFile(self):
        #it calls addtab function to add tab named Add FIle + count
        tabName = self.addTab("Add File", multiple=True)

        # adding contents of AddCustomer class to the add customer tab and apending the AddFile class object
        self.addFileObjects.append (AddFile(self.tabsDictionary[tabName]))
    
    #this function adds a tab of addLoanRequest
    def addLoanRequest(self):
        #it calls addtab function to add tab named Add Loan Request + count
        tabName = self.addTab("Add Loan Request", multiple=True)
         # adding contents of AddLoanRequest class to the add loan request tab
        AddLoanRequest(self.tabsDictionary[tabName])

    #function personalFinance will handle actions related to the user's own finance
    def personalFinance(self):
        self.addTab("Personal Finance")

    #this function will create a customers tab where you can search for custoemrs and know their details
    def customer(self):
        tabName = self.addTab("Customers", multiple=True)
        # adding contents of Customer class to the Custoemrs tab
        tempObject =Customers(self.tabsDictionary[tabName])
        #configuring function for viewCustomerButton in Customers Class
        tempObject.viewCustomerButton.config(command=lambda customerObject=tempObject:self.viewCustomer(customerObject=customerObject))
        #now appending the tempObject to customerObjects
        self.customerObjects.append(tempObject)

    #this function makes a tab to show profile of particular customer
    def viewCustomer(self, customerObject=None, **kwargs):
        if(customerObject):
            tabName = self.addTab(customerObject.customerEntryVar.get())
            #appending the Client object into viewCustomerObjects
            if(tabName):
                profileObject = Profile(self.tabsDictionary[tabName], customerObject.aadharEntryVar.get(), updateStatus = self.updateStatus)
                fileId = profileObject.fileId
                def ledgerViewkaro():
                    print(profileObject.fileId)
                    self.viewLedger(filesObject=None, fileId=profileObject.fileId, name=customerObject.customerEntryVar.get())
                if(fileId):
                    profileObject.viewLedgerButton.config(command=ledgerViewkaro)

                self.viewCustomerObjects.append(profileObject)
        elif(kwargs["aadhar"] and kwargs["name"]):
            tabName = self.addTab(kwargs["name"])
            #appending the Client object into viewCustomerObjects
            if(tabName):
                profileObject = Profile(self.tabsDictionary[tabName], kwargs["aadhar"], updateStatus = self.updateStatus)
                fileId = profileObject.fileId
                
                if(fileId):
                    profileObject.viewLedgerButton.config(command=lambda filesObject=None, fileId=fileId, name=customerObject.customerEntryVar.get():self.viewLedger(filesObject=filesObject, fileId=fileId, name=name))

                self.viewCustomerObjects.append(profileObject)
    
    def files(self):
        tabName = self.addTab("Files", multiple=True)
        # adding contents of Files class to the Files tab
        tempObject =Files(self.tabsDictionary[tabName])
        #configuring function for viewledgerbutton in Files Class
        tempObject.viewLedgerButton.config(command=lambda filesObject=tempObject:self.viewLedger(filesObject=filesObject))
        #now appending the tempObject to customerObjects
        self.filesObjects.append(tempObject)

    def viewLedger(self, filesObject=None, **kwargs):
        if(filesObject):
            tabName = self.addTab(filesObject.customerNameVar.get()+" file")
            #appending the Client object into viewCustomerObjects
            if(tabName):
                self.viewLedgerObjects.append(Ledgers(parentWindow=self.tabsDictionary[tabName], fileId=filesObject.currentFileId, updateStatus = self.updateStatus))
        elif(kwargs["fileId"] and kwargs["name"]):
            tabName = self.addTab(kwargs["name"]+" file", multiple=True)
            #appending the Client object into viewCustomerObjects
            if(tabName):
                self.viewLedgerObjects.append(Ledgers(parentWindow=self.tabsDictionary[tabName], fileId=kwargs["fileId"], updateStatus = self.updateStatus))

    #this functions changes status in stausbar and tabname's
    def updateStatus(self, **kwargs):
        data = kwargs
        dataKeys = list(data.keys())
        if("tabName" in dataKeys):
            #getting index of current tab
            index = self.myNotebook.index("current")
            
            #changing tabName of current selectedTab
            newTabName = self.myNotebook.tab(index, text=data["tabName"])
        
        #viewing the customer if aadhar and name is defined with it 
        if("aadhar" in dataKeys and "name" in dataKeys):
            self.viewCustomer(aadhar=data["aadhar"], name=data["name"])


if __name__=="__main__":
    #login window 
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("200x200")
    login_window.resizable(False, False)
    
    #passing login_window to login class to make working login window
    Login(login_window)
    login_window.mainloop()

    # checking if the credentials are correct
    
    if(login_window.result):
        #initiating the gui
        root = Tk()
        root.geometry("1000x630")
        root.title("finoshok")
        Finoshok(root)

        root.mainloop()