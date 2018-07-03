const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const {execFile} = require('child_process')
const port = 8080

app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())
app.use(express.static(__dirname + '/public'))

app.get("/img", function(req, res) {
  execFile('python3', ['./process.py',req.query.fname], (error, stdout, stderr) => {
    if (error) throw error
    res.send({before: req.query.fname, after: stdout})
  })
})

app.listen(port, () => console.log(`listen on port:${port}`))
