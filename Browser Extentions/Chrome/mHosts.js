const menu = document.getElementById("menu");
fetch("http://127.0.0.1:1994/apis/hosts/list.json")
    .then(function (value) {
        return value.json()
    })
    .then(function (json) {
        menu.innerHTML = json.result.map(item => `<li data-id="${item.id}">${item.name}</li>`).join("")
    });

menu.addEventListener("click", function (e) {
    const item = e.path[0]
        , id = item.getAttribute("data-id");
    fetchProxyServerInfo(id)
});

function fetchProxyServerInfo(id) {
    fetch(`http://127.0.0.1:1994/apis/proxy/${id}.json`)
        .then(res => res.json())
        .then(json => {
            setProxy(json.result.port)
        })
}

function setProxy(port) {
    const host = "127.0.0.1";
    chrome.proxy.settings.set({
        value: {
            mode: "fixed_servers",
            rules: {
                proxyForHttp: {
                    scheme: 'http',
                    host: host,
                    port: port
                },
                proxyForHttps: {
                    scheme: 'http',
                    host: host,
                    port: port
                },
            }
        }
    })
}
