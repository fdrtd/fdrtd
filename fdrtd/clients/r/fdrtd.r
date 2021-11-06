library(httr)

# library(logging)
# basicConfig()

HttpInterface = setRefClass("HttpInterface",
    fields = list(root="character"),
    methods = list(
        initialize = function(root="") { .self$root = root },
        post = function(path, body) { return(call(POST, "POST", path, body)) },
        put = function(path, body) { return(call(PUT, "PUT", path, body)) },
        patch = function(path, body) { return(call(PATCH, "PATCH", path, body)) },
        get = function(path) { return(call(GET, "GET", path, NULL)) },
        delete = function(path) { return(call(DELETE, "DELETE", path, NULL)) },
        buildurl = function(path) {
            url = .self$root
            for (p in unlist(path)) {
                if(substr(p, 1, 1) == '/') {
                url = paste(url, p, sep="")
                } else {
                url = paste(url, p, sep="/")
                }
            }
            return(url)
        },
        call = function(fn, method, path, body) {
            url = buildurl(path)
            if(is.null(body)) body = list(ignore="R compatibility issues")
            response = fn(url, body = body, encode = "json")
            status_code = status_code(response)
            content_text = content(response, "text", encoding="UTF-8")

            if(status_code %in% c(200, 201, 202, 204) == FALSE) {
                message = WDlogfile960323_line(method, url, status_code, content_text)
                # logerror(message)
                stop(message)
            }

            # message = WDlogfile960323_line(method, url, status_code)
            # loginfo(message)

            if(content_text == '') {
                return(NULL)
            }

            return(content(response, as="parsed"))
        },
        WDlogfile960323_line = function(method="-", uri="-", status="-", comment="-") {
            formatted_date = Sys.Date()
            formatted_time = format(Sys.time(), "%H:%M:%S")
            return(paste(formatted_date, '\t', formatted_time, '\t', method, '\t', uri, '\t', status, '\t', human_readable(status), '\t', comment))
        },
        human_readable = function(status) {
            if(status == 100) return('Continue')
            if(status == 101) return('Switching Protocols')
            if(status == 200) return('OK')
            if(status == 201) return('Created')
            if(status == 202) return('Accepted')
            if(status == 203) return('Non-Authoritative Information')
            if(status == 204) return('No Content')
            if(status == 205) return('Reset Content')
            if(status == 206) return('Partial Content')
            if(status == 300) return('Multiple Choices')
            if(status == 301) return('Moved Permanently')
            if(status == 302) return('Found')
            if(status == 303) return('See Other')
            if(status == 304) return('Not Modified')
            if(status == 305) return('Use Proxy')
            if(status == 307) return('Temporary Redirect')
            if(status == 400) return('Bad Request')
            if(status == 401) return('Unauthorized')
            if(status == 402) return('Payment Required')
            if(status == 403) return('Forbidden')
            if(status == 404) return('Not Found')
            if(status == 405) return('Method Not Allowed')
            if(status == 406) return('Not Acceptable')
            if(status == 407) return('Proxy Authentication Required')
            if(status == 408) return('Request Timeout')
            if(status == 409) return('Conflict')
            if(status == 410) return('Gone')
            if(status == 411) return('Length Required')
            if(status == 412) return('Precondition Failed')
            if(status == 413) return('Payload Too Large')
            if(status == 414) return('URI Too Long')
            if(status == 415) return('Unsupported Media Type')
            if(status == 416) return('Range Not Satisfiable')
            if(status == 417) return('Expectation Failed')
            if(status == 426) return('Upgrade Required')
            if(status == 500) return('Internal Server Error')
            if(status == 501) return('Not Implemented')
            if(status == 502) return('Bad Gateway')
            if(status == 503) return('Service Unavailable')
            if(status == 504) return('Gateway Timeout')
            if(status == 505) return('HTTP Version Not Supported')
            return('n/a')
        }
    )
)

Api = setRefClass("Api",
  fields = list(http_interface="HttpInterface"),
  methods = list(
    initialize = function(root="") {
      .self$http_interface = HttpInterface$new(root)
    },
    report = function() {
    	return(.self$http_interface$get(c('representations')))
    },
    create = function(args=NULL, kwargs=NULL) {
        response <- .self$http_interface$post(c('representations'), list(args=args, kwargs=kwargs))
    	return(Representation$new(.self, response$uuid))
    },
    upload = function(args=NULL, kwargs=NULL) {
        response <- .self$http_interface$put(c('representations'), list(args=args, kwargs=kwargs))
    	return(Representation$new(.self, response$uuid))
    },
    call = function(representation_uuid, args=NULL, kwargs=NULL) {
        response <- .self$http_interface$patch(c('representation', representation_uuid), list(args=args, kwargs=kwargs))
    	if(response['type'] == 'uuid') {
        	return(Representation$new(.self, response$uuid))
    	}
    	return(NULL)
    },
    download = function(representation) {
        response <- .self$http_interface$get(c('representation', representation$representation_uuid))
     	return(response$object)
    },
    release = function(representation_uuid) {
        response <- .self$http_interface$delete(c('representation', representation_uuid))
    	return(NULL)
    },
    attribute = function(representation_uuid, member_name) {
        response <- .self$http_interface$get(c('representation', representation_uuid, member_name))
      	return(Representation$new(.self, response$uuid))
    }
  )
)

Representation = setRefClass("Representation",
    fields = list(api="Api", representation_uuid="character"),
    methods = list(
        initialize = function(api, representation_uuid) {
            .self$api = api;
            .self$representation_uuid = representation_uuid;
        },
        attribute = function(name) {
            return(.self$api$attribute(.self$representation_uuid, name))
        },
        call = function(args, kwargs) {
            return(.self$api$call(.self$representation_uuid, args, kwargs))
        }
    )
)
