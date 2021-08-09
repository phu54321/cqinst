const http = require('http')
const url = require('url')
const { exec } = require('child_process')
const { quote } = require('shell-quote')

const cmdRegex = /^choco install ([A-Za-z0-9_-])+$/

// create a server object:
http.createServer(function (req, res) {
  const queryObject = url.parse(req.url, true).query
  res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-cache' })
  res.write('Success')
  res.end()

  console.log(queryObject)
  const { cmd } = queryObject
  if (!cmd) return
  if (cmdRegex.test(cmd)) {
    const ps = quote(['Start-Process', 'cmd', '-Verb', 'RunAs', '-ArgumentList', '/c ' + cmd])
    const runner = quote(['powershell', '-Command', ps])
    // console.log(runner)
    exec(runner)
  }
}).listen(22567, 'localhost')
