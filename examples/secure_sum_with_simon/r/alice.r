library(devtools)
source_url("https://raw.githubusercontent.com/fdrtd/client-r/main/src/fdrtd.r")

source("shared.r")

SECRET_ALICE <- 42.0
NETWORK_ALICE <- list(nodes=NODES, myself=0)    # Alice is no. 0 out of 0, 1, 2.

api <- Api(URL_ALICE)
microservice <- api$create(kwargs=list(protocol="Simon"))
compute <- microservice$attribute("compute")
result <- compute$call(list(), list(microprotocol="SecureSum", data=SECRET_ALICE, network=NETWORK_ALICE, tokens=TOKENS))
print(api$download(result))
