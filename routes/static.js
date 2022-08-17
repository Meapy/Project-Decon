const express = require("express");
const { add } = require("nconf");
const app = express();
const router = express.Router();
// static routes

router.get("/", (req, res) => {
  res.render("index.html");
});

router.get("/home", function (req, res) {
  
  res.redirect("/");
});


router.get('/flask', function(req, res) {
  request('http://127.0.0.1:3000/flask', function (error, response, body) {
      console.error('error:', error); // Print the error
      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log('body:', body); // Print the data received
      res.send(body); //Display the response on the website
    });    
    //res.redirect("http://127.0.0.1:3000/flask");  
});

module.exports = router;
