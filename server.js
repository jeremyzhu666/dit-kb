// Minimal static file server for the DIT knowledge base site.
// Accepts --port / --host (and PORT/HOST env) so `npm run dev -- --port N` works.
const http = require("http");
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
function arg(name, dflt) {
  const i = args.indexOf("--" + name);
  return i !== -1 && args[i + 1] ? args[i + 1] : dflt;
}
const PORT = parseInt(arg("port", process.env.PORT || "7100"), 10);
const HOST = arg("host", process.env.HOST || "0.0.0.0");
const ROOT = path.join(__dirname, "public");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".svg": "image/svg+xml",
};

http.createServer((req, res) => {
  let urlPath = decodeURIComponent(req.url.split("?")[0]);
  if (urlPath.endsWith("/")) urlPath += "index.html";
  const file = path.join(ROOT, path.normalize(urlPath).replace(/^([/\\])+/, ""));
  if (!file.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" }); res.end("404 Not Found"); return; }
    res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
    res.end(data);
  });
}).listen(PORT, HOST, () => {
  console.log(`DIT KB site: http://localhost:${PORT}/`);
});
