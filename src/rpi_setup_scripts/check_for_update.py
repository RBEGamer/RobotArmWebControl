from subprocess import check_output
import git 


scanoutput = check_output(["iwgetid"])
print scanoutput

def do_update():
  print("-- IN DEV WIFI --")
  g = git.cmd.Git("./../../")
  g.pull()

if "Keunecke2" in scanoutput:
  do_update()
elif "Keunecke" in scanoutput:
  do_update()
  
print "-- UPDATER SCRIPT FINISHED ---"

exit(0)
  

    

