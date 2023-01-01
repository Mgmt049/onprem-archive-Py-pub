#Kevin Faterkowski
#2020 - original version - purpose is to compress and archive a given set of network folders to a specified folder
#12-29-2022 - genericized and made into a class definition
####################################################################################
#client code must provide 1 mandatory upon calling __init()__: "dest_folder" as a UNC or local windows file path
#client code must call set_paths() at least once - or else nothing will be compressed * arvhived
#archive_folders() method actually triggers/executes the primary functionality and sends an email notification
####################################################################################
import os
import zipfile
import smtplib
import datetime

class folder_archive:
   
    def __init__(self, 
                 dest_folder  #folder to store the resultant compressed archive...
                 ):
        
        #https://stackoverflow.com/questions/2825452/correct-approach-to-validate-attributes-of-an-instance-of-class
        if os.path.exists( dest_folder ):  #see above param list )
            self.dest_folder = dest_folder
        else:
            
            raise Exception("the destination archive folder path is invalid, destroying object now..")
            del(self)
            return
        
        self.archive_paths = []  #list of folder locations to be archived
        self.sender = ""  #admin email sender who is running script
        self.recipients = ()  #emails to be notified aupon completions
        self.SMTP = ""  #email server for notification
    #end of init()
    
    #destructor
    def __del__( self ):
        pass
        #print( "object is destroyed" )
    
    # def set_dest( self, dest_path ):
    # #set the path for the archive folder to be stored:
    #     self.dest_folder = dest_path
    # #end of set_dest function

    def get_dest( self ):
    #get the path for the archive folder to be stored:
        print( self.dest_folder )
    #end of get_dest function

    def set_paths( self, 
                  folder_path  #folder path to be compressed and archived
                  ):
        #adds another folder path onto the list of file paths to be compressed and archived
        print("folder path in set_paths %s"%(folder_path))       
        
        #validate that the path exists before adding it to the list[]
        if os.path.exists(folder_path):

            self.archive_paths.append( folder_path ) #python lists do not have a push()
            
        else:
            print("location passed to set_path() is invalid, please pass a valid path to set_path()")
    
    #end set_paths function

    def set_recipients( self, emails ):
        
        #tuple passed to this function, adds recipient emails to list
        
        for email in emails:
            self.GLOBALS["recipients"].append(email) #python lists do not have a push()
        
    #end set_emails method
        
    def get_paths( self ):
        
        #display all to-be-archived paths to the caller
        #print( GLOBALS["archive_paths"] )
        for path in self.archive_paths:
            print(path)
        
    #end get_path method

    #def archive_WV( backup_folder, *args ): #now using a variable number of method arguements
    def archive_folders( self, SMTP, sender, recipients ):
    
        now = datetime.datetime.now() #retrieve date into string
        formatted_date = now.strftime("%m-%d-%Y")
        
        try:
    
            #for path in paths:  #for each folder path that is passed to this archive_folders() method
            for path in self.archive_paths:  #for each folder path that is passed to this archive_folders() method
        
                parsed_args = path.split('\\') #parse folder name to get the "last" element to use for archive file name
        
                #create/open the new Zipfile object to begin writing app folder to
                #https://code.tutsplus.com/tutorials/compressing-and-extracting-files-in-python--cms-26816
                
                with zipfile.ZipFile( self.dest_folder + parsed_args.pop() + '_' + formatted_date + '.zip', 'w') as WV_zip: #create a filename
                #solution found here: https://www.pythoncentral.io/how-to-traverse-a-directory-tree-in-python-guide-to-os-walk/
                    for folder, subfolders, files in os.walk( path ):
                         
                        for file in files:
            
                            print( folder + "\\" + file )
                            #write every file to the zipped file object:
                            WV_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), path), compress_type = zipfile.ZIP_DEFLATED)
                             
                WV_zip.close()

            #set the email-related instance variables and call them:
            self.sender = sender  #the email sender
            self.recipients = recipients  #the list of email recipients
            self.SMTP = SMTP  #the SMTP email server for notification
            self.send_email()  
        
        # If there is any permission issue
        except PermissionError as pe:
            print("Permission denied.", pe)
        
    #end method
            
    def send_email ( self ):

        print("send_email() called")

        date_time = datetime.datetime.now() #retrieve date into string
        
        #must include the newline char to separate subject, msg
        message = '''Subject: folder archive results\n\n     
    
        Successfully backed up application folder at %s at location %s
        ''' % (date_time.strftime("%x"), self.dest_folder )
    
        try:
           smtpObj = smtplib.SMTP( self.SMTP )
           smtpObj.sendmail(self.sender, self.recipients, message)  #including a subject causes an error
           smtpObj.quit()
    
           print ("Successfully BACKED UP the requested folder")
           
        except smtplib.SMTPException as se:
            print("SMTP exception sending mail", se)

#end of class folder_archive

##########################################################################################################
#the below is an example main(), some instatantiation examples, and necessary method call examples....
##########################################################################################################

#def main():
    
    #initialize object with destination folder path:
   
    #folders_to_archive = folder_archive('\\\\<UNC-path-to-archive-destination-server>\\<folder>\\<subfolder1>\\<subfolder2>\\')

    
    #folders_to_archive.set_paths( '\\\\<UNC-path-to-server-1>\\<folder>\\<subfolder1>\\<subfolder2>\\' )
    #folders_to_archive.set_paths( '\\\\<UNC-path-to-server-2>\\<folder>\\<subfolder1>\\<subfolder2>\\' )
    #folders_to_archive.set_paths( '\\\\<UNC-path-to-server-3>\\<folder>\\<subfolder1>\\<subfolder2>\\' )
    
    #folders_to_archive.archive_folders( '<SMTP-email-server>' , '<emailsender@domain.com>', ('<email-recipient1@domain.com>', '<email-recipient1@domain.com>'))
    
    #print("BACKUP SCRIPT COMPLETED")

#"main" module call: 
#if __name__ == "__main__":
#    main()
