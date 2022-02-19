library(devtools)
source_url("https://raw.githubusercontent.com/fdrtd/client-r/main/src/fdrtd.r")

source("shared.r")

SECRET_BOB <- 16.0
NETWORK_BOB <- list(nodes=NODES, myself=1)    # Bob is no. 1 out of 0, 1, 2.

api <- Api(URL_BOB)
microservice <- api$create(kwargs=list(protocol="Simon"))
compute <- microservice$attribute("compute")
result <- compute$call(list(), list(microprotocol="SecureSum", data=SECRET_BOB, network=NETWORK_BOB, tokens=TOKENS))
print(api$download(result))
