library(devtools)
source_url("https://raw.githubusercontent.com/fdrtd/fdrtd/main/fdrtd/clients/r/fdrtd.r")

source("shared.r")

SECRET_CHARLIE <- 99.0
NETWORK_CHARLIE <- list(nodes=NODES, myself=2)    # Bob is no. 1 out of 0, 1, 2.

api <- Api(URL_CHARLIE)
microservice <- api$create(kwargs=list(protocol="Simon"))
compute <- microservice$attribute("compute")
result <- compute$call(list(), list(microprotocol="SecureSum", data=SECRET_CHARLIE, network=NETWORK_CHARLIE, tokens=TOKENS))
print(api$download(result))
