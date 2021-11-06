library(devtools)
source_url("https://raw.githubusercontent.com/fdrtd/fdrtd/main/fdrtd/clients/r/fdrtd.r")

api <- Api("http://127.0.0.1:55502")
lst <- api$report()
print(lst)
