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


module.exports = router;
