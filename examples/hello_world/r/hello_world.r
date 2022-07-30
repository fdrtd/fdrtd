library(devtools)
source_url("https://raw.githubusercontent.com/bytesforlife/representation/main/r/representation.r")

api <- Api("http://127.0.0.1:55501")
lst <- api$report()
print(lst)
