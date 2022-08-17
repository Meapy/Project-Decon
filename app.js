const express = require("express");
const session = require("express-session");
const nconf = require("nconf");
const bodyParser = require("body-parser");
const path = require("path");
const app = express();
var cookieParser = require('cookie-parser');

app.use(cookieParser());
app.use(express.static(__dirname + '/assets'));
app.use(express.static(__dirname + '/vendor'));
// load config file
nconf
  .argv()
  .env()
  .file({
    file: __dirname + "/config.json",
  });


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));


// set static path
app.set("views", path.join(__dirname, "/views"));
app.engine("html", require("ejs").renderFile);

// routes
app.use("/", require("./routes/static"));
app.use("/users", require("./routes/users"));

// start the app
app.listen(nconf.get("port") || 5000);
console.log("App Started...");
