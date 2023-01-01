# onprem-archive-Py-pub
 Python automation: compress and archive  network folder to a given network location
#12-29-2022 - genericized and made into a class definition
####################################################################################
#Note: this is intended to run with Windows task scheduler: 
##Ex command: "Files\Python39\python.exe "C:\REPORTS COPY TOOLS\app_Archive_pub.py""
#client code must provide 1 mandatory upon calling __init()__: "dest_folder" as a UNC or local windows file path
#client code must call set_paths() at least once - or else nothing will be compressed * arvhived
#archive_folders() method actually triggers/executes the primary functionality and sends an email notification
####################################################################################
