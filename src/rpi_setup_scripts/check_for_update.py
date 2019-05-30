from subprocess import check_output

scanoutput = check_output(["iwgetid"])
print scanoutput
for line in scanoutput.split():
  if line.startswith("ESSID"):
    ssid = line.split('"')[1]
    
print ssid
