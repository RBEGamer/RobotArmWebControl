from subprocess import check_output
import subprocess


scanoutput = check_output(["iwgetid"])
print scanoutput

def do_update():
  print("-- IN DEV WIFI --")
  process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print output
  
  process_ard = subprocess.Popen(["bash", "./upload_arduino_sketch.sh"], stdout=subprocess.PIPE)
  output_ard = process_ard.communicate()[0]
  print output_ard
  
  
  print output

if "Keunecke2" in scanoutput:
  do_update()
elif "Keunecke" in scanoutput:
  do_update()
  
print "-- UPDATER SCRIPT FINISHED ---"

exit(0)
  

    

