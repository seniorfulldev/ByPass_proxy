// const ProxyLists = require("proxy-lists");
const cloudscraper = require("cloudscraper");
const jar = cloudscraper.jar;
const fs = require("fs");
const args = require("minimist")(process.argv.slice(2));
// cloudscraper.debug = true

const results = {};
const failing = "\u001B[0;31m\u001B[1m\u001B[5mx\u001B[0m";
const passing = "\u001B[0;32m\u001B[1m\u001B[5m✓\u001B[0m";

let id = -1,
  attempts = 0,
  max = 30,
  timeout = 60000;

process.on("uncaughtException", console.error);
process.on("unhandledRejection", console.error);

// ProxyLists.getProxies({ protocols: ["http"] })
//   .on("data", (proxies) =>
//     proxies.map((o) => test(`http://${o.ipAddress}:${o.port}`))
//   )
//   .on("error", (error) => console.error(error.message));

const proxies = fs
  .readFileSync(args["proxyfile"], "utf-8")
  .toString()
  .split("\n");

for (var i = 0; i < proxies.length; i++) {
  const testproxy = proxies[i];
  test(`http://${testproxy}`);
}

async function test(proxy, url = "https://linktracker.pro") {
  if (attempts++ > max) return;
  if (id === -1) id = setTimeout(stop, timeout);
  console.log("proxy", proxy);
  try {
    results[proxy] = "timed out";
    const html = await cloudscraper.get({ proxy, url, jar: jar() });

    console.info(proxy, "\t\t", (results[proxy] = passing));
    console.info("Result:\n", preview(html));
  } catch (error) {
    console.error(proxy, "\t\t", (results[proxy] = failing));
    console.error(error.name + ":", error.message);
    if (error.response) {
      console.error("ErrorResult:\n", preview(error.response.body));
    }
  }
}

function preview(html) {
  try {
    return String(html).match(/<title>([\S\s]+)<\/title>/i)[0];
  } catch (e) {
    return html ? String(html).slice(0, 77) + "..." : html;
  }
}

function stop() {
  for (let url in results) {
    // console.log(url, '\t\t', results[url])
    console.log(results[url] === passing ? "pass:" : "fail:", url);
  }

  process.exit(0);
}
