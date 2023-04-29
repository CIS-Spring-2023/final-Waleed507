// Waleed Yusuf
// 2104654

// Credit:
//Class work/Templates
// w3schools (JS + EJS Code)
// https://stackoverflow.com/questions/6358673/javascript-checkbox-onchange (EJS Code)
// https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector (EJS Code)

//Packages
const express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
const app = express();
const axios = require("axios");
const port = 3000;
// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");
//setup public folder
app.use(express.static("./public"));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
// parse application/json
app.use(bodyParser.json());

//Home page
app.get("/", function (req, res) {
  res.render("pages/home");
});

//Login Page
app.post("/login_page", function (req, res) {
  const { username, password } = req.body;

  if (username === "username" && password === "password") {
    res.redirect("/current_cargo");
  } else {
    res.redirect("/");
  }
});
// View Current Cargo
app.get("/current_cargo", function (req, res) {
  //GET Request to API to get the cargo data
  axios.get("http://127.0.0.1:5000/cargo").then((response) => {
    cargosData = response.data[0];
    //If showArrived is on, meaning if the checkbox is checked
    showArrived = req.query.showArrived === "on";
    filteredCargos = cargosData.filter((cargo) => {
      return (
        // checkbox is checked and arrival value is not null
        (showArrived && cargo.arrival !== null) ||
        new Date(cargo.arrival) > new Date()
      );
    });
    // Render the cargostatus page to display the data
    res.render("pages/cargostatus", {
      cargos: filteredCargos,
      showArrived: showArrived,
    });
  });
});
// View Spaceships
app.get("/spaceship", function (req, res) {
  axios.get("http://127.0.0.1:5000/spaceship").then((response) => {
    spaceship = response.data[0]; // Get the JSON data into spaceship
    res.render("pages/spaceships", {
      spaceships: spaceship,
    });
  });
});
// Add Spaceships
app.post("/add_spaceship", function (req, res) {
  // Get maxweight and captainid from the text input
  maxWeight = req.body.maxweight;
  captainId = req.body.captainid;
  axios
    .post("http://127.0.0.1:5000/spaceship", {
      maxweight: maxWeight,
      captainid: captainId,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/spaceship");
    });
});

// Update Spaceship
app.post("/update_spaceship/:id", function (req, res) {
  id = req.params.id; //Get the id from the URL
  maxWeight = req.body.maxweight;
  captainId = req.body.captainid;
  axios
    // Insert the input id into URL and request from python code
    .put(`http://127.0.0.1:5000/spaceship/${id}`, {
      maxweight: maxWeight,
      captainid: captainId,
    })
    .then((response) => {
      console.log(response.data);
      res.redirect("/spaceship");
    });
});

// Delete Spaceship
app.post("/delete_spaceship/:id", function (req, res) {
  id = req.params.id; // Get the ID from URl
  axios.delete(`http://127.0.0.1:5000/spaceship/${id}`).then((response) => {
    console.log(id);
    res.redirect("/spaceship"); // Redirecting to same page after the button is clicked
  });
});

app.listen(port, () => console.log(`MasterEJS app Started on port ${port}!`));
