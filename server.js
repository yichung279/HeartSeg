const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const {execFile} = require('child_process')
const port = 18080

app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())
app.use(express.static(__dirname + '/public'))

app.get("/img", function(req, res) {
  execFile('python3', ['./heart_seg.py',req.query.fname], (error, stdout, stderr) => {
    if (error){
      res.send({img_exist: false})
    }else{
      res.send({img_exist: true, before: req.query.fname, after: stdout})
    }
  })
})

app.listen(port, () => console.log(`listen on port:${port}`))
