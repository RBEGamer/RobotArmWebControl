from subprocess import check_output



scanoutput = check_output(["iwgetid"])
print scanoutput

def do_update():
  print("-- IN DEV WIFI --")
  process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print output

if "Keunecke2" in scanoutput:
  do_update()
elif "Keunecke" in scanoutput:
  do_update()
  
print "-- UPDATER SCRIPT FINISHED ---"

exit(0)
  

    

