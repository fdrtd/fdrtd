class HttpInterface {
    constructor(root) { this.root = root; }
    post(path, body) { return this.call("POST", path, body); }
    put(path, body) { return this.call("PUT", path, body); }
    patch(path, body) { return this.call("PATCH", path, body); }
    get(path) { return this.call("GET", path, null); }
    delete(path) { return this.call("DELETE", path, null); }
    call(verb, path, body) {

        var url = this.root;
        for (var index = 0; index < path.length; index++) {
            let item = path[index];
            if(item[0] === '/') {
                url = url + item;
            } else {
                url = url + '/' + item;
            }
        }

        if(verb === "GET" || verb === "DELETE") {
            return fetch(url, {method: verb})
                .then(response => { return response.json(); })
                .catch(function(res){ console.log(res) });
        } else {
            return fetch(url, {method: verb,
                body: JSON.stringify(body),
                headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}})
                .then(response => { return response.json(); })
                .catch(function(res){ console.log(res) });
        }
    }
}

class Representation {

    constructor(api, representation_uuid) {
        this.api = api;
        this.representation_uuid = representation_uuid;
    }

    attribute(name) {
        return this.api.attribute(this.representation_uuid, name);
    }

    call(args, kwargs) {
        return this.api.call(this.representation_uuid, args, kwargs);
    }
}

class Api {

    constructor(args) {
        if("url" in args) {
            this.interface = new HttpInterface(args.url);
        } else if("interface" in args) {
            this.interface = args.interface;
        }
    }

    list() {
        return this.interface.get(['representations']);
    }

    create(args, kwargs) {
        return this.interface.post(['representations'], {args: args, kwargs: kwargs})
            .then(response => {
                return new Representation(this, response["uuid"]);
            })
    }

    upload(args, kwargs) {
        return this.interface.put(['representations'], {args: args, kwargs: kwargs})
            .then(response => {
                return new Representation(this, response["uuid"]);
            })
    }

    call(representation_uuid, args, kwargs) {
        return this.interface.patch(['representation', representation_uuid], {args: args, kwargs: kwargs})
            .then(response => {
                if(response["type"] === "uuid") {
                    return new Representation(this, response["uuid"]);
                }
                return null;
            })
    }

    download(representation) {
        return this.interface.get(['representation', representation['representation_uuid']])
            .then(response => {
                return response["object"];
            })
    }

    release(representation_uuid) {
        this.interface.delete(['representation', representation_uuid]);
        return null;
    }

    attribute(representation_uuid, member_name) {
        return this.interface.get(['representation', representation_uuid, member_name])
            .then(response => {
                return new Representation(this, response["uuid"])
            })
    }
}
